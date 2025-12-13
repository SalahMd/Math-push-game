# model/dfs.py
import time

class DFS:
    def __init__(self, game):
        self.game = game           
        self.stack = []            
        self.visited = set()        
        self.iteration = 0          

    def push(self, game_instance, path):
        self.stack.append((game_instance, path))

    def pop(self):
        return self.stack.pop()

    def is_empty(self):
        return len(self.stack) == 0

    def state_hash(self, game_instance):
        return game_instance.hashable()

    def solve(self):
        self.push(self.game, [])
        start_time = time.time()
        last_time = start_time

        while not self.is_empty():
            self.iteration += 1
            current_game, path = self.pop()
            state_id = self.state_hash(current_game)
            if state_id in self.visited:
                continue
            self.visited.add(state_id)

            if self.iteration % 1000 == 0:
                now = time.time()
                elapsed = now - last_time
                total_elapsed = now - start_time
                print(f"Iteration: {self.iteration}, Stack size: {len(self.stack)}, "
                      f"Visited states: {len(self.visited)}, "
                      f"Time per 1000 iters: {elapsed:.3f}s, Total time: {total_elapsed:.3f}s")
                last_time = now

            if current_game.check_win():
                total_time = time.time() - start_time
                print(f"Goal reached in {self.iteration} iterations! Total time: {total_time:.3f}s")
                return path

            for next_game, direction in current_game.get_available_states():
                
                sid = self.state_hash(next_game)
                if sid in self.visited:
                    continue
                self.visited.add(state_id)
                self.push(next_game, path + [direction])

        print("could not reach the goal.")
        return None
