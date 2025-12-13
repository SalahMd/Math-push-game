from heapq import heappush, heappop
import itertools

class AStar:
    def __init__(self, game):
        self.game = game
        self.visited = set()
        self.iteration = 0
        self.counter = itertools.count()  # tie-breaker

    def heuristic(self, game_instance):
        pr, pc = game_instance.player.get_pos()
        gr, gc = game_instance.goalPos
        return abs(pr - gr) + abs(pc - gc)

    def solve(self):
        start_game = self.game.clone()
        start_id = start_game.hashable()
        
        pq = []
        heappush(pq, (self.heuristic(start_game), 0, next(self.counter), start_game, []))
        self.visited.add(start_id)

        while pq:
            f, g, _, current_game, path = heappop(pq)
            self.iteration += 1

            if current_game.check_win():
                print(f"[A*] Goal reached in {self.iteration} iterations!")
                return path

            for next_game, direction in current_game.get_available_states():
                state_id = next_game.hashable()
                if state_id in self.visited:
                    continue

                self.visited.add(state_id)
                g_next = g + 1
                f_next = g_next + self.heuristic(next_game)
                heappush(pq, (f_next, g_next, next(self.counter), next_game, path + [direction]))

            if self.iteration % 3000 == 0:
                print(f"[A*] Iteration: {self.iteration}, visited: {len(self.visited)}, queue size: {len(pq)}")

        print("could not reach the goal.")
        return None
