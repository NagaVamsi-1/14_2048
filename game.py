from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.best_score = 0
        self.history = []
        self.won = False
        self.game_over = False
        self.last_action = None

    def _update_game_state(self):
        self.won = any(2048 in row for row in self.board.grid)
        self.game_over = self.won or not self.board.can_move()

    def display(self):
        print("\n" + "+------+------+------+------+")
        for row in self.board.grid:
            print("|" + "|".join(f"{x:^6}" if x else f"{' ':^6}" for x in row) + "|")
            print("+------+------+------+------+")
        print("Score:", self.board.score, " Best:", self.best_score)

    def move(self, key):
        moves = {"a": self.board.move_left, "d": self.board.move_right,
                 "w": self.board.move_up, "s": self.board.move_down}
        if key not in moves:
            return False

        old_grid = [row[:] for row in self.board.grid]
        old_score = self.board.score
        old_tiles = sum(value != 0 for row in old_grid for value in row)
        changed = moves[key]()
        if changed:
            # Determine feedback from the move result before creating the new tile.
            new_tiles = sum(value != 0 for row in self.board.grid for value in row)
            merged = new_tiles < old_tiles

            # Keep only the previous state of the latest successful move.
            self.history = [(old_grid, old_score)]
            self.last_action = f"Moved {key.upper()}"
            if merged:
                self.last_action += " — merged"

            # A new tile is created only after a successful move.
            self.board.add_random_tile()
            self._update_game_state()
        return changed

    def undo(self):
        if not self.history:
            return False

        old_grid, old_score = self.history.pop()
        self.board.grid = [row[:] for row in old_grid]
        self.board.score = old_score
        self._update_game_state()
        return True

    def run(self):
        print("2048 — W/A/S/D to move, U to undo, Q to quit.")
        while True:
            self.display()
            self._update_game_state()
            if self.won:
                print("You reached 2048!")
                return
            if self.game_over:
                print("No legal moves remain.")
                return
            key = input("> ").strip().lower()
            if key == "q":
                return
            if key == "u":
                if self.undo():
                    print("Move undone.")
                else:
                    print("Nothing to undo.")
                continue
            if key not in "wasd":
                print("Use W/A/S/D.")
                continue
            if self.move(key):
                self.best_score = max(self.best_score, self.board.score)
                print(self.last_action + ".")
