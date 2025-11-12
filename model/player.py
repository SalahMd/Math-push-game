from .empty_cell import EmptyCell
from .cell import Cell
class Player(Cell):
    def __init__(self, row, col):
        super().__init__(row, col, type="player")
        

    def get_pos(self):
        return (self.row, self.col)
    def is_number(self):
        return False


    def move_player(self, direction, grid, game):
        direction_map = {
            "W": (-1, 0),
            "S": (1, 0),
            "A": (0, -1),
            "D": (0, 1),
        }

        if direction not in direction_map:
            return

        dr, dc = direction_map[direction]
        new_row, new_col = self.row + dr, self.col + dc

        # Ensure move is within bounds
        if not (0 <= new_row < grid.rows and 0 <= new_col < grid.cols):
            return

        next_cell = grid.grid[new_row][new_col]

        # Blocked cells are not walkable
        if next_cell.is_blocked() or next_cell.is_blockedNum():
            return

        # Push logic: if next cell is number or operation
        if next_cell.is_number() or next_cell.is_operation():
            push_row, push_col = new_row + dr, new_col + dc
            if not (0 <= push_row < grid.rows and 0 <= push_col < grid.cols):
                return

            push_target = grid.grid[push_row][push_col]
            if push_target.is_empty():
                # Push forward
                grid.grid[push_row][push_col] = next_cell
                grid.grid[new_row][new_col] = EmptyCell(new_row, new_col)
            else:
                return  # Can't push into blocked cell

        # Move player
        grid.grid[self.row][self.col] = EmptyCell(self.row, self.col)
        self.row, self.col = new_row, new_col
        game.playerPos = (self.row, self.col)
        grid.grid[self.row][self.col] = self  # Replace cell with player
        game.check_if_equal()  # check only after a move


    def display(self):
        return "  🤖  "
