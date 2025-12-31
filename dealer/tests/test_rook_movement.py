import pytest
from board import Board
from piece import Color, Knight, Rook

# game id 1 had one white rook at d4, h1 and c1 free and one white bishop at e4

@pytest.fixture
def board():
        board = Board()
        board.bypass_validation_move("h1d4")  
        board.bypass_validation_move("c1e4")  
        return board

def test_valid_forward_rook_move(board: Board):
    board.move("d4d5")
    assert board.legal == True
    assert isinstance(board.positions.get("d5", None), Rook)

def test_valid_backward_rook_move(board: Board):
    board.move("d4d3")
    assert board.legal == True
    assert isinstance(board.positions.get("d3", None), Rook)

def test_valid_horizontal_rook_move(board: Board):
    board.move("d4c4")
    assert board.legal == True
    assert isinstance(board.positions.get("c4", None), Rook)

def test_invalid_rook_move(board: Board):
    board.move("d4c3")
    assert board.legal == False
    assert isinstance(board.positions.get("d4", None), Rook)

def test_blocked_rook_move(board: Board):
    board.move("d4d2")
    assert board.legal == False
    assert isinstance(board.positions.get("d4", None), Rook)

def test_rook_cant_jump_over_ally(board: Board):
    board.move("d4h4")
    assert board.legal == False
    assert isinstance(board.positions.get("d4", None), Rook)

def test_rook_cant_jump_over_opponent(board: Board):
    board.move("d4d8")
    assert board.legal == False
    assert isinstance(board.positions.get("d4", None), Rook)

def test_rook_takes(board: Board):
    board.move("d4d7")
    assert board.legal == True
    assert board.positions.get("d7", None).color == Color.WHITE