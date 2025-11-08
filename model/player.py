from .cell import Cell
class Player(Cell):
    def __init__(self, row, col):
        super().__init__(row, col, "player")

    def display(self):
        return " P "