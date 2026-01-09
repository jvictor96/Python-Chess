import queue
import pytest

from dealer_interface import CommandReader, CommandRouter, DealerDispatcher
from game_viewer import NoViewerAdapter
from keyboard_input import InMemoryKeyboard
from machine_core import DealerMachineMode, DealerState, DealerStateMachine
from memory_persistnce import MemoryGamePersistenceAdapter
from message_crossing import FileMessageCrossingFactory

@pytest.fixture
def dealer_machine():
    user="jose"
    memory_persistence = MemoryGamePersistenceAdapter()
    memory_keyboard = InMemoryKeyboard()
    viewer_adapater = NoViewerAdapter()
    message_crossing_factory = FileMessageCrossingFactory(user)
    movements = queue.Queue()
                    
    return DealerStateMachine({
        DealerState.READING: CommandReader(keyboard=memory_keyboard),
        DealerState.FILTERING: CommandRouter(movements=movements, user=user, game_viewer=viewer_adapater, persistence=memory_persistence),
        DealerState.EXECUTING: DealerDispatcher(movements=movements, user=user, message_crossing_factory=message_crossing_factory, game_viewer=viewer_adapater, keyboard=memory_keyboard, persistence=memory_persistence)
    }, mode=DealerMachineMode.WHILE_THERE_ARE_MESSAGES_ON_KEYBOARD)


def test_get_keyboard(dealer_machine):
    keyboard = dealer_machine.handler_map[DealerState.READING].keyboard
    assert keyboard != None

def test_create_game(dealer_machine):
    persistence : MemoryGamePersistenceAdapter = dealer_machine.handler_map[DealerState.EXECUTING].persistence
    assert persistence.get_board(1) == None
    keyboard: InMemoryKeyboard = dealer_machine.handler_map[DealerState.READING].keyboard
    keyboard.append_output("start game")
    keyboard.append_output("gisele")
    dealer_machine.main_loop()
    game = persistence.get_board(1)
    assert game.white == "jose"
    assert game.black == "gisele"
