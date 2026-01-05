from abc import ABC, abstractmethod
import time
from machine_core import MovementStateHandler, MovementMessage
from player_input import ShellMovementInputUI
from game_viewer import GameViewerPort
from game_persistence import GamePersistencePort


class HumanInterfacePort(MovementStateHandler, ABC):
    @abstractmethod
    def __call__(msg):
        pass
    @abstractmethod
    def play(msg: MovementMessage):
        pass

class TerminalInterfaceAdapter(HumanInterfacePort):
    def __init__(self, user: str, game_viewer: GameViewerPort, persistence: GamePersistencePort, player_input: ShellMovementInputUI):
        self.game_viewer = game_viewer
        self.player_input = player_input
        self.persistence = persistence
        self.user = user

    def __call__(self, msg: MovementMessage):
        if msg.move:
            board = self.persistence.get_board(msg.game)
            board.move(msg.move)
            self.persistence.burn(board)
        self.game_viewer.display(msg.game, self.user)
        msg = self.player_input.play(msg, self.user)
        self.game_viewer.display(msg.game, self.user)
        return msg
    
    def play(self, msg):
        self(msg)
        while True:
            time.sleep(10)