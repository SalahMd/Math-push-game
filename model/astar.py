import heapq
from itertools import count
from collections import defaultdict

class AStarSolver:
    def __init__(self, start_game, heuristic):
        self.start = start_game
        self.heuristic = heuristic
        self.counter = count()
        self.visited_count = 0

    def solve(self, verbose=True):
        open_heap = []
        visited = set()

        start_h = self.heuristic.evaluate(self.start)
        heapq.heappush(
            open_heap,
            (start_h, 0, next(self.counter), self.start, [])
        )

        visited.add(self.start.hashable())
        self.visited_count = 1

        while open_heap:
            f, g, _, game, path = heapq.heappop(open_heap)

            if game.check_win():
                if verbose:
                    print("Goal reached")
                    print(f"Visited: {self.visited_count}")
                    print(f"Path length: {len(path)}")
                return path

            for next_game, move in game.get_available_states():
                state = next_game.hashable()
                if state in visited:
                    continue

                visited.add(state)
                self.visited_count += 1

                new_g = g + 1
                h = self.heuristic.evaluate(next_game)
                f = new_g + h

                heapq.heappush(
                    open_heap,
                    (f, new_g, next(self.counter), next_game, path + [move])
                )

        return None

