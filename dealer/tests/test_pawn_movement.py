import pytest
from board import Board
from piece import Color, Pawn


@pytest.fixture
def pawn_takes_board_from_a4():
        board = Board()
        board.bypass_validation_move("a2a4")  
        board.bypass_validation_move("b7b5")  
        board.bypass_validation_move("a7a5")  
        return board

@pytest.fixture
def pawn_out_to_a3():
        board = Board()
        board.bypass_validation_move("a2a3")  
        return board

@pytest.fixture
def knight_out_to_c3():
        board = Board()
        board.bypass_validation_move("b1c3")  
        return board

@pytest.fixture
def board():
        board = Board()
        return board

def test_pawn_two_step(board: Board):
    board.move("a2a4")
    assert board.legal == True
    assert isinstance(board.positions.get("a4", None), Pawn)

def test_pawn_one_step(board: Board):
    board.move("a2a3")
    assert board.legal == True
    assert isinstance(board.positions.get("a3", None), Pawn)

def test_pawn_step_back(pawn_takes_board_from_a4: Board):
    pawn_takes_board_from_a4.move("a4a3")
    assert pawn_takes_board_from_a4.legal == False
    assert isinstance(pawn_takes_board_from_a4.positions.get("a4", None), Pawn)

def test_pawn_illegal_two_step(pawn_out_to_a3: Board):
    pawn_out_to_a3.move("a3a5")
    assert pawn_out_to_a3.legal == False
    assert isinstance(pawn_out_to_a3.positions.get("a3", None), Pawn)

def test_locked_pawn(knight_out_to_c3: Board):
    knight_out_to_c3.move("c2c3")
    assert knight_out_to_c3.legal == False
    assert isinstance(knight_out_to_c3.positions.get("c2", None), Pawn)

def test_locked_pawn_two_step(knight_out_to_c3: Board):
    knight_out_to_c3.move("c2c4")
    assert knight_out_to_c3.legal == False
    assert isinstance(knight_out_to_c3.positions.get("c2", None), Pawn)

def test_valid_pawn_takes(pawn_takes_board_from_a4: Board):
    assert pawn_takes_board_from_a4.positions.get("b5", None).color == Color.BLACK
    pawn_takes_board_from_a4.move("a4b5")
    assert pawn_takes_board_from_a4.legal == True
    assert isinstance(pawn_takes_board_from_a4.positions.get("b5", None), Pawn)
    assert pawn_takes_board_from_a4.positions.get("b5", None).color == Color.WHITE

def test_invalid_pawn_takes(pawn_takes_board_from_a4: Board):
    assert pawn_takes_board_from_a4.positions.get("a5", None).color == Color.BLACK
    pawn_takes_board_from_a4.move("a4a5")
    assert pawn_takes_board_from_a4.legal == False
    assert isinstance(pawn_takes_board_from_a4.positions.get("a5", None), Pawn)
    assert pawn_takes_board_from_a4.positions.get("a5", None).color == Color.BLACK
    assert pawn_takes_board_from_a4.positions.get("a4", None).color == Color.WHITE