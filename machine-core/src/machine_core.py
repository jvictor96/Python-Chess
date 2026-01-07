from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
import threading

class MovementState(Enum):
    YOUR_TURN = "YOUR_TURN"
    THEIR_TURN = "THEIR_TURN"

class DealerState(Enum):
    READING = "IDLE"
    FILTERING = "FILTERING"
    EXECUTING = "EXECUTING"

class Action(Enum):
    PLAY_MOVE = "PLAY_MOVE"
    PRINT_HELP = "PRINT_HELP"
    LIST_GAMES = "LIST_GAMES"
    CHANGE_GAME = "CHANGE_GAME"
    RESIGN_GAME = "RESIGN_GAME"
    START_GAME = "START_GAME"

@dataclass
class Players():
    white: str
    black: str

@dataclass
class MovementMessage():
    game: int
    move: str = ""
    error: str = ""
    player_state: MovementState = MovementState.YOUR_TURN
    next_player_state: MovementState = MovementState.YOUR_TURN

@dataclass
class DealerMessage():
    content: str
    action: Action
    new_game: Players = None
    resign: int = 0
    dealer_state: DealerState = DealerState.READING
    next_dealer_state: DealerState = DealerState.READING

class MovementStateHandler(ABC):

    @abstractmethod
    def handle_movement(self, msg: MovementMessage) -> DealerMessage:
        pass

class DealerStateHandler(ABC):

    @abstractmethod
    def handle_command(self, msg: DealerMessage) -> DealerMessage:
        pass

class DealerStateMachine():
    message: DealerMessage
    handler_map: dict[DealerState, DealerStateHandler]

    def __init__(self, handler_map: dict[DealerState, DealerStateHandler]):
        self.handler_map = handler_map

    async def main_loop(self, dealer_message: DealerMessage):
        self.message = dealer_message
        while True:
            self.message = self.handler_map[self.message.dealer_state](self.message)
            self.message.dealer_state = self.message.next_dealer_state

class MovementStateMachine():
    message: MovementMessage | None
    handler_map: dict[MovementState, MovementStateHandler]

    def __init__(self, handler_map: dict[MovementState, MovementStateHandler]):
        self.handler_map = handler_map

    async def main_loop(self, movement_message: MovementMessage, stop_event: threading.Event):
        self.message = movement_message
        while not stop_event.is_set():
            self.message = self.handler_map[self.message.player_state](self.message)
            self.message.player_state = self.message.next_player_state