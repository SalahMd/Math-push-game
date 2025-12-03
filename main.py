import json
from model.dfs import DFS
from model.bfs import BFS


from model.game import Game
from model.json import Json
if __name__ == "__main__":

    file= open("grid2.json")
    data = json.load(file)
    json_data = Json(data)
    
    game = Game(json_data.cells,json_data.rows,json_data.cols)
    
    # game.run()
    # game.display_grid()
    # game.get_available_states()


    # bfs_solver = BFS(game)
    # solution_bfs = bfs_solver.solve()
    # print("BFS solution:", solution_bfs)


    dfs_solver = DFS(game)
    solution_dfs = dfs_solver.solve()
    print("path", solution_dfs)

    # for move in solution_dfs:
    #     game.player.move_player(move, game.grid, game)
    #     game.check_if_equal()
    #     if(game.check_win()):
    #         print(game.player.get_pos())
    #         print(game.goalPos)
    #         print('DFS solved the board')


            
