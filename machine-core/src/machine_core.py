from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
import time

class MovementState(Enum):
    BLACK_TURN = "BLACK_TURN"
    WHITE_TURN = "WHITE_TURN"
    WHITE_PLAYED = "WHITE_PLAYED"
    BLACK_PLAYED = "BLACK_PLAYED"
    IDLE = "IDLE"

class DealerState(Enum):
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
    player_state: MovementState

    def play(self, move: str):
        self.move = move
        self.player_state = MovementState.WHITE_PLAYED if self.player_state == MovementState.WHITE_TURN else MovementState.BLACK_PLAYED

    def pass_the_turn(self):
        self.player_state = MovementState.IDLE

    def show(self):
        self.change_turn()
        return self.game

    def change_turn(self):
        self.player_state = MovementState.BLACK_TURN if self.player_state == MovementState.WHITE_PLAYED else MovementState.WHITE_TURN

    def return_turn(self):
        self.player_state = MovementState.WHITE_TURN if self.player_state == MovementState.WHITE_PLAYED else MovementState.BLACK_TURN

@dataclass
class DealerMessage():
    new_game: NewGame
    end_game: int
    next_id: int
    daemon_state: DealerState

    def get_next_id(self):
        self.next_id += 1
        return self.next_id
    
    def consume_new_game(self):
        ans = self.new_game
        self.new_game = None
        return ans
    
    def consume_end_game(self):
        ans = self.end_game
        self.end_game = 0
        return ans

    def free(self):
        self.player_state = DealerState.IDLE

    def mark_as_filled(self):
        self.player_state = DealerState.COMMAND_SENT

    def mark_as_digested(self):
        self.player_state = DealerState.DIGESTED

class MovementStateHandler(ABC):

    @abstractmethod
    def __call__(self, msg: PlayerMessage) -> DealerMessage:
        pass

class DealerStateHandler(ABC):

    @abstractmethod
    def __call__(self, msg: DealerMessage) -> DealerMessage:
        pass

class DealerStateMachine():
    workload: list[DealerMessage]
    message: DealerMessage
    handler_map: dict[DealerState, DealerStateHandler]

    def __init__(self):
        self.workload: list[DealerMessage] = []
        self.handler_map: dict[DealerState, DealerStateHandler] = {}
        self.message: DealerMessage | None = None
    
    def register(self, handler: DealerStateHandler, state: DealerState):
        self.handler_map[state] = handler

    def main_loop(self):
        while True:
            time.sleep(0.05)
            if self.message != None and self.message.daemon_state == DealerState.IDLE:
                while len(self.workload) == 0:
                    time.sleep(0.05)
                self.message = self.handler_map[DealerState.IDLE](self.workload.pop(0))
                while self.message.daemon_state != DealerState.IDLE:
                    self.message = self.handler_map[self.message.daemon_state](self.workload.pop(0))

    def post_task(self, msg: DealerMessage):
        self.workload.append(msg)

class MovementStateMachine():
    workload: list[PlayerMessage]
    message: PlayerMessage | None
    handler_map: dict[MovementState, MovementStateHandler]

    def __init__(self):
        self.workload: list[PlayerMessage] = []
        self.handler_map: dict[MovementState, MovementStateHandler] = {}
        self.message: PlayerMessage | None = None
    
    def register(self, handler: MovementStateHandler, state: MovementState):
        self.handler_map[state] = handler

    def main_loop(self):
        while True:
            time.sleep(0.05)
            if self.message != None and self.message.player_state == MovementState.IDLE:
                while len(self.workload) == 0:
                    time.sleep(0.05)
                self.message = self.handler_map[MovementState.IDLE](self.workload.pop(0))
                while self.message.player_state != MovementState.IDLE:
                    self.message = self.handler_map[self.message.player_state](self.workload.pop(0))

    def post_task(self, msg: PlayerMessage):
        self.workload.append(msg)