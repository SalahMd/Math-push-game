from model.grid import Grid
import json
from model.game import Game
if __name__ == "__main__":

    with open("grid.json", "r") as file:
        data = json.load(file)
    cells = data["cells"]
    
    game = Game(cells,data["rows"],data["cols"])
    game.run()


