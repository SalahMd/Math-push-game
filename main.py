import json
from model.game import Game
from model.json import Json
if __name__ == "__main__":

    file= open("grid2.json")
    data = json.load(file)
    json_data = Json(data)
    
    game = Game(json_data.cells,json_data.rows,json_data.cols)
    game.run()


