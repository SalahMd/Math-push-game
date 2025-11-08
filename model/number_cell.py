from .cell import Cell
class NumberCell(Cell):
    def __init__(self, row, col, number: int):
        super().__init__(row, col, "number")
        self.number = number

    def display(self):
        return f" {self.number} "