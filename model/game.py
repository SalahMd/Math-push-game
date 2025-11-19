from model.grid import Grid
from .empty_cell import EmptyCell

class Game:

    def __init__(self, cells, rows, cols):
        self.grid = Grid(cells, rows, cols,self)
        self.rows = rows
        self.cols = cols
        self.player
        self.goalPos

    def display_grid(self):
        self.grid.display()

    def run(self):
        is_finished = False
        while not is_finished:
            self.display_grid()
            if self.check_win():
                print("Congrats, you won")
                break

            direction = input("Enter W-A-S-D or Q to quit:  ").upper()
            if direction == "Q":
                is_finished = True
            else:
                self.player.move_player(direction, self.grid, self)
                self.check_if_equal()

    def check_win(self):
        return self.player.get_pos() == self.goalPos


    def collect_expression(self, r, c, dr, dc, is_number):
        if  self.grid.check_bounds(self.rows,self.cols):
            return ""
        cell = self.grid.grid[r][c]
        if is_number and not cell.is_number():
            return ""
        if not is_number and not cell.is_operation():
            return ""
        value = str(cell.number if is_number else cell.operation)
        return value + self.collect_expression(r + dr, c + dc, dr, dc, not is_number)

    def check_if_equal(self):
        directions = [(0, 1), (1, 0)] 
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid.grid[r][c]
                if cell.is_number():
                    for dr, dc in directions:
                        expr = self.collect_expression(r, c, dr, dc,True)
                        if expr and expr[-1].isdigit() and any(op in expr for op in "+-*/"):
                            self.remove_blocked_number(expr)

    

    def remove_blocked_number(self, expr):
        result = eval(expr)
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid.grid[r][c]
                if cell.is_blockedNum() and cell.number == result:
                    self.grid.grid[r][c] = EmptyCell(r, c)
    
