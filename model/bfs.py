# model/bfs.py
from collections import deque

class BFS:
    def __init__(self, game):
        self.game = game              # original game
        self.queue = deque()          # queue for BFS
        self.visited = set()          # visited states
        self.iteration = 0            # iteration counter

    def enqueue(self, game_instance, path):
        self.queue.append((game_instance, path))

    def dequeue(self):
        return self.queue.popleft()

    def is_empty(self):
        return len(self.queue) == 0

    def state_hash(self, game_instance):
        """
        Return hashable state for O(1) visited check.
        """
        return game_instance.hashable()

    def solve(self, max_iters=1_000_000):
        # Start BFS with the initial cloned game
        self.enqueue(self.game.clone(), [])

        while not self.is_empty():
            self.iteration += 1
            current_game, path = self.dequeue()

            state_id = self.state_hash(current_game)
            if state_id in self.visited:
                continue
            self.visited.add(state_id)

            # Debug: show current iteration and path length every 1000 iterations
            if self.iteration % 1000 == 0:
                print(f"[BFS] Iteration: {self.iteration}, path length: {len(path)}, queue size: {len(self.queue)}, visited: {len(self.visited)}")

            # Check if goal reached
            if current_game.check_win():
                print(f"[BFS] Goal reached in {self.iteration} iterations!")
                return path

            # Explore available moves
            for next_game, direction, affected in current_game.get_available_states():
                sid = self.state_hash(next_game)
                if sid in self.visited:
                    continue
                self.enqueue(next_game, path + [direction])

            if self.iteration > max_iters:
                print("[BFS] Reached iteration limit")
                break

        print("BFS could not reach the goal.")
        return None
