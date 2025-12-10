import json
from model.dfs import DFS
from model.bfs import BFS
from model.game import Game
from model.json import Json
from model.astar import AStar
if __name__ == "__main__":

    #grid3 is the small grid 
    #grid2 is the large grid
    file= open("grid2.json")
    data = json.load(file)
    json_data = Json(data)  
    game = Game(json_data.cells,json_data.rows,json_data.cols)

    #To play game manually
    # game.run()


    # bfs_solver = BFS(game)
    # solution_bfs = bfs_solver.solve()
    # print("BFS solution:", solution_bfs)

    # astar_solver = AStar(game)
    # sol = astar_solver.solve()
    # print("path",astar_solver)


    dfs_solver = DFS(game)
    solution_dfs = dfs_solver.solve()
    print("path", solution_dfs)



            
