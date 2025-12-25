import pytest
from board import Board, BoardIO
from piece import King, Color

# game id 2 had the white queen at d4, d1, e1 free and the white king at e4, and a black pawn at e5

@pytest.fixture
def board():
        board = BoardIO.get_board(0)
        board.bypass_validation_move("d1d4")  
        board.bypass_validation_move("e1e4")  
        board.bypass_validation_move("e7e5")  
        return board

def test_valid_diagonal_up_king_move(board: Board):
    board.move("e4d5")
    assert board.legal == True
    assert isinstance(board.positions.get("d5", None), King)

def test_valid_diagonal_down_king_move(board: Board):
    board.move("e4d3")
    assert board.legal == True
    assert isinstance(board.positions.get("d3", None), King)

def test_valid_right_king_move(board: Board):
    board.move("e4f4")
    assert board.legal == True
    assert isinstance(board.positions.get("f4", None), King)

def test_valid_down_king_move(board: Board):
    board.move("e4e3")
    assert board.legal == True
    assert isinstance(board.positions.get("e3", None), King)

def test_invalid_king_move(board: Board):
    board.move("e4e6")
    assert board.legal == False
    assert isinstance(board.positions.get("e4", None), King)

def test_blocked_king_move(board: Board):
    board.move("e4d4")
    assert board.legal == False
    assert isinstance(board.positions.get("e4", None), King)

def test_king_takes(board: Board):
    board.move("e4e5")
    assert board.legal == True
    assert board.positions.get("e5", None).color == Color.WHITE