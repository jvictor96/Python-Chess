from board import Board, BoardIO
from piece import Queen, Color

import pytest

# game id 2 had the white queen at d4, d1, e1 free and the white king at e4, and a black pawn at e5

@pytest.fixture
def board():
        board = BoardIO.get_board(0)
        board.bypass_validation_move("d1d4")  
        board.bypass_validation_move("e1e4")  
        board.bypass_validation_move("e7e5")  
        return board

def test_valid_diagonal_up_queen_move(board: Board):
    board.move("d4b6")
    assert board.legal == True
    assert isinstance(board.positions.get("b6", None), Queen)

def test_valid_diagonal_down_queen_move(board: Board):
    board.move("d4c3")
    assert board.legal == True
    assert isinstance(board.positions.get("c3", None), Queen)

def test_valid_left_queen_move(board: Board):
    board.move("d4c4")
    assert board.legal == True
    assert isinstance(board.positions.get("c4", None), Queen)

def test_valid_down_queen_move(board: Board):
    board.move("d4d3")
    assert board.legal == True
    assert isinstance(board.positions.get("d3", None), Queen)

def test_invalid_queen_move(board: Board):
    board.move("d4a3")
    assert board.legal == False
    assert isinstance(board.positions.get("d4", None), Queen)

def test_blocked_queen_move(board: Board):
    board.move("d4e4")
    assert board.legal == False
    assert isinstance(board.positions.get("d4", None), Queen)

def test_queen_cant_jump_over_ally(board: Board):
    board.move("d4h4")
    assert board.legal == False
    assert isinstance(board.positions.get("d4", None), Queen)

def test_queen_takes(board: Board):
    board.move("d4e5")
    assert board.legal == True
    assert board.positions.get("e5", None).color == Color.WHITE