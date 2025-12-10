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
        # 1. Setup initial state
        initial_state = self.game.clone()
        initial_hash = self.state_hash(initial_state)
        
        self.enqueue(initial_state, [])
        self.visited.add(initial_hash) # Mark start as visited immediately

        while not self.is_empty():
            self.iteration += 1
            current_game, path = self.dequeue()

            # Debugging print
            if self.iteration % 1000 == 0:
                print(f"Iteration: {self.iteration}, Path len: {len(path)}, Queue size: {len(self.queue)}")

            # Check win
            if current_game.check_win():
                print(f"[BFS] Goal reached in {self.iteration} iterations!")
                return path

            # 2. Get neighbors
            for next_game, direction in current_game.get_available_states():
                sid = self.state_hash(next_game)
                
                # Only enqueue if NOT visited
                if sid not in self.visited:
                    self.visited.add(sid) 
                    self.enqueue(next_game, path + [direction])

        print("Could not reach the goal.")
        return None