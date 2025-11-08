from abc import ABC, abstractmethod

class Cell(ABC):
    def __init__(self, row, col, type="empty", value=None):
        self.row = row
        self.col = col
        self.type = type
        self.value = value

    # Polymorphic checks
    def is_empty(self):
        return self.type == "empty"

    def is_blocked(self):
        return self.type == "blocked"

    def is_blockedNum(self):
        return self.type == "blocked_number"

    def is_number(self):
        return self.type == "number"

    def is_operation(self):
        return self.type == "operation"

    def is_goal(self):
        return self.type == "goal"

    def is_player(self):
        return self.type == "player"


    @abstractmethod
    def display(self) -> str:
        """Return a string representation of the cell"""
        pass

    def is_walkable(self) -> bool:
        """Whether the player can move onto this cell"""
        return True

    def getPos(self) -> tuple[int, int]:
        """Return the (row, col) position of this cell."""
        return (self.row, self.col)