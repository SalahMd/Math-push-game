from model.blocked_number import BlockedNumberCell
from model.goal import GoalCell
from model.operation import OperationCell
from model.player import Player
from .cell import Cell
from .number_cell import NumberCell
from .blocked_cell import BlockedCell
from .empty_cell import EmptyCell

class Grid:
    def __init__(self, cells, rows, cols, game):
        self.rows = rows
        self.cols = cols
        self.game = game
        self.cells = cells
        self.grid = [[EmptyCell(r, c) for c in range(cols)] for r in range(rows)]
        
        for cell in self.cells:
            cell_type = cell["type"]
            cell_row = cell["row"]
            cell_col = cell["col"]
            if cell_type == "number":
                cell = NumberCell(cell_row, cell_col, cell['number'])
            elif cell_type == "operation":
                cell = OperationCell(cell_row, cell_col, cell['operation'])
            elif cell_type == "block":
                cell = BlockedCell(cell_row, cell_col)
            elif cell_type == "door":
                cell = BlockedNumberCell(cell_row, cell_col, cell['value'])
            elif cell_type == "target":
                cell = GoalCell(cell_row, cell_col)
                game.goalPos = (cell_row, cell_col)
            elif cell_type == "agent":
                cell = Player(cell_row, cell_col)
                game.player = cell
            else:
                cell = EmptyCell(cell_row, cell_col)
            
            self.grid[cell_row][cell_col] = cell

    def display(self):
        for row in self.grid:
            row_display = ""
            for cell in row:
                row_display += f"{cell.display()}  "
            print(row_display)
        print()

    def check_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols    

    def clone(self, new_game):
        new_grid = Grid([], self.rows, self.cols, new_game)
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                cell_type = getattr(cell, "type", None)

                if cell_type == "player":
                    new_cell = Player(r, c)
                    new_game.player = new_cell
                elif cell_type == "number":
                    new_cell = NumberCell(r, c, cell.number)
                elif cell_type == "operation":
                    new_cell = OperationCell(r, c, cell.operation)
                elif cell_type == "block":
                    new_cell = BlockedCell(r, c)
                elif cell_type == "door":
                    new_cell = BlockedNumberCell(r, c, cell.number)
                elif cell_type == "target":
                    new_cell = GoalCell(r, c)
                    new_game.goalPos = (r, c)
                else:  # EmptyCell
                    new_cell = EmptyCell(r, c)

                new_grid.grid[r][c] = new_cell

        return new_grid


