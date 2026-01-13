import queue
from piece import Color
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

def test_pastor_check(dealer_machine):
    dispatcher : DealerDispatcher = dealer_machine.handler_map[DealerState.EXECUTING]
    dispatcher.register_opponent_moves(["a7a6", "a6a5", "h7h6", "a8a7"]) # This will actually user the file message crossing under the hood
    keyboard: InMemoryKeyboard = dealer_machine.handler_map[DealerState.READING].keyboard
    keyboard.append_output("sg")
    keyboard.append_output("gisele")
    keyboard.append_output("cg")
    keyboard.append_output("1")
    keyboard.append_output("play move e2e4")
    keyboard.append_output("play move f1c4")
    keyboard.append_output("play move d1f3")
    keyboard.append_output("play move f3f7")
    dealer_machine.main_loop()
    dealer_machine.wait_test_game_end()
    persistence : MemoryGamePersistenceAdapter = dealer_machine.handler_map[DealerState.EXECUTING].persistence
    game = persistence.get_board(1)
    assert game != None
    assert game.winner == "jose"

@pytest.mark.timeout(1)
def test_invalid_movement_repeat_turn(dealer_machine):
    dispatcher : DealerDispatcher = dealer_machine.handler_map[DealerState.EXECUTING]
    dispatcher.register_opponent_moves(["a7a6"]) # This will actually user the file message crossing under the hood
    keyboard: InMemoryKeyboard = dealer_machine.handler_map[DealerState.READING].keyboard
    keyboard.append_output("sg")
    keyboard.append_output("gisele")
    keyboard.append_output("cg")
    keyboard.append_output("1")
    keyboard.append_output("play move e2e5")
    keyboard.append_output("play move f1c4")
    keyboard.append_output("play move a2a3")
    dealer_machine.main_loop()
    dealer_machine.wait_test_game_end()
    persistence : MemoryGamePersistenceAdapter = dealer_machine.handler_map[DealerState.EXECUTING].persistence
    game = persistence.get_board(1)
    assert game != None
    assert not "e5" in game.positions
    assert not "c5" in game.positions

@pytest.mark.timeout(1)
def test_i_move_they_move(dealer_machine):
    dispatcher : DealerDispatcher = dealer_machine.handler_map[DealerState.EXECUTING]
    dispatcher.register_opponent_moves(["e7e5"]) # This will actually user the file message crossing under the hood
    keyboard: InMemoryKeyboard = dealer_machine.handler_map[DealerState.READING].keyboard
    for i in range(5):
        keyboard.append_output("sg")
        keyboard.append_output("gisele")
        keyboard.append_output("cg")
        keyboard.append_output(f"{i+1}")
        keyboard.append_output("play move e2e4")
        keyboard.append_output("play move e4e5")
        dealer_machine.main_loop()
        dealer_machine.wait_test_game_end()
        persistence : MemoryGamePersistenceAdapter = dealer_machine.handler_map[DealerState.EXECUTING].persistence
        game = persistence.get_board(i+1)
        assert game != None
        assert game.positions["e5"].color == Color.BLACK
