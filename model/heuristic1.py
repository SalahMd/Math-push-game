class Heuristic:
    def evaluate(self, game_instance) -> int:
        base = self._manhattan(game_instance)
        conflict = self._linear_conflict(game_instance)
        blockers = self._blocked_corridor_penalty(game_instance)
        unreachable = self._unreachable_penalty(game_instance)
        return base + conflict + blockers + unreachable

    def _manhattan(self, game_instance) -> int:
        pr, pc = game_instance.player.get_pos()
        gr, gc = game_instance.goalPos
        return abs(pr - gr) + abs(pc - gc)

    def _linear_conflict(self, game_instance) -> int:
        pr, pc = game_instance.player.get_pos()
        gr, gc = game_instance.goalPos
        grid = game_instance.grid.grid

        def blocked_between_row(row, c1, c2):
            lo, hi = sorted((c1, c2))
            for c in range(lo + 1, hi):
                cell = grid[row][c]
                if cell.is_blocked() or cell.is_blockedNum():
                    return True
            return False

        def blocked_between_col(col, r1, r2):
            lo, hi = sorted((r1, r2))
            for r in range(lo + 1, hi):
                cell = grid[r][col]
                if cell.is_blocked() or cell.is_blockedNum():
                    return True
            return False

        if pr == gr and blocked_between_row(pr, pc, gc):
            return 2
        if pc == gc and blocked_between_col(pc, pr, gr):
            return 2
        return 0

    def _blocked_corridor_penalty(self, game_instance) -> int:
        pr, pc = game_instance.player.get_pos()
        gr, gc = game_instance.goalPos
        grid = game_instance.grid.grid

        def is_hard_block(cell):
            return cell.is_blocked() or cell.is_blockedNum()

        def count_blocks(path):
            return sum(1 for r, c in path if is_hard_block(grid[r][c]))

        path_row_first = (
            [(pr, c) for c in range(min(pc, gc), max(pc, gc) + 1) if c != pc]
            + [(r, gc) for r in range(min(pr, gr), max(pr, gr) + 1) if r != pr]
        )
        path_col_first = (
            [(r, pc) for r in range(min(pr, gr), max(pr, gr) + 1) if r != pr]
            + [(gr, c) for c in range(min(pc, gc), max(pc, gc) + 1) if c != pc]
        )

        return min(count_blocks(path_row_first), count_blocks(path_col_first))

    def _unreachable_penalty(self, game_instance) -> int:
        pr, pc = game_instance.player.get_pos()
        gr, gc = game_instance.goalPos
        if (pr, pc) == (gr, gc):
            return 0

        seen = {(pr, pc)}
        stack = [(pr, pc)]
        grid = game_instance.grid

        def can_step(cell):
            return cell.is_empty() or cell.is_goal() or cell.is_player()

        while stack:
            r, c = stack.pop()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if not grid.check_bounds(nr, nc) or (nr, nc) in seen:
                    continue
                cell = grid.grid[nr][nc]
                if not can_step(cell):
                    continue
                if (nr, nc) == (gr, gc):
                    return 0
                seen.add((nr, nc))
                stack.append((nr, nc))
        return 1
