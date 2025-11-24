from collections import deque

class BFS:
    def __init__(self, game):
        self.game = game
        self.queue = deque()
        self.visited = set()

    def put(self, state, path):
        """Add state to the queue."""
        self.queue.append((state, path))

    def pop(self):
        """Pop from the queue (FIFO)."""
        return self.queue.popleft()

    def remove(self, state_id):
        """Optional: remove a state from visited if needed."""
        self.visited.discard(state_id)

    def is_empty(self):
        return len(self.queue) == 0

    def solve(self):
        self.put(self.game, [])
        while not self.is_empty():
            current_game, path = self.pop()

            state_id = tuple(
            tuple(tuple(sorted(cell.serialize().items())) for cell in row)
            for row in current_game.grid.grid
            )


            if state_id in self.visited:
                continue
            self.visited.add(state_id)

            if current_game.check_win():
                return path

            for next_game in current_game.get_available_states():
                move_taken = None
                for direction in ["W", "A", "S", "D"]:
                    temp_game = current_game.clone()
                    temp_game.player.move_player(direction, temp_game.grid, temp_game)
                    if tuple(tuple(cell.serialize() for cell in row) for row in temp_game.grid.grid) == \
                       tuple(tuple(cell.serialize() for cell in row) for row in next_game.grid.grid):
                        move_taken = direction
                        break
                self.put(next_game, path + [move_taken])
        return None
