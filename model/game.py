from model.grid import Grid
from .empty_cell import EmptyCell

class Game:
    def __init__(self, cells, rows, cols):
        self.grid = Grid(cells, rows, cols, self)

        self.rows = rows
        self.cols = cols
        self.player
        self.goalPos 

    def display_grid(self):
        self.grid.display()
    def run(self):
        is_finished = False
        while not is_finished:
            self.display_grid()
            if self.check_win():
                print("Congrats, you won")
                break

            direction = input("Enter W-A-S-D or Q to quit:  ").upper()
            if direction == "Q":
                is_finished = True
        else:
            self.player.move_player(direction, self.grid, self)
            self.check_if_equal()

    def check_win(self):
        return self.player.get_pos() == self.goalPos

    def clone(self):
        new_game = Game([], self.rows, self.cols)
        new_game.grid = self.grid.clone(new_game)
        return new_game


    def get_available_states(self):
        """Return all possible next states from current game."""
        directions = ["W", "A", "S", "D"]
        states = []

        for move in directions:
            new_game = self.clone()
            old_pos = new_game.player.get_pos()

            # Simulate the move
            new_game.player.move_player(move, new_game.grid, new_game)

            # If player actually moved, add the new state
            if new_game.player.get_pos() != old_pos:
                states.append(new_game)

        return states
