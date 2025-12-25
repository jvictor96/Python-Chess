from board import Board
from piece import King, Color

# game id 2 has one white queen at d4, d1, e1 free and one white king at e4 and a black pawn at e5

def test_valid_diagonal_up_king_move():
    board = Board.move(2, "e4d5")
    assert board.legal == True
    assert isinstance(board.positions.get("d5", None), King)

def test_valid_diagonal_down_king_move():
    board = Board.move(2, "e4d3")
    assert board.legal == True
    assert isinstance(board.positions.get("d3", None), King)

def test_valid_right_king_move():
    board = Board.move(2, "e4f4")
    assert board.legal == True
    assert isinstance(board.positions.get("f4", None), King)

def test_valid_down_king_move():
    board = Board.move(2, "e4e3")
    assert board.legal == True
    assert isinstance(board.positions.get("e3", None), King)

def test_invalid_king_move():
    board = Board.move(2, "e4e6")
    assert board.legal == False
    assert isinstance(board.positions.get("e4", None), King)

def test_blocked_king_move():
    board = Board.move(2, "e4d4")
    assert board.legal == False
    assert isinstance(board.positions.get("e4", None), King)

def test_king_takes():
    board = Board.move(2, "e4e5")
    assert board.legal == True
    assert board.positions.get("e5", None).color == Color.WHITE