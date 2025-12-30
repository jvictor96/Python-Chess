from board import Board, BoardIO
from piece import Bishop, Color

import pytest

# game id 1 had one white rook at d4, h1 and c1 free and one white bishop at e4

@pytest.fixture
def board():
        board = BoardIO.get_board(0)
        board = board.bypass_validation_move("h1d4")  
        board = board.bypass_validation_move("c1e4")  
        return board

def test_minor_roque(board: Board):
    assert False == True

def test_blocked_minor_roque(board: Board):
    assert False == True

def test_moved_king_minor_roque(board: Board):
    assert False == True

def test_moved_rook_minor_roque(board: Board):
    assert False == True

def test_major_roque(board: Board):
    assert False == True

def test_promotion(board: Board):
    assert False == True