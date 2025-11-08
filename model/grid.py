from .cell import Cell
from .empty_cell import EmptyCell
class Grid:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.grid = [[EmptyCell(r, c) for c in range(cols)] for r in range(rows)]

    def set_cell(self, cell: Cell):
        self.grid[cell.row][cell.col] = cell
 
    def display(self):
        for r in range(self.rows):
            row_display = ""
            for c in range(self.cols):
                row_display += f"{self.grid[r][c].display()}  "
            print(row_display)
        print()




