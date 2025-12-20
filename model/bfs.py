from collections import deque

class BFS:
    def __init__(self, game):
        self.start_game = game
        self.queue = deque()
        self.visited = set()
        self.iteration = 0

    def state_id(self, game):
        return game.hashable()

    def solve(self):
        start_id = self.state_id(self.start_game)
        self.visited.add(start_id)
        self.queue.append((self.start_game, []))
        
        while self.queue:
            self.iteration += 1
            game, path = self.queue.popleft()
            if self.iteration% 2000 == 0:
                print(
                    f"Iteration {self.iteration} ,"
                    f"Visited states: {len(self.visited)}, "
                    f"Path length: {len(path)}, "
                )
            if game.check_win():
                print(
                    f"Congrats, You Won\n"
                    f"path length: {len(path)}"
                )
                return path

            for next_game, move in game.get_available_states():
                id = self.state_id(next_game)
                if id not in self.visited:
                    self.visited.add(id)
                    self.queue.append((next_game, path + [move]))
        print("No solution")
        return None
