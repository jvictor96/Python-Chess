import time
import os, json
from ports import GamePersistencePort, GameViewerPort
from board import Board

class ChessDaemon:
    def __init__(self, game_persistence_adapter: GamePersistencePort, game_viewer_adapter: GameViewerPort):
        self.game_persistence_adapter = game_persistence_adapter
        self.game_viewer_adapter = game_viewer_adapter
        self.path = f"{os.environ['HOME']}/python_chess"

    def main_loop(self):
        try:
            os.mkdir(self.path)
        except Exception as e:
            pass
        while True:
            time.sleep(0.1)
            try:
                with open(f"{self.path}/daemon.json", "r+") as daemon:
                    control_fields = json.load(daemon)
                    for game in control_fields["games"]:
                        self.update_game(game)
                    if control_fields["new_game"]["white"] != "":
                        white = control_fields["new_game"]["white"]
                        black = control_fields["new_game"]["black"]
                        control_fields["new_game"] = { "white": "", "black": "" }
                        control_fields["games"].append(control_fields["next_id"])
                        board = Board(white=white, black=black, game_id=control_fields["next_id"])
                        self.game_persistence_adapter.burn(board)
                        self.reprint_input(
                            game_id=control_fields["next_id"])
                        self.game_viewer_adapter.display(board)
                        control_fields["next_id"] += 1
                    if control_fields["end_game"] > 0:
                        control_fields["games"].remove(control_fields["end_game"])
                        control_fields["end_game"] = 0
                    daemon.seek(0)
                    daemon.truncate()
                    json.dump(control_fields, daemon)
            except FileNotFoundError as e:
                with open(f"{self.path}/daemon.json", "x+") as daemon:
                    if len(daemon.readlines()) == 0:
                        control_fields = {
                            "games": [],
                            "new_game": { "white": "", "black": "" },
                            "next_id": 1,
                            "end_game": 0
                        }
                        daemon.seek(0)
                        daemon.truncate()
                        json.dump(control_fields, daemon)

    def update_game(self, game: int):
        with open(f"{self.path}/game_{game}_input.json", "r+") as game_file:
            game_control_fields = json.load(game_file)
            if game_control_fields["move"] != "":
                board = self.game_persistence_adapter.get_board(game)
                board.move(game_control_fields["move"])
                self.game_persistence_adapter.burn(board)
                self.reprint_input(game, "" if board.legal else "Illegal move")
                self.game_viewer_adapter.display(board)

    def reprint_input(self, game_id: int, error: str = ""):
        game_control_fields = json.loads("{}")
        game_control_fields["move"] = ""
        game_control_fields["error"] = error
        with open(f"{self.path}/game_{game_id}_input.json", "w") as input_file:
            json.dump(game_control_fields, input_file)