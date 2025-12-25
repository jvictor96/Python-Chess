import pytest
from board import Board
from piece import Color, Knight, Pawn


@pytest.fixture
def board():
        board = Board.get_board(0)
        return board

def test_white_playing_twice_in_a_row(board: Board):
    board = board.move("a2a3")
    assert board.legal == True
    assert isinstance(board.positions.get("a3", None), Pawn)
    board = board.move("a3a4")
    assert board.legal == False
    assert isinstance(board.positions.get("a3", None), Pawn)

def test_white_playing_outside_the_board(board: Board):
    board = board.move("a2z9")
    assert board.legal == False
    assert isinstance(board.positions.get("a2", None), Pawn)

def test_white_playing_to_the_same_location(board: Board):
    board = board.move("a2a2")
    assert board.legal == False
    assert isinstance(board.positions.get("a2", None), Pawn)

def test_black_move_first(board: Board):
    board = board.move("a7a6")
    assert board.legal == False
    assert isinstance(board.positions.get("a7", None), Pawn)

def test_first_movement_is_invalid_white_plays_again(board: Board):
    board = board.move("a2a2")
    assert board.legal == False
    assert isinstance(board.positions.get("a2", None), Pawn)
    board = board.move("a2a3")
    assert board.legal == True
    assert isinstance(board.positions.get("a3", None), Pawn)