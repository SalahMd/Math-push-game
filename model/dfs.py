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
        while not self.is_empty():
            self.iteration += 1
            current_game, path = self.pop()
            state_id = self.state_hash(current_game)
            if state_id in self.visited:
                continue
            self.visited.add(state_id)

            if self.iteration % 1000 == 0:
                print(f"Iteration: {self.iteration},"
                      f"Visited states: {len(self.visited)}, "
                      )
            if current_game.check_win():
                print(f"You Won\nVisited states: {len(self.visited)}")
                return path

            for next_game, direction in current_game.get_available_states():
                id = self.state_hash(next_game)
                if id in self.visited:
                    continue
                self.visited.add(state_id)
                self.push(next_game, path + [direction])

        print("No solution")
        return None
