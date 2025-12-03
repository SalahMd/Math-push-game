# player.py
from .empty_cell import EmptyCell
from .cell import Cell

class Player(Cell):
    def __init__(self, row, col):
        super().__init__(row, col, type="player")

    def get_pos(self):
        return (self.row, self.col)

    def set_pos(self, r, c):
        self.row = r
        self.col = c
    def display(self): return "  🤖  "    


    

    def move_player(self, direction, grid, game):
        directions = {
            "W": (-1, 0),
            "S": (1, 0),
            "A": (0, -1),
            "D": (0, 1),
        }

        if direction not in directions:
            return False, []

        dr, dc = directions[direction]
        new_row, new_col = self.row + dr, self.col + dc

        if not grid.check_bounds(new_row, new_col):
            return False, []

        next_cell = grid.grid[new_row][new_col]
        
        if next_cell.is_blocked() or next_cell.is_blockedNum():
            return False, []

        affected = []
        # simple step into empty/goal
        if next_cell.is_empty() or next_cell.is_goal():
            affected.append((self.row, self.col))
            affected.append((new_row, new_col))

            grid.grid[self.row][self.col] = EmptyCell(self.row, self.col)
            self.row, self.col = new_row, new_col
            grid.grid[self.row][self.col] = self
            game.playerPos = (self.row, self.col)
            return True, affected

        # pushing sequence of number/operation cells
        if next_cell.is_number() or next_cell.is_operation():
            pushed_cells = []
            cr, cc = new_row, new_col

            while grid.check_bounds(cr, cc) and (grid.grid[cr][cc].is_number() or grid.grid[cr][cc].is_operation()):
                pushed_cells.append((cr, cc))
                cr += dr
                cc += dc

            # can't push if out of bounds or final cell not empty
            if not grid.check_bounds(cr, cc):
                return False, []
            if not grid.grid[cr][cc].is_empty():
                return False, []

            # perform push (move from end to front)
            for r, c in reversed(pushed_cells):
                grid.grid[r + dr][c + dc] = grid.grid[r][c]
                affected.append((r + dr, c + dc))
                affected.append((r, c))

            first_r, first_c = pushed_cells[0]
            grid.grid[first_r][first_c] = EmptyCell(first_r, first_c)

            # move player
            affected.append((self.row, self.col))
            affected.append((new_row, new_col))

            grid.grid[self.row][self.col] = EmptyCell(self.row, self.col)
            self.row, self.col = new_row, new_col
            grid.grid[self.row][self.col] = self
            game.playerPos = (self.row, self.col)

            # normalize affected (unique)
            affected = list({(r, c) for (r, c) in affected})
            return True, affected

        return False, []
