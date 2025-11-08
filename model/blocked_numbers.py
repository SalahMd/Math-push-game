from .cell import Cell
from .number_cell import NumberCell
class BlockedNumberCell(NumberCell):
    def __init__(self, row, col, number: int):
        super().__init__(row, col, number)
        self.type = "blocked_number"

    def display(self):
        return f"[{self.number}]"