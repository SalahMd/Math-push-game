from model.grid import Grid
from model.player import Player
from .empty_cell import EmptyCell

class Game:

    def __init__(self, cells, rows, cols):
        self.grid = Grid(cells, rows, cols)
        self.rows = rows
        self.cols = cols
        self.player = self.find_player()
        self.goalPos = self.find_goal_pos()
        self.is_running = True

    def find_player(self):
        for r, row in enumerate(self.grid.grid):
            for c, cell in enumerate(row):
                if cell.is_player():
                    return Player(r, c)

    def find_goal_pos(self):
        for r, row in enumerate(self.grid.grid):
            for c, cell in enumerate(row):
                if cell.is_goal():
                    return (r, c)

    def display_grid(self):
        self.grid.display()

    def run(self):
        while self.is_running:
            self.display_grid()
            if self.check_win():
                print("Congrats, you won!")
                break

            direction = input("Enter W-A-S-D or Q to quit: ").upper()
            if direction == "Q":
                self.is_running = False
            else:
                self.player.move_player(direction, self.grid, self)
                self.check_if_equal()

    def check_win(self):
        return self.player.getPos() == self.goalPos


    def collect_expression(self, r, c, dr, dc, expect_number=True):
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return ""
        cell = self.grid.grid[r][c]
        if expect_number and not cell.is_number():
            return ""
        if not expect_number and not cell.is_operation():
            return ""

        value = str(cell.number if expect_number else cell.operation)
        return value + self.collect_expression(r + dr, c + dc, dr, dc, not expect_number)

    def check_if_equal(self):
        directions = [(0, 1), (1, 0)] 
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid.grid[r][c]
                if cell.is_number():
                    for dr, dc in directions:
                        print (dr,dc)
                        expr = self.collect_expression(r, c, dr, dc, expect_number=True)
                        if expr and expr[-1].isdigit() and any(op in expr for op in "+-*/"):
                            self.remove_blocked_number(expr)


    def remove_blocked_number(self, expression):
        try:
            result = eval(expression)
            for r in range(self.rows):
                for c in range(self.cols):
                    cell = self.grid.grid[r][c]
                    if cell.is_blockedNum() and int(cell.number) == int(result):
                        self.grid.grid[r][c] = EmptyCell(r, c)
                        print(f"Removed blocked number {result} at ({r},{c})")
        except Exception as e:
            print("Error evaluating expression:", expression, e)
