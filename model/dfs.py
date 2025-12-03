class DFS:
    def __init__(self, game):
        self.game = game
        self.stack = []
        self.visited = set()
        self.iteration = 0

    def push(self, state, path):
        self.stack.append((state, path))

    def pop(self):
        return self.stack.pop()

    def is_empty(self):
        return len(self.stack) == 0

    def hash_states(self, game):
        hashed_grid = tuple(
            tuple(
                (cell.number if cell.is_number() else None,
                cell.operation if cell.is_operation() else None)
                for cell in row
            )
            for row in game.grid.grid
        )
        player_pos = game.player.get_pos()
        return (hashed_grid, player_pos)

    def solve(self):
        self.push(self.game.clone(), [])
        while not self.is_empty():
            self.iteration += 1
            current_game, path = self.pop()

            state_id = self.hash_states(current_game)
            if state_id in self.visited:
                continue
            self.visited.add(state_id)

            current_game.check_if_equal()

            if current_game.check_win():
                return path

            for direction in ["W", "A", "S", "D"]:
                next_game = current_game.clone()
                next_game.player.move_player(direction, next_game.grid, next_game)

                if self.hash_states(next_game) != state_id:
                    self.push(next_game, path + [direction])

            if self.iteration % 100 == 0:
                print(f"visited {self.iteration}")

        print("DFS could not reach the goal.")
        return None
