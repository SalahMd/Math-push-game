# game.py
from model.blocked_cell import BlockedCell
from model.blocked_number import BlockedNumberCell
from model.goal import GoalCell
from model.grid import Grid
from model.number_cell import NumberCell
from model.operation import OperationCell
from .empty_cell import EmptyCell

class Game:

    def __init__(self, cells, rows, cols):
        self.rows = rows
        self.cols = cols
        self.player = None
        self.goalPos = None
        self.grid = Grid(cells, rows, cols, self)
        self.playerPos = None

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
                moved, affected = self.player.move_player(direction, self.grid, self)
                if moved:
                    self.check_if_equal(affected)
                else:
                    print("Can't move")


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
    
    def hashable(self):
        important = []
        for r in range(self.rows):
            row_state = []
            for cell in self.grid.grid[r]:
                if cell.type in ("empty", "blocked",'goal','target','door','blocked_number'):  
                    row_state.append(None)
                    continue
                if cell.is_number():
                    row_state.append(("num", cell.number))
                    continue
                if cell.is_operation():
                    row_state.append(("op", cell.operation))
                    continue
                if cell.type == "player":
                    row_state.append(("P", cell.get_pos()))
                    continue
                
                row_state.append(cell.type)

            important.append(tuple(row_state))

        return (tuple(important), self.player.get_pos())






    def check_if_equal(self, affected_positions=None):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        rows_to_check = {r for r, _ in affected_positions}
        cols_to_check = {c for _, c in affected_positions}

        # Check rows
        for r in rows_to_check:
            for c in range(self.cols):
                cell = self.grid.grid[r][c]
                if not cell.is_number():
                    continue
                for dr, dc in directions:
                    expr = self.collect_expression(r, c, dr, dc, True)
                    if expr and expr[-1].isdigit() and any(op in expr for op in "+-*/"):
                        try:
                            value = eval(expr)
                            self.remove_blocked_number_by_value(value)
                        except Exception:
                            continue

        # Check columns
        for c in cols_to_check:
            for r in range(self.rows):
                cell = self.grid.grid[r][c]
                if not cell.is_number():
                    continue
                for dr, dc in directions:
                    expr = self.collect_expression(r, c, dr, dc, True)
                    if expr and expr[-1].isdigit() and any(op in expr for op in "+-*/"):
                        try:
                            value = eval(expr)
                            self.remove_blocked_number_by_value(value)
                        except Exception:
                            continue


    def remove_blocked_number_by_value(self, value):
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid.grid[r][c]
                if cell.is_blockedNum() and cell.number == value:
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
    
    def clone1(self):
        new_game = Game.__new__(Game)   # no init
        new_game.rows = self.rows
        new_game.cols = self.cols
        new_game.goalPos = self.goalPos

        # Clone grid ultra-fast
        new_game.grid = self.grid.fast_clone(new_game)

        # Player already set during cloning
        return new_game





    def get_available_states(self):
        states = []
        for move in ["A", "S", "D", "W"]:
            new_game = self.clone1()
            affected = new_game.player.move_player(move, new_game.grid, new_game)

            if affected is not None :
                new_game.check_if_equal(affected)
                states.append((new_game, move))
                
        return states

