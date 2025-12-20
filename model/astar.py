from __future__ import annotations

import itertools
import time
from dataclasses import dataclass, field
from heapq import heappop, heappush
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass(order=True)
class PrioritizedState:
    f: int
    h: int
    order: int
    state_id: Tuple = field(compare=False)
    g: int = field(compare=False)
    game: "Game" = field(compare=False)


class AStar:
    def __init__(self, game):
        self.game = game
        self.iteration = 0
    def heuristic(self, game_instance) -> int:
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
            count = 0
            for r, c in path:
                if is_hard_block(grid[r][c]):
                    count += 1
            return count

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

        def can_step(cell) -> bool:
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

    def _reconstruct_path(self, goal_id, parents: Dict) -> List[str]:
        moves: List[str] = []
        cursor = goal_id
        while parents[cursor][0] is not None:
            cursor, move = parents[cursor]
            moves.append(move)
        return list(reversed(moves))

    def _push_neighbors(
        self,
        current: PrioritizedState,
        parents: Dict,
        g_score: Dict,
        frontier: List[PrioritizedState],
        counter: Iterable[int],
    ) -> None:
        for next_game, move in current.game.get_available_states():
            nid = next_game.hashable()
            tentative_g = current.g + 1
            if tentative_g >= g_score.get(nid, float("inf")):
                continue

            g_score[nid] = tentative_g
            parents[nid] = (current.state_id, move)
            h = self.heuristic(next_game)
            heappush(
                frontier,
                PrioritizedState(
                    tentative_g + h,
                    h,
                    next(counter),
                    nid,
                    tentative_g,
                    next_game,
                ),
            )

    def solve(self, log_every: int = 2000) -> Optional[List[str]]:
        self.iteration = 0
        start_time = time.time()
        counter = itertools.count()

        start_game = self.game.clone1()
        start_id = start_game.hashable()
        start_h = self.heuristic(start_game)

        parents = {start_id: (None, None)} 
        g_score = {start_id: 0} 
        frontier: List[PrioritizedState] = [
            PrioritizedState(start_h, start_h, next(counter), start_id, 0, start_game)
        ]

        while frontier:
            current = heappop(frontier)
            self.iteration += 1

            if g_score.get(current.state_id, float("inf")) != current.g:
                continue

            if current.game.check_win():
                elapsed = time.time() - start_time
                path = self._reconstruct_path(current.state_id, parents)
                print(
                    f"[A*] Goal reached in {self.iteration} iterations | "
                    f"path length: {len(path)} | time: {elapsed:.2f}s"
                )
                return path

            if log_every and self.iteration % log_every == 0:
                elapsed = time.time() - start_time
                print(
                    f"[A*] Iter {self.iteration} | "
                    f"Frontier: {len(frontier)} | "
                    f"Seen: {len(g_score)} | "
                    f"Current f: {current.f} | "
                    f"Elapsed: {elapsed:.2f}s"
                )

            self._push_neighbors(current, parents, g_score, frontier, counter)

        print(
            f"[A*] No solution after {self.iteration} iterations; explored {len(g_score)} states."
        )
        return None
