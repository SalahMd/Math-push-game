class Heuristic:
    
    def distanceForGoal(self, game):
        pr, pc = game.player.get_pos()
        gr, gc = game.goalPos
        return abs(pr - gr) + abs(pc - gc)

    def lockedDoors(self, game):
        gr, gc = game.goalPos
        count = 0
        for c in range(game.cols):
            cell = game.grid.grid[gr][c]
            if cell.type in ( "blocked_number"):
                count += 1
        for r in range(game.rows):
            if r == gr:
                continue
            cell = game.grid.grid[r][gc]
            if cell.type in ( "blocked_number"):
                count += 1
        return count * 3


    def operationsInCorner(self, game):
        penalty = 0
        corners = [(0,0),(0,game.cols-1),(game.rows-1,0),(game.rows-1,game.cols-1)]
        for r,c in corners:            
            if game.grid.grid[r][c].is_operation():
                penalty += 1
        return penalty*2

    def affectedPotential(self, game):
        pr, pc = game.player.get_pos()
        score = 0
        g = game.grid.grid
        for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
            r, c = pr + dr, pc + dc
            if game.grid.check_bounds(r, c):
                if g[r][c].is_number() or g[r][c].is_operation():
                    score += 5
        return score
    
    def createdEquations(self, game):
        score = 0
        g = game.grid.grid
        for r in range(game.rows):
            for c in range(game.cols):
                if not g[r][c].is_number():
                    continue
                if c + 2 < game.cols and g[r][c+1].is_operation() and g[r][c+2].is_number():
                    score += 1
                if r + 2 < game.rows and g[r+1][c].is_operation() and g[r+2][c].is_number():
                    score += 1
        return score * 3
    
    def calculate(self, game):
        return (
        self.distanceForGoal(game)+
        self.lockedDoors(game)+
        self.operationsInCorner(game)-
        self.createdEquations(game)-
        self.affectedPotential(game)
        )
        


    
    