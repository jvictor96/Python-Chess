from board import Board

import pytest

# game id 1 had one white rook at d4, h1 and c1 free and one white bishop at e4

@pytest.fixture
def board():
        board = Board()
        board.bypass_validation_move("f1f4")  
        board.bypass_validation_move("g1g4")  
        board.bypass_validation_move("b1b4")  
        board.bypass_validation_move("c1c4")  
        board.bypass_validation_move("d1d4")  
        board.bypass_validation_move("e2e3")  
        board.bypass_validation_move("h2h3")  
        return board

@pytest.fixture
def blocked_by_kngiht():
        board = Board()
        board.bypass_validation_move("f1f4")  
        board.bypass_validation_move("c1c4")  
        return board

@pytest.fixture
def blocked_by_bishop():
        board = Board()
        board.bypass_validation_move("g1g4")  
        board.bypass_validation_move("b1b4")  
        return board

@pytest.fixture
def blocked_by_queen():
        board = Board()
        board.bypass_validation_move("b1b4")  
        board.bypass_validation_move("c1b4")   
        return board

@pytest.fixture
def absent_rook():
        board = Board()
        board.bypass_validation_move("b1b4")  
        board.bypass_validation_move("c1b4")   
        board.bypass_validation_move("a1a4")   
        return board

def test_minor_roque(board: Board):
    board.move("e1g1")
    assert board.legal

def test_major_roque(board: Board):
    board.move("e1c1")
    assert board.legal

def test_blocked_by_knight_minor_roque(blocked_by_kngiht: Board):
    blocked_by_kngiht.move("e1g1")
    assert not blocked_by_kngiht.legal

def test_blocked_by_knight_major_roque(blocked_by_kngiht: Board):
    blocked_by_kngiht.move("e1c1")
    assert not blocked_by_kngiht.legal

def test_blocked_by_bishop_minor_roque(blocked_by_bishop: Board):
    blocked_by_bishop.move("e1g1")
    assert not blocked_by_bishop.legal

def test_blocked_by_bishop_major_roque(blocked_by_bishop: Board):
    blocked_by_bishop.move("e1c1")
    assert not blocked_by_bishop.legal

def test_blocked_by_queen_major_roque(blocked_by_queen: Board):
    blocked_by_queen.move("e1c1")
    assert not blocked_by_queen.legal

def test_absent_rook_roque(absent_rook: Board):
    absent_rook.move("e1c1")
    assert not absent_rook.legal

def test_moved_king_minor_roque(board: Board):
    board.move("e1e2")
    assert board.legal
    board.move("a7a6")
    assert board.legal
    board.move("e2e1")
    assert board.legal
    board.move("a6a5")
    assert board.legal
    board.move("e1g1")
    assert not board.legal

def test_moved_rook_minor_roque(board: Board):
    board.move("h1h2")
    assert board.legal
    board.move("a7a6")
    assert board.legal
    board.move("h2h1")
    assert board.legal
    board.move("a6a5")
    assert board.legal
    board.move("e1g1")
    assert not board.legal

def test_promotion(board: Board):
    assert False == True