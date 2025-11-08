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
        return self.playerPos == self.goalPos
    def collect_expression(self, r, c, dr, dc):
            expr = ""
            expect_number = True
            row, col = r, c

            while 0 <= row < self.grid.rows and 0 <= col < self.grid.cols:
                cell = self.grid.grid[row][col]

                if expect_number:
                    if not cell.is_number():
                        break
                    expr += str(cell.number)
                else:
                    if not cell.is_operation():
                        break
                    expr += str(cell.operation)

                # Alternate expectation and move forward
                expect_number = not expect_number
                row += dr
                col += dc

            # Must end with a number to be valid
            if not expect_number:
                return expr
            return None

    def check_equations(self):
        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                cell = self.grid.grid[r][c]
                if cell.is_number():
                    # Horizontal scan
                    if c + 2 < self.grid.cols:
                        expression = self.collect_expression(r, c, dr=0, dc=1)
                        if expression:
                            self.removeBlockedNumber(expression)

                    # Vertical scan
                    if r + 2 < self.grid.rows:
                        expression = self.collect_expression(r, c, dr=1, dc=0)
                        if expression:
                            self.removeBlockedNumber(expression)

    def removeBlockedNumber(self, expression):
        try:
            result = eval(expression)
            for r in range(self.grid.rows):
                for c in range(self.grid.cols):
                    cell = self.grid.grid[r][c]
                    if cell.is_blockedNum() and int(cell.number) == int(result):
                        self.grid.grid[r][c] = EmptyCell(r, c)

        except Exception as e:
            print("Error", e)




