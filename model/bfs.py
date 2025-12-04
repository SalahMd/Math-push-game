# model/bfs.py
from collections import deque

class BFS:
    def __init__(self, game):
        self.game = game              
        self.queue = deque()        
        self.visited = set()         
        self.iteration = 0           

    def enqueue(self, game_instance, path):
        self.queue.append((game_instance, path))

    def dequeue(self):
        return self.queue.popleft()

    def is_empty(self):
        return len(self.queue) == 0

    def state_hash(self, game_instance):
        return game_instance.hashable()

    def solve(self):
        self.enqueue(self.game.clone(), [])

        while not self.is_empty():
            self.iteration += 1
            current_game, path = self.dequeue()

            state_id = self.state_hash(current_game)
            if state_id in self.visited:
                continue
            self.visited.add(state_id)

            if self.iteration % 1000 == 0:
                print(f"Iteration: {self.iteration}, path length: {len(path)}")

            if current_game.check_win():
                print(f"[BFS] Goal reached in {self.iteration} iterations!")
                return path

            for next_game, direction, affected in current_game.get_available_states():
                sid = self.state_hash(next_game)
                if sid in self.visited:
                    continue
                self.enqueue(next_game, path + [direction])


        print("could not reach the goal.")
        return None
