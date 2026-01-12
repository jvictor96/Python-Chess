import asyncio
from dataclasses import asdict, dataclass
from enum import Enum
from abc import ABC, abstractmethod
import json
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

    def as_json_string(self):
        data = asdict(self)
        data.pop("player_state", None)
        data.pop("next_player_state", None)
        return json.dumps(data)

@dataclass
class DealerMessage():
    content: str | None = None
    action: Action | None = None
    new_game: Players = None
    resign: int = 0
    dealer_state: DealerState = DealerState.READING
    next_dealer_state: DealerState = DealerState.READING

class MovementStateHandler(ABC):

    @abstractmethod
    def handle_movement(self, msg: MovementMessage) -> MovementMessage:
        pass

class DealerStateHandler(ABC):

    @abstractmethod
    def handle_command(self, msg: DealerMessage) -> DealerMessage:
        pass

class DealerMachineMode(Enum):
    FOR_EVER = "FOR_EVER"
    WHILE_THERE_ARE_MESSAGES_ON_KEYBOARD = "WHILE_THERE_ARE_MESSAGES_ON_KEYBOARD"

class DealerStateMachine():
    message: DealerMessage
    handler_map: dict[DealerState, DealerStateHandler]

    def __init__(self, handler_map: dict[DealerState, DealerStateHandler], mode = DealerMachineMode.FOR_EVER):
        self.handler_map = handler_map
        self.mode = mode

    def game_still_playing(self):
        mc = self.handler_map[DealerState.EXECUTING].message_crossing
        return (mc and mc.sending_batch)

    def isnt_done(self):
        return any([
            self.mode == DealerMachineMode.FOR_EVER,
            self.message.dealer_state != DealerState.READING,
            self.handler_map[DealerState.READING].keyboard.outputs
        ])

    def main_loop(self):
        self.message = DealerMessage(dealer_state=DealerState.READING)
        while self.isnt_done():
            self.message = self.handler_map[self.message.dealer_state].handle_command(self.message)
            self.message.dealer_state = self.message.next_dealer_state


class MovementStateMachine():
    message: MovementMessage | None
    handler_map: dict[MovementState, MovementStateHandler]

    def __init__(self, handler_map: dict[MovementState, MovementStateHandler]):
        self.handler_map = handler_map

    async def main_loop(self, movement_message: MovementMessage, stop_event: threading.Event):
        self.message = movement_message
        while not stop_event.is_set():
            await asyncio.sleep(.2)
            print(f"game state {self.message.player_state}", flush=True)
            self.message = self.handler_map[self.message.player_state].handle_movement(self.message)
            self.message.player_state = self.message.next_player_state