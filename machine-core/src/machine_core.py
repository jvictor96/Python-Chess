from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
from external_event_source import ExternalEventSource, Message
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
class Players():
    white: str
    black: str

@dataclass
class MovementMessage(Message):
    game: int
    move: str = ""
    error: str = ""
    player_state: MovementState = MovementState.IDLE

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
class DealerMessage(Message):
    new_game: Players = None
    end_game: int = 0
    dealer_state: DealerState = DealerState.IDLE
    
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
    def __call__(self, msg: MovementMessage) -> DealerMessage:
        pass

class DealerStateHandler(ABC):

    @abstractmethod
    def __call__(self, msg: DealerMessage) -> DealerMessage:
        pass

class DealerStateMachine():
    workload: list[DealerMessage]
    message: DealerMessage
    handler_map: dict[DealerState, DealerStateHandler]
    external_event_source: ExternalEventSource[DealerMessage]

    def __init__(self):
        self.workload: list[DealerMessage] = []
        self.handler_map: dict[DealerState, DealerStateHandler] = {}
        self.message = DealerMessage(dealer_state=DealerState.IDLE)
    
    def register(self, handler: DealerStateHandler, state: DealerState):
        self.handler_map[state] = handler

    def set_event_source(self, event_source: ExternalEventSource[DealerMessage]):
        self.external_event_source = event_source

    async def main_loop(self):
        while True:
            time.sleep(0.05)
            if self.message.dealer_state == DealerState.IDLE:
                if self.workload:
                    self.message = self.workload.pop[0]
                    while self.message.dealer_state != DealerState.IDLE:
                        self.message = self.handler_map[self.message.dealer_state](self.workload.pop(0))
                elif messages:=self.external_event_source.poll():
                    self.workload.extend(messages)

class MovementStateMachine():
    workload: list[MovementMessage]
    message: MovementMessage | None
    handler_map: dict[MovementState, MovementStateHandler]
    external_event_source: ExternalEventSource[MovementMessage]

    def __init__(self):
        self.workload: list[MovementMessage] = []
        self.handler_map: dict[MovementState, MovementStateHandler] = {}
        self.message: MovementMessage | None = None
    
    def register(self, handler: MovementStateHandler, state: MovementState):
        self.handler_map[state] = handler

    def set_event_source(self, event_source: ExternalEventSource[MovementMessage]):
        self.external_event_source = event_source

    async def main_loop(self):
        while True:
            time.sleep(0.05)
            if self.message.player_state == MovementState.IDLE:
                if self.workload:
                    self.message = self.workload.pop(0)
                    while self.message.player_state != MovementState.IDLE:
                        self.message = self.handler_map[self.message.player_state](self.workload.pop(0))
                elif messages:=self.external_event_source.poll():
                    self.workload.extend(messages)