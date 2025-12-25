from board import Board
from piece import Bishop, Color

import pytest

# game id 1 had one white rook at d4, h1 and c1 free and one white bishop at e4

@pytest.fixture
def board():
        board = Board.get_board(0)
        board.bypass_validation_move("h1d4")  
        board.bypass_validation_move("c1e4")  
        return board

def test_valid_forward_left_biship_move(board: Board):
    board.keep_moving("e4d5")
    assert board.legal == True
    assert isinstance(board.positions.get("d5", None), Bishop)

def test_valid_backward_left_bishop_move(board: Board):
    board.keep_moving("e4d3")
    assert board.legal == True
    assert isinstance(board.positions.get("d3", None), Bishop)

def test_valid_backward_right_bishop_move(board: Board):
    board.keep_moving("e4f3")
    assert board.legal == True
    assert isinstance(board.positions.get("f3", None), Bishop)

def test_invalid_bishop_move(board: Board):
    board.keep_moving("e4e5")
    assert board.legal == False
    assert isinstance(board.positions.get("e4", None), Bishop)

def test_blocked_bishop_move(board: Board):
    board.keep_moving("e4c2")
    assert board.legal == False
    assert isinstance(board.positions.get("e4", None), Bishop)

def test_bishop_cant_jump_over_ally(board: Board):
    board.keep_moving("e4h1")
    assert board.legal == False
    assert isinstance(board.positions.get("e4", None), Bishop)

def test_bishop_cant_jump_over_opponent(board: Board):
    board.keep_moving("e4a8")
    assert board.legal == False
    assert isinstance(board.positions.get("d4", None), Bishop)

def test_bishop_takes(board: Board):
    board.keep_moving("e4b7")
    assert board.legal == True
    assert board.positions.get("d7", None).color == Color.WHITE