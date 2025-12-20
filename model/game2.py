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
                if not moved:
                    print("Can't move")
                    continue
                if affected:
                    self.check_if_equal(affected)

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
    
    def hashable(self):
        rows = []
        for r in range(self.rows):
            row_tuple = tuple(
                (cell.type, getattr(cell, "number", None), getattr(cell, "operation", None))
                for cell in self.grid.grid[r]
            )
            rows.append(row_tuple)
        return (tuple(rows), self.player.get_pos(), self.goalPos)



    def load_state(self, state):
        grid_state, player_pos, goal_pos = state

        for r in range(self.rows):
            for c in range(self.cols):
                cell_type, number, operation = grid_state[r][c]
                if cell_type == "player":
                    self.player.set_pos(r, c)
                    self.grid.grid[r][c] = self.player
                elif cell_type == "number":
                    self.grid.grid[r][c] = NumberCell(r, c, number)
                elif cell_type == "operation":
                    self.grid.grid[r][c] = OperationCell(r, c, operation)
                elif cell_type in ["block","blocked"]:
                    self.grid.grid[r][c] = BlockedCell(r, c)
                elif cell_type in ["door","blocked_number"]:
                    self.grid.grid[r][c] = BlockedNumberCell(r, c, number)
                elif cell_type in ["target","goal"]:
                    self.grid.grid[r][c] = GoalCell(r, c)
                else:
                    self.grid.grid[r][c] = EmptyCell(r, c)

        self.goalPos = goal_pos


    def check_if_equal(self, affected_positions=None):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        if not affected_positions:
            rows_to_check = range(self.rows)
            cols_to_check = range(self.cols)
        else:
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
                    # print('remove door')
                    
                    self.grid.grid[r][c] = EmptyCell(r, c)
                    # for row in self.grid.grid:
                    #     row_display = ""
                    #     for cell in row:
                    #         row_display += f"{cell.display()}  "
                    #     print(row_display)
                    # print()

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
        for move in ["A", "S", "D", "W"]:
            new_game = self.clone()
            old_pos = new_game.player.get_pos()
            moved, affected = new_game.player.move_player(move, new_game.grid, new_game)

            if moved and new_game.player.get_pos() != old_pos:
                if affected:
                    new_game.check_if_equal(affected)
                states.append((new_game, move, affected))
                
        return states

