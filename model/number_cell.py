from .cell import Cell
class NumberCell(Cell):
    def __init__(self, row, col, number: int):
        super().__init__(row, col, "number")
        self.number = number

    def display(self):
        emoji_numbers = ["  0️⃣   ","  1️⃣   ","  2️⃣   ","  3️⃣   ","  4️⃣   ","  5️⃣   ","  6️⃣   ","  7️⃣   ","  8️⃣   ","  9️⃣   "]
        return emoji_numbers[int(self.number)] if int(self.number) < 10 else str(self.number)