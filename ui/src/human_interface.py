from abc import ABC, abstractmethod
from machine_core import MovementStateHandler
from player_input import ShellMovementInputUI
from game_viewer import TextViewerAdapter


class HumanInterfacePort(MovementStateHandler, ABC):
    @abstractmethod
    def __call__(game_id: int, player: str):
        pass

class TerminalInterfaceAdapter(HumanInterfacePort):
    def __init__(self):
        self.game_viewer = TextViewerAdapter()
        self.player_input = ShellMovementInputUI()

    def __call__(self, msg):
        self.game_viewer(msg)
        msg = self.player_input(msg)
        return msg