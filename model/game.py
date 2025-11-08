from .grid import Grid
from .blocked_numbers import BlockedNumberCell
from .blocked_cell import BlockedCell
from .empty_cell import EmptyCell
from .number_cell import NumberCell
from .operation import OperationCell
from .goal import GoalCell
from .player import Player

class Game:
    def __init__(self, grid: Grid, playerPos, goalPos):
        self.grid = grid
        self.playerPos = tuple(playerPos)  # ensure it's a tuple
        self.goalPos = tuple(goalPos)      # also tuple for consistency
        self.is_running = True
        self.turn_count = 0

    def display_grid(self):
        self.grid.display()

    def _update_player_position(self, new_row, new_col):
        """Move the player in the grid."""
        old_row, old_col = self.playerPos
        player_cell = self.grid.grid[old_row][old_col]

        # Move player object
        self.grid.grid[new_row][new_col] = player_cell

        # Set old cell to empty
        self.grid.grid[old_row][old_col] = EmptyCell(old_row, old_col)

        # Update position as a tuple
        self.playerPos = (new_row, new_col)

    def move_player(self, direction):
        row, col = self.playerPos
        d_row, d_col = 0, 0

        # Determine movement direction
        if direction == "W": d_row = -1
        elif direction == "S": d_row = 1
        elif direction == "A": d_col = -1
        elif direction == "D": d_col = 1
        else:
            print("Invalid command!")
            return

        new_row, new_col = row + d_row, col + d_col

        # Check bounds
        if not (0 <= new_row < self.grid.rows and 0 <= new_col < self.grid.cols):
            print("Out of bounds!")
            return

        next_cell = self.grid.grid[new_row][new_col]

        # Blocked or blocked-number cell
        if next_cell.is_blocked() or next_cell.is_blockedNum():
            print("Blocked cell!")
            return

        # Push logic: number or operation
        if next_cell.is_number() or next_cell.is_operation():
            push_row, push_col = new_row + d_row, new_col + d_col

            # Check bounds for push
            if not (0 <= push_row < self.grid.rows and 0 <= push_col < self.grid.cols):
                print("Can't push — out of bounds!")
                return

            push_target = self.grid.grid[push_row][push_col]

            # Only push if target is empty
            if push_target.is_empty():
                # Move the number/operation object
                self.grid.grid[push_row][push_col] = next_cell
                # Set current cell to empty
                self.grid.grid[new_row][new_col] = EmptyCell(new_row, new_col)
                # Move player
                self._update_player_position(new_row, new_col)
            else:
                print("Can't push — cell behind is not empty!")
                return
        else:
            # Normal move into empty or goal
            self._update_player_position(new_row, new_col)

        # After move, check equations
        self.check_equations()
        self.turn_count += 1

    def run(self):
        while self.is_running:
            self.display_grid()
            if self.check_win():
                print("🎉 Congratulations! You reached the goal!")
                break

            command = input("Enter move (W/A/S/D or Q to quit): ").upper()
            if command == "Q":
                self.is_running = False
            else:
                self.move_player(command)

        print("Game over! Total turns:", self.turn_count)

    def check_win(self):
        print(f"Checking win: playerPos={self.playerPos}, goalPos={self.goalPos}")
        return self.playerPos == self.goalPos

    def check_equations(self):
        """Check for Number-Operation-Number patterns and clear any matching blocked-number nearby."""
        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                cell = self.grid.grid[r][c]
                if cell.is_number():
                    # Horizontal check: Number-Operation-Number
                    if c + 2 < self.grid.cols:
                        num1 = cell
                        op = self.grid.grid[r][c + 1]
                        num2 = self.grid.grid[r][c + 2]
                        if op.is_operation() and num2.is_number():
                            print(f"Found horizontal pattern at ({r},{c})")
                            self.evaluate_and_clear(num1, op, num2)

                    # Vertical check: Number-Operation-Number
                    if r + 2 < self.grid.rows:
                        num1 = cell
                        op = self.grid.grid[r + 1][c]
                        num2 = self.grid.grid[r + 2][c]
                        if op.is_operation() and num2.is_number():
                            self.evaluate_and_clear(num1, op, num2)


    def evaluate_and_clear(self, num1, op, num2):
        print("evaluate_and_clear called")
        """Evaluate num1 op num2 and clear any matching blocked-number anywhere on the grid."""
        try:
            expression = f"{num1.number}{op.operation}{num2.number}"
            print(expression)
            result = eval(expression)
            

            # Scan the entire grid for matching blocked-number
            for r in range(self.grid.rows):
                for c in range(self.grid.cols):
                    cell = self.grid.grid[r][c]
                    if cell.is_blockedNum():
                        print(f"Checking blocked cell at ({r},{c}) with value: {cell.value}")
                        if isinstance(cell, BlockedNumberCell) and int(cell.number) == result:
                            print(f"✅ Unlocked blocked number at ({r},{c})!")
                            self.grid.grid[r][c] = EmptyCell(r, c)


        except Exception:
            pass


