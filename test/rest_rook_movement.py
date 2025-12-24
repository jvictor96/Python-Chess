from board import Board
from piece import Color, Knight, Rook

# game id 1 has one white root at d4 and one white bishop at e4

def test_valid_forward_rook_move():
    board = Board.move(0, "d4d5")
    assert board.legal == True
    assert isinstance(board.positions.get("d5", None), Rook)

def test_valid_backward_rook_move():
    board = Board.move(0, "d4d3")
    assert board.legal == True
    assert isinstance(board.positions.get("d3", None), Rook)

def test_valid_horizontal_rook_move():
    board = Board.move(0, "d4c4")
    assert board.legal == True
    assert isinstance(board.positions.get("c4", None), Rook)

def test_invalid_rook_move():
    board = Board.move(0, "d4c3")
    assert board.legal == False
    assert isinstance(board.positions.get("d4", None), Rook)

def test_blocked_rook_move():
    board = Board.move(0, "d4d2")
    assert board.legal == False
    assert isinstance(board.positions.get("d4", None), Rook)

def test_rook_cant_jump_over_ally():
    board = Board.move(0, "d4h4")
    assert board.legal == False
    assert isinstance(board.positions.get("d4", None), Rook)

def test_rook_cant_jump_over_opponent():
    board = Board.move(0, "d4d8")
    assert board.legal == False
    assert isinstance(board.positions.get("d4", None), Rook)

def test_rook_takes():
    board = Board.move(0, "d4d7")
    assert board.legal == True
    assert board.positions.get("d7", None).color == Color.WHITE