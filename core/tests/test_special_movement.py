from board import Board

import pytest

# game id 1 had one white rook at d4, h1 and c1 free and one white bishop at e4

@pytest.fixture
def board():
        board = Board()
        board.bypass_validation_move("f1f4")  
        board.bypass_validation_move("g1g4")  
        board.bypass_validation_move("f8f5")  
        board.bypass_validation_move("g8g5")  
        return board

def test_minor_roque(board: Board):
    board.move("e1g1")
    assert board.legal

def test_blocked_minor_roque(board: Board):
    assert False == True

def test_moved_king_minor_roque(board: Board):
    assert False == True

def test_moved_rook_minor_roque(board: Board):
    assert False == True

def test_major_roque(board: Board):
    board.move("e1a1")
    assert board.legal

def test_promotion(board: Board):
    assert False == True