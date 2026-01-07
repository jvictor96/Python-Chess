import os, json
from dataclasses import asdict
from ports import GamePersistencePort, GameViewerPort
from machine_core import MovementMessage, MovementState, MovementStateHandler
from typing import Iterable

class FileOpponentInterface(MovementStateHandler):
    def __init__(self, user: str, persistence: GamePersistencePort, game_viewer: GameViewerPort):
        self.path = f"{os.environ['HOME']}/python_chess"
        self.persistence = persistence
        self.game_viewer = game_viewer
        self.user = user
        if f"{user}.fifo" not in os.listdir(self.path):
            os.mkfifo(f"{self.path}/{self.user}.fifo")
    
    def handle_movement(self, msg) -> MovementMessage:          # I know this implementation blocks the flow
        board = self.persistence.get_board(msg.game)
        with open(f"{self.path}/{self.user}.fifo", "r") as ff:
            content = json.load(ff)
            board.move(content["move"])
        self.game_viewer.display(msg.game, self.user)
        self.persistence.burn(board)
        msg.next_player_state = MovementState.YOUR_TURN
        return msg
    
    def send_message(self, message: MovementMessage) -> None:          # I know this implementation blocks the flow
        board = self.persistence.get_board(message.game)
        other_user = [player for player in [board.black, board.white] if player != self.user][0]
        if not (f"{other_user}.fifo" in os.listdir(self.path)):
            os.mkfifo(f"{self.path}/{other_user}.fifo")
        with open(f"{self.path}/{other_user}.fifo", "w") as ff:
            data = asdict(message)
            data.pop("player_state", None)
            json.dump(data, ff)