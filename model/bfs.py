import time
from collections import deque

class BFS:
    def __init__(self, game):
        self.start_game = game
        self.queue = deque()
        self.visited = set()
        self.iter_count = 0

    def state_id(self, game):
        return game.hashable()

    def solve(self, log_every=1000):
        start_time = time.time()
        start_id = self.state_id(self.start_game)
        self.visited.add(start_id)
        self.queue.append((self.start_game, []))
        

        while self.queue:
            self.iter_count += 1
            game, path = self.queue.popleft()
            if self.iter_count % log_every == 0:
                now = time.time()
                print(
                    f"Iter {self.iter_count} | "
                    f"Path length: {len(path)} | "
                    f"Total: {now - start_time:.3f}s"
                )
            if game.check_win():
                total = time.time() - start_time
                print(
                    f"🎉 WIN in {self.iter_count} iterations!\n"
                    f"Total time: {total:.2f}s\n"
                    f"Solution path length: {len(path)}"
                )
                return path

            for next_game, move in game.get_available_states():
                nid = self.state_id(next_game)
                if nid not in self.visited:
                    self.visited.add(nid)
                    self.queue.append((next_game, path + [move]))

        # If queue exhausted
        print(
            f"❌ No solution.\n"
            f"Total iterations: {self.iter_count}\n"
            f"Visited: {len(self.visited)}\n"
            f"Total time: {time.time() - start_time:.2f}s"
        )
        return None
