from .cell import Cell
class OperationCell(Cell):
    def __init__(self, row, col, operation: str):
        super().__init__(row, col, "operation")
        self.operation = operation

    def display(self):
        return f" {self.operation} "