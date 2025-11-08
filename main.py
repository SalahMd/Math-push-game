from model.grid import Grid
from model.blocked_number import BlockedNumberCell
from model.blocked_cell import BlockedCell
from model.number_cell import NumberCell
from model.operation import OperationCell
from model.goal import GoalCell
from model.player import Player
from model.game import Game
if __name__ == "__main__":

    grid = Grid(10, 10)
    grid.set_cell(BlockedCell(8, 9))
    grid.set_cell(BlockedCell(8, 8))
    grid.set_cell(BlockedCell(8, 7))
    for c in range(10):
        grid.set_cell(BlockedCell(0, c))

    for r in range(10):
        grid.set_cell(BlockedCell(r, 0))  

    for r in range(8):
        grid.set_cell(BlockedCell(r, 9))        
    grid.set_cell(NumberCell(3, 1, 2))
    grid.set_cell(OperationCell(2, 2, '+'))
    grid.set_cell(OperationCell(4, 2, '+'))
    grid.set_cell(NumberCell(3, 3, 3))
    grid.set_cell(NumberCell(5, 5, 3))

    player=   Player(6, 3)
    goalPos = GoalCell(9,9)
    grid.set_cell( player)
    grid.set_cell(goalPos)
    blockedNumber1 = BlockedNumberCell(9,8,8)
    blockedNumber2 = BlockedNumberCell(9,7,6)

    grid.set_cell(blockedNumber1)
    grid.set_cell(blockedNumber2)
    game = Game(grid, player, goalPos.getPos())
    game.run()


