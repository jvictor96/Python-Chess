import queue
from piece import Color, King
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
    viewer_adapater = NoViewerAdapter(memory_persistence)
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

@pytest.mark.timeout(5)
def test_magnus_against_gukesh(dealer_machine):
    dispatcher : DealerDispatcher = dealer_machine.handler_map[DealerState.EXECUTING]
    dispatcher.register_opponent_moves(['e7e5', 'b8c6', 'g8f6', 'f8c5', 'e8g8', 'd7d6', 'a7a6', 'h7h6', 'b7b5', 'c5b6', 'c6e7', 'a8b8', 'e7g6', 'c7c5', 'c5d4', 'b5a4', 'c8b7', 'a6a5', 'b7c8', 'b6e3', 'g6f4', 'b8b4', 'g7g6', 'c8a6', 'a6d3', 'h6h5', 'd8a5', 'h5h4', 'f8b8', 'g8g7', 'b4d4', 'h4g3', 'f4h3', 'd3e4', 'd4d1', 'e4d5', 'f6d5', 'd5f4', 'g7f6', 'f6e6', 'e6d5', 'd5d4', 'd4d3', 'f7f6', 'd3e2', 'd1d2', 'e2d2', 'd2e2', 'd6d5', 'b8f8', 'e2e1', 'f4e2', 'e1e2', 'd5d4', 'd4d3', 'e2e3', 'e5e4', 'g6h5', 'e3d2', 'e4e3', 'd2e2']) # This will actually user the file message crossing under the hood
    keyboard: InMemoryKeyboard = dealer_machine.handler_map[DealerState.READING].keyboard
    keyboard.append_output("sg")
    keyboard.append_output("gisele")
    keyboard.append_output("cg")
    keyboard.append_output(f"1")
    keyboard.append_output("play move e2e4")
    keyboard.append_output("play move g1f3")
    keyboard.append_output("play move f1b5")
    keyboard.append_output("play move d2d3")
    keyboard.append_output("play move c2c3")
    keyboard.append_output("play move e1g1")
    keyboard.append_output("play move h2h3")
    keyboard.append_output("play move b5a4")
    keyboard.append_output("play move f1e1")
    keyboard.append_output("play move a4c2")
    keyboard.append_output("play move b1d2")
    keyboard.append_output("play move a2a4")
    keyboard.append_output("play move d3d4")
    keyboard.append_output("play move d2f1")
    keyboard.append_output("play move f1g3")
    keyboard.append_output("play move c3d4")
    keyboard.append_output("play move c2a4")
    keyboard.append_output("play move d4d5")
    keyboard.append_output("play move c1e3")
    keyboard.append_output("play move b2b3")
    keyboard.append_output("play move e1e3")
    keyboard.append_output("play move a4c6")
    keyboard.append_output("play move d1c2")
    keyboard.append_output("play move g1h1")
    keyboard.append_output("play move c2a2")
    keyboard.append_output("play move f3d2")
    keyboard.append_output("play move a2a5")
    keyboard.append_output("play move a1a5")
    keyboard.append_output("play move a5a4")
    keyboard.append_output("play move a4a2")
    keyboard.append_output("play move a2a7")
    keyboard.append_output("play move d2f3")
    keyboard.append_output("play move f2g3")
    keyboard.append_output("play move g2h3")
    keyboard.append_output("play move h1h2")
    keyboard.append_output("play move g3g4")
    keyboard.append_output("play move c6d5")
    keyboard.append_output("play move e3e2")
    keyboard.append_output("play move e2c2")
    keyboard.append_output("play move h3h4")
    keyboard.append_output("play move f3g5")
    keyboard.append_output("play move a7a5")
    keyboard.append_output("play move a5a4")
    keyboard.append_output("play move c2f2")
    keyboard.append_output("play move f2f3")
    keyboard.append_output("play move a4a2")
    keyboard.append_output("play move a2d2")
    keyboard.append_output("play move g5e4")
    keyboard.append_output("play move h2g3")
    keyboard.append_output("play move e4f6")
    keyboard.append_output("play move f3f2")
    keyboard.append_output("play move f6d7")
    keyboard.append_output("play move f2e2")
    keyboard.append_output("play move d7f8")
    keyboard.append_output("play move f8e6")
    keyboard.append_output("play move e6c5")
    keyboard.append_output("play move c5a4")
    keyboard.append_output("play move h4h5")
    keyboard.append_output("play move g4h5")
    keyboard.append_output("play move a4b2")
    keyboard.append_output("play move b2c4")
    keyboard.append_output("play move g3f4")
    dealer_machine.main_loop()
    dealer_machine.wait_test_game_end()
    persistence : MemoryGamePersistenceAdapter = dealer_machine.handler_map[DealerState.EXECUTING].persistence
    game = persistence.get_board(1)
    assert game != None
    assert type(game.positions["f4"]) == King
    assert type(game.positions["e3"]) == King
