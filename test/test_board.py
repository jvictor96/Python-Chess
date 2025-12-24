from board import Board
from piece import Rook
from position import Position

def test_load():
    board = Board.get_board(0)
    assert board.positions[Position(1, 1)].__class__ != Rook.__class__