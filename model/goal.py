from .cell import Cell
class GoalCell(Cell):
    def __init__(self, row, col):
        super().__init__(row, col, "goal")

    def display(self):
        return " G "