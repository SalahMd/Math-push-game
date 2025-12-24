import heapq

class AStarSolver:
    def __init__(self, start_game, heuristic):
        self.start = start_game
        self.heuristic = heuristic
        self.counter = 0

    def solve(self, ):
        heap = []
        visited = set()

        started_h = self.heuristic.calculate(self.start)
        self.counter +=1
        heapq.heappush(
            heap,
            (started_h, 0, self.counter, self.start, [])
        )

        visited.add(self.start.hashable())
        while heap:
            f, g, _, game, path = heapq.heappop(heap)
            if game.check_win():
                print("Goal reached")
                print(f"Visited: {len(visited)}")
                print(f"Path length: {len(path)}")
                return path

            for next_game, move in game.get_available_states():
                state = next_game.hashable()
                if state in visited:
                    continue
                visited.add(state)
                new_g = g + 1
                h = self.heuristic.calculate(next_game)
                f = new_g + h
                self.counter +=1
                heapq.heappush(
                    heap,
                    (f, new_g, self.counter, next_game, path + [move])
                )

        return None

