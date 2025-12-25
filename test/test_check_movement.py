from board import Board
from piece import King, Color

# game id 3 has d2 and e2 free and black bishop at b4

def test_king_move_out_check():
    board = Board.move(2, "e1e2")
    assert board.legal == True
    assert isinstance(board.positions.get("e2", None), King)