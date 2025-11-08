from .cell import Cell
class EmptyCell(Cell):
    def __init__(self, row, col):
        super().__init__(row, col, "empty")

    def display(self):
        return "  🟩  "