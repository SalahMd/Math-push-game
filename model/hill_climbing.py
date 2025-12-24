class HillClimbingSolver:
    def __init__(self, start_game, heuristic):
        self.start = start_game
        self.heuristic = heuristic

    def solve(self):
        current = self.start
        current_h = self.heuristic.calculate(current)
        path = []

        for s in range(1000):
            if current.check_win():
                print("Goal reached")
                print(f"Path length: {len(path)}")
                return path
            
            neighbors = current.get_available_states()
            if not neighbors:
                break

            best_game = None
            best_move = None
            best_h = current_h

            for next_game, move in neighbors:
                h = self.heuristic.calculate(next_game)
                if h <= best_h:
                    print(best_h,",",h)
                    best_h = h
                    best_game = next_game
                    best_move = move

            if best_game is None:
                break
            current = best_game
            current_h = best_h
            path.append(best_move)

        print("Hill Climbing failed")

        return None
