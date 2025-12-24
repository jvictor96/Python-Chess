from board import Board
from piece import Color, Knight, Pawn

def test_valid_knight_move():
    board = Board.move(0, "b1a3")
    assert board.legal == True
    assert isinstance(board.positions.get("a3", None), Knight)

def test_invalid_knight_move():
    board = Board.move(0, "b1b3")
    assert board.legal == False
    assert isinstance(board.positions.get("b1", None), Knight)

def test_blocked_knight_move():
    board = Board.move(0, "b1d2")
    assert board.legal == False
    assert isinstance(board.positions.get("b1", None), Knight)

def test_knight_takes():
    board = Board.move(0, "b1c3")
    board.keep_moving("d7d5")
    board.keep_moving("c3d5")
    assert board.legal == True
    assert board.positions.get("d5", None).color == Color.WHITE