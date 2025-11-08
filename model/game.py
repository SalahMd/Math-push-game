from .grid import Grid
from .blocked_number import BlockedNumberCell
from .empty_cell import EmptyCell

class Game:
    def __init__(self, grid: Grid, player, goalPos):
        self.grid = grid
        self.player = player
        self.goalPos = tuple(goalPos)
        self.is_running = True
        self.turn_count = 0
        self.playerPos = player.get_pos()

    def display_grid(self):
        self.grid.display()

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
                self.player.move_player(command, self.grid, self)
                self.turn_count += 1

        print("Game over! Total turns:", self.turn_count)

    def check_win(self):
        print(f"Checking win: playerPos={self.playerPos}, goalPos={self.goalPos}")
        return self.playerPos == self.goalPos

    def check_equations(self):
        """Check for Number-Operation-Number patterns and clear matching blocked-number nearby."""
        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                cell = self.grid.grid[r][c]
                if cell.is_number():
                    # Horizontal
                    if c + 2 < self.grid.cols:
                        num1 = cell
                        op = self.grid.grid[r][c + 1]
                        num2 = self.grid.grid[r][c + 2]
                        if op.is_operation() and num2.is_number():
                            self.evaluate_and_clear(num1, op, num2)
                    # Vertical
                    if r + 2 < self.grid.rows:
                        num1 = cell
                        op = self.grid.grid[r + 1][c]
                        num2 = self.grid.grid[r + 2][c]
                        if op.is_operation() and num2.is_number():
                            self.evaluate_and_clear(num1, op, num2)

    def evaluate_and_clear(self, num1, op, num2):
        try:
            expression = f"{num1.number}{op.operation}{num2.number}"
            result = eval(expression)
            for r in range(self.grid.rows):
                for c in range(self.grid.cols):
                    cell = self.grid.grid[r][c]
                    if cell.is_blockedNum() and int(cell.number) == result:
                        print(f"✅ Unlocked blocked number at ({r},{c})!")
                        self.grid.grid[r][c] = EmptyCell(r, c)
        except Exception:
            pass
