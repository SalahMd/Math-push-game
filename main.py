from model.grid import Grid
from model.blocked_numbers import BlockedNumberCell
from model.blocked_cell import BlockedCell
from model.number_cell import NumberCell
from model.operation import OperationCell
from model.goal import GoalCell
from model.player import Player
from model.game import Game
if __name__ == "__main__":

    grid = Grid(10, 10)
    #grid.set_cell(0, 0, BlockedCell(0, 0))
    grid.set_cell(NumberCell(2, 1, 5))
    grid.set_cell(OperationCell(1, 2, '+'))
    grid.set_cell(NumberCell(3, 3, 3))
    grid.set_cell(NumberCell(5, 5, 3))
    player=   Player(0, 3)
    goalPos = GoalCell(9,9)
    grid.set_cell( player)
    grid.set_cell(goalPos)
    blockedNumber1 = BlockedNumberCell(9,8,8)
    blockedNumber2 = BlockedNumberCell(8,9,6)

    grid.set_cell(blockedNumber1)
    grid.set_cell(blockedNumber2)
    #grid.display()
    game = Game(grid, player.getPos(), goalPos.getPos())
    game.run()


