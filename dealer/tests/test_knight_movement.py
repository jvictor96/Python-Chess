import pytest
from board import Board, BoardIO
from piece import Color, Knight

@pytest.fixture
def knight_takes_board():
        board = BoardIO.get_board(0)
        board.bypass_validation_move("b1c3")  
        board.bypass_validation_move("d7d5")  
        return board

@pytest.fixture
def knight_out():
        board = BoardIO.get_board(0)
        board.bypass_validation_move("b1c3")  
        return board

@pytest.fixture
def board():
        board = BoardIO.get_board(0)
        return board

def test_valid_knight_move(board: Board):
    board.move("b1a3")
    assert board.legal == True
    assert isinstance(board.positions.get("a3", None), Knight)

def test_valid_knight_move_flipped_90(knight_out: Board):
    knight_out.move("c3e4")
    assert knight_out.legal == True
    assert isinstance(knight_out.positions.get("e4", None), Knight)

def test_valid_knight_move_flipped_180(board: Board):
    board.move("b1c3")
    assert board.legal == True
    assert isinstance(board.positions.get("c3", None), Knight)

def test_valid_knight_move_flipped_270(knight_out: Board):
    knight_out.move("c3a4")
    assert knight_out.legal == True
    assert isinstance(knight_out.positions.get("a4", None), Knight)

def test_invalid_knight_move(board: Board):
    board.move("b1b3")
    assert board.legal == False
    assert isinstance(board.positions.get("b1", None), Knight)

def test_blocked_knight_move(board: Board):
    board.move("b1d2")
    assert board.legal == False
    assert isinstance(board.positions.get("b1", None), Knight)

def test_knight_takes(knight_takes_board: Board):
    assert knight_takes_board.positions.get("d5", None).color == Color.BLACK
    knight_takes_board.move("c3d5")
    assert knight_takes_board.legal == True
    assert knight_takes_board.positions.get("d5", None).color == Color.WHITE