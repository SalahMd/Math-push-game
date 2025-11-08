from .cell import Cell
class OperationCell(Cell):
    def __init__(self, row, col, operation: str):
        super().__init__(row, col, "operation")
        self.operation = operation

    def display(self):
        ops_map = {"+":"  ➕  ","-":"  ➖  ","*":"  ✖️  ","/":"  ➗  "}
        return ops_map.get(self.operation, self.operation)