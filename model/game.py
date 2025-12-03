from model.grid import Grid
from .empty_cell import EmptyCell

class Game:

    def __init__(self, cells, rows, cols):
        self.rows = rows
        self.cols = cols
        self.player = None
        self.goalPos = None
        self.grid = Grid(cells, rows, cols, self)

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

    def safe_eval(self, tokens):
        try:
            expr = ""
            for t in tokens:
                if t in "+-*/" or t.isdigit():
                    expr += t
                else:
                    return None
            return eval(expr)
        except:
            return None
  

    def check_win(self):
        return self.player.get_pos() == self.goalPos

    def collect_expression(self, r, c, dr, dc, is_number):
        if  not self.grid.check_bounds(r,c):
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
                    print('removing door')
                    self.grid.grid[r][c] = EmptyCell(r, c)

    def clone(self):
        new_game = Game([], self.rows, self.cols)
        new_game.goalPos = self.goalPos
        new_game.grid = self.grid.clone(new_game)
        for r in range(self.rows):
            for c in range(self.cols):
                if new_game.grid.grid[r][c].type == "player":
                    new_game.player = new_game.grid.grid[r][c]
        return new_game


    def get_available_states(self):
        states = []
        for move in ["W", "A", "S", "D"]:
            new_game = self.clone()
            old_pos = new_game.player.get_pos()
            new_game.player.move_player(move, new_game.grid, new_game)
            for row in new_game.grid.grid:
                row_display = ""
                for cell in row:
                    row_display += f"{cell.display()}  "
                print(row_display)
            print()

            if new_game.player.get_pos() != old_pos:
                states.append(new_game)
        return states
