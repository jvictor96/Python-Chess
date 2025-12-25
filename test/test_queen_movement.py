from board import Board
from piece import Queen, Color

# game id 2 has one white queen at d4, d1, e1 free and one white Queen at e4 and a black pawn at e5

def test_valid_diagonal_up_queen_move():
    board = Board.move(2, "d4b6")
    assert board.legal == True
    assert isinstance(board.positions.get("b6", None), Queen)

def test_valid_diagonal_down_queen_move():
    board = Board.move(2, "d4c3")
    assert board.legal == True
    assert isinstance(board.positions.get("c3", None), Queen)

def test_valid_left_queen_move():
    board = Board.move(2, "d4c4")
    assert board.legal == True
    assert isinstance(board.positions.get("c4", None), Queen)

def test_valid_down_queen_move():
    board = Board.move(2, "d4d3")
    assert board.legal == True
    assert isinstance(board.positions.get("d3", None), Queen)

def test_invalid_queen_move():
    board = Board.move(2, "d4a3")
    assert board.legal == False
    assert isinstance(board.positions.get("d4", None), Queen)

def test_blocked_queen_move():
    board = Board.move(2, "d4e4")
    assert board.legal == False
    assert isinstance(board.positions.get("d4", None), Queen)

def test_queen_cant_jump_over_ally():
    board = Board.move(2, "d4h4")
    assert board.legal == False
    assert isinstance(board.positions.get("d4", None), Queen)

def test_queen_takes():
    board = Board.move(2, "d4e5")
    assert board.legal == True
    assert board.positions.get("e5", None).color == Color.WHITE