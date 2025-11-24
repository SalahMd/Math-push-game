from .empty_cell import EmptyCell
from .cell import Cell

class Player(Cell):
    def __init__(self, row, col):
        super().__init__(row, col, type="player")

    def get_pos(self):
        return (self.row, self.col)

    def move_player(self, direction, grid, game):
        directions = {
            "W": (-1, 0),
            "S": (1, 0),
            "A": (0, -1),
            "D": (0, 1),
        }

        if direction not in directions:
            return

        dr, dc = directions[direction]
        new_row, new_col = self.row + dr, self.col + dc

        if not grid.check_bounds(new_row, new_col):
            return

        next_cell = grid.grid[new_row][new_col]

        # Case 1: empty cell → move player
        if next_cell.is_empty():
            grid.grid[self.row][self.col] = EmptyCell(self.row, self.col)
            self.row, self.col = new_row, new_col
            grid.grid[self.row][self.col] = self
            game.playerPos = (self.row, self.col)
            return

        # Case 2: blocked → cannot move
        if next_cell.is_blocked() or next_cell.is_blockedNum():
            return

        # Case 3: number/operation → attempt to push
        if next_cell.is_number() or next_cell.is_operation():
            pushed_cells = []
            cr, cc = new_row, new_col

            while grid.check_bounds(cr, cc) and (grid.grid[cr][cc].is_number() or grid.grid[cr][cc].is_operation()):
                pushed_cells.append((cr, cc))
                cr += dr
                cc += dc

            # Check if we can push
            if not grid.check_bounds(cr, cc):
                return  # cannot push out of bounds
            if not grid.grid[cr][cc].is_empty():
                return  # cannot push into blocked cell

            # Push all cells
            for r, c in reversed(pushed_cells):
                grid.grid[r + dr][c + dc] = grid.grid[r][c]

            # Clear original first pushed cell
            first_r, first_c = pushed_cells[0]
            grid.grid[first_r][first_c] = EmptyCell(first_r, first_c)

            # Move player into the next cell
            grid.grid[self.row][self.col] = EmptyCell(self.row, self.col)
            self.row, self.col = new_row, new_col
            grid.grid[self.row][self.col] = self
            game.playerPos = (self.row, self.col)




    def display(self):
        return "  🤖  "
    
    def serialize(self):
        return super().serialize()

