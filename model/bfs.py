from collections import deque
import copy

class BFS:
    def __init__(self, game):
        self.game = game
        self.queue = deque()
        self.visited = set()
        self.iteration = 0

    def serialize_state(self, game):
        """Serialize grid and player to track visited states"""
        grid_repr = tuple(
            tuple(
                (
                    cell.number if cell.is_number() else None,
                    cell.operation if cell.is_operation() else None,
                    cell.type  # include doors, empty, etc.
                )
                for cell in row
            )
            for row in game.grid.grid
        )
        player_pos = game.player.get_pos()
        return (grid_repr, player_pos)

    def solve(self):
        # Start BFS with the initial game state
        self.queue.append((self.game.clone(), []))

        while self.queue:
            self.iteration += 1
            current_game, path = self.queue.popleft()

            state_id = self.serialize_state(current_game)
            if state_id in self.visited:
                continue
            self.visited.add(state_id)

            # Evaluate expressions **without changing the grid**
            current_game.check_if_equal()  # ensure this method is non-destructive

            # Check win condition
            if current_game.check_win():
                print(f"BFS solution reached the goal in {len(path)} moves!")
                print("Moves:", path)
                return path

            # Generate next states
            for direction in ["W", "A", "S", "D"]:
                next_game = current_game.clone()
                next_game.player.move_player(direction, next_game.grid, next_game)

                # Only enqueue if the state changed
                next_state_id = self.serialize_state(next_game)
                if next_state_id not in self.visited:
                    self.queue.append((next_game, path + [direction]))

            # Optional: debug output
            if self.iteration % 500 == 0:
                print(f"Iteration {self.iteration}, queue size: {len(self.queue)}")

        print("BFS could not reach the goal.")
        return None
