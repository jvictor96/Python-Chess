from abc import ABC, abstractmethod
import time
from machine_core import MovementStateHandler, MovementMessage
from player_input import ShellMovementInputUI
from game_viewer import GameViewerPort


class HumanInterfacePort(MovementStateHandler, ABC):
    @abstractmethod
    def __call__(msg):
        pass
    @abstractmethod
    def play(msg: MovementMessage):
        pass

class TerminalInterfaceAdapter(HumanInterfacePort):
    def __init__(self, user: str, game_viewer: GameViewerPort, player_input: ShellMovementInputUI):
        self.game_viewer = game_viewer
        self.player_input = player_input
        self.user = user

    def __call__(self, msg: MovementMessage):
        self.game_viewer.display(msg.game, self.user)
        msg = self.player_input.play(msg, self.user)
        return msg
    
    def play(self, msg):
        self(msg)
        while True:
            time.sleep(10)