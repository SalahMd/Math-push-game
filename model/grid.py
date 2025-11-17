from model.blocked_number import BlockedNumberCell
from model.goal import GoalCell
from model.operation import OperationCell
from model.player import Player
from .cell import Cell
from .number_cell import NumberCell
from .blocked_cell import BlockedCell
from .empty_cell import EmptyCell

class Grid:
    def __init__(self, cells,rows,cols,game):
        self.rows = rows
        self.cols = cols
        self.game = game
        self.grid = []
        for r, row in enumerate(cells):
            row_list = []
            for c, cell_info in enumerate(row):
                cell_type = cell_info["type"]  
                value = cell_info.get("value", None) 
                if cell_type == "number":
                    cell = NumberCell(r, c, value)
                elif cell_type == "operation":
                    cell = OperationCell(r, c, value)
                elif cell_type == "blocked":
                    cell = BlockedCell(r, c)
                elif cell_type == "blocked_number":
                    cell = BlockedNumberCell(r, c, value)
                elif cell_type == "goal":
                    cell = GoalCell(r, c)
                    game.goalPos = (r, c)
                elif cell_type == "player":
                    cell = Player(r, c)
                    game.player = cell
                else:
                    cell = EmptyCell(r, c)
                row_list.append(cell)
            self.grid.append(row_list)
 
    def display(self):
        for r, row in enumerate(self.grid):
            row_display = ""
            for c, cell in enumerate(row):
                row_display += f"{cell.display()}  "
            print(row_display)
        print()

    def check_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols    





