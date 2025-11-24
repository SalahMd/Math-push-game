import json
from model.bfs import BFS
from model.dfs import DFS
from model.game import Game
from model.json import Json
if __name__ == "__main__":

    file= open("grid2.json")
    data = json.load(file)
    json_data = Json(data)
    
    game = Game(json_data.cells,json_data.rows,json_data.cols)

    game.run()
    # bfs_solver = BFS(game)
    # solution_bfs = bfs_solver.solve()
    # print("BFS solution:", solution_bfs)

    # dfs_solver = DFS(game)
    # solution_dfs = dfs_solver.solve()
    # print("DFS solution:", solution_dfs)