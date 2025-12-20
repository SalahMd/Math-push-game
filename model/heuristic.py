#Unlocked doors
#Affected
#Equation created
#Operation in corner
#Distance between agent and target
class Heuristic:
    
    def distanceForGoal(self, game) -> int:
        pr, pc = game.player.get_pos()
        gr, gc = game.goalPos
        return abs(pr - gr) + abs(pc - gc)
    
    