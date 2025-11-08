from .cell import Cell
class BlockedCell(Cell):
    def __init__(self, row, col):
        super().__init__(row, col, "blocked")

    def display(self):
        return "  🧱  "
    
    
    def is_walkable(self):
        return False