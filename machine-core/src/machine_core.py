from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
import time

class PlayerState(Enum):
    BLACK_TURN = "BLACK_TURN"
    WHITE_TURN = "WHITE_TURN"
    PLAYED = "PLAYED"
    BOARD_UPDATED = "BOARD_UPDATED"
    SHOWN = "SHOWN"

class DaemonState(Enum):
    IDLE = "IDLE"
    DIGESTED = "DIGESTED"
    COMMAND_SENT = "COMMAND_SENT"

@dataclass
class NewGame():
    white: str
    black: str

@dataclass
class PlayerMessage():
    move: str
    game: int
    error: str
    player_state: PlayerState

@dataclass
class DaemonMessage():
    new_game: NewGame
    end_game: int
    next_id: int
    daemon_state: DaemonState

class PlayerStateHandler(ABC):

    @abstractmethod
    def __call__(self, msg: PlayerMessage) -> DaemonMessage:
        pass

class DaemonStateHandler(ABC):

    @abstractmethod
    def __call__(self, msg: DaemonMessage) -> DaemonMessage:
        pass

class DaemonHookController(ABC):
    @abstractmethod
    def register(self, handler: DaemonStateHandler, state: DaemonState):
        pass

    @abstractmethod
    def main_loop(self):
        pass

    @abstractmethod
    def post_task(self):
        pass

class PlayerHookController(ABC):
    @abstractmethod
    def register(self, handler: PlayerStateHandler, state: PlayerState):
        pass

    @abstractmethod
    def post_task(self):
        pass

    @abstractmethod
    def main_loop(self):
        pass

class DaemonStateMachine(DaemonHookController):
    workload: list[DaemonMessage]
    message: DaemonMessage
    handler_map: dict[DaemonState, DaemonStateHandler]

    def __init__(self):
        self.workload: list[DaemonMessage] = []
        self.handler_map: dict[DaemonState, DaemonStateHandler] = {}
        self.message: DaemonMessage | None = None
    
    def register(self, handler: DaemonStateHandler, state: DaemonState):
        self.handler_map[state] = handler

    def main_loop(self):
        while True:
            time.sleep(0.05)
            if self.message != None and self.message.daemon_state == DaemonState.IDLE:
                while len(self.workload) == 0:
                    time.sleep(0.05)
                self.message = self.handler_map[DaemonState.IDLE](self.workload.pop(0))
                while self.message.daemon_state != DaemonState.IDLE:
                    self.message = self.handler_map[self.message.daemon_state](self.workload.pop(0))

    def post_task(self, msg: DaemonMessage):
        self.workload.append(msg)

class PlayerStateMachine(PlayerHookController):
    workload: list[PlayerMessage]
    message: PlayerMessage | None
    handler_map: dict[PlayerState, PlayerStateHandler]

    def __init__(self):
        self.workload: list[PlayerMessage] = []
        self.handler_map: dict[PlayerState, PlayerStateHandler] = {}
        self.message: PlayerMessage | None = None
    
    def register(self, handler: PlayerStateHandler, state: PlayerState):
        self.handler_map[state] = handler

    def main_loop(self):
        while True:
            time.sleep(0.05)
            if self.message != None and self.message.player_state == PlayerState.IDLE:
                while len(self.workload) == 0:
                    time.sleep(0.05)
                self.message = self.handler_map[PlayerState.IDLE](self.workload.pop(0))
                while self.message.player_state != PlayerState.IDLE:
                    self.message = self.handler_map[self.message.player_state](self.workload.pop(0))

    def post_task(self, msg: PlayerMessage):
        self.workload.append(msg)