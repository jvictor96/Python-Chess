from board import Board
from piece import King, Queen, Pawn

# game id 3 has d2 and e2 free and black bishop at b4
# game id 4 black bishop at b4
# game id 5 e2 free and black bishop at g4

def test_king_move_out_check():
    board = Board.move(3, "e1e2")
    assert board.legal == True
    assert isinstance(board.positions.get("e2", None), King)

def test_king_move_is_still_check():
    board = Board.move(3, "e1d2")
    assert board.legal == False
    assert isinstance(board.positions.get("e1", None), King)

def test_check_is_blocked_by_queen():
    board = Board.move(3, "d1d2")
    assert board.legal == True
    assert isinstance(board.positions.get("d2", None), Queen)

def test_invalid_pawn_moves_and_puts_king_in_check():
    board = Board.move(4, "d2d3")
    assert board.legal == False
    assert isinstance(board.positions.get("d2", None), Pawn)

def test_invalid_king_goes_to_check():
    board = Board.move(5, "e1e2")
    assert board.legal == False
    assert isinstance(board.positions.get("e1", None), King)