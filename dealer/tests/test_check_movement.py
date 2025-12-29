import pytest
from board import Board, BoardIO
from piece import King, Queen, Pawn

# game id 3 had d2 and e2 free and black bishop at b4

@pytest.fixture
def king_in_check_by_bishop():
        board = BoardIO.get_board(0)
        board = board.bypass_validation_move("d2d4")  
        board = board.bypass_validation_move("e2e4")  
        board = board.bypass_validation_move("f8b4")  
        return board

# game id 4 had black bishop at b4

@pytest.fixture
def board4():
        board = BoardIO.get_board(0)
        board.bypass_validation_move("f8b4")  
        return board

# game id 5 e2 free and black bishop at g4

@pytest.fixture
def board5():
        board = BoardIO.get_board(0)
        board.bypass_validation_move("e2e4")  
        board.bypass_validation_move("c8g4")  
        return board

def test_king_move_out_check(king_in_check_by_bishop: Board):
    king_in_check_by_bishop.move("e1e2")
    assert king_in_check_by_bishop.legal == True
    assert isinstance(king_in_check_by_bishop.positions.get("e2", None), King)

def test_king_move_is_still_check(king_in_check_by_bishop: Board):
    king_in_check_by_bishop.move("e1d2")
    assert king_in_check_by_bishop.legal == False
    assert isinstance(king_in_check_by_bishop.positions.get("e1", None), King)

def test_check_is_blocked_by_queen(king_in_check_by_bishop: Board):
    king_in_check_by_bishop.move("d1d2")
    assert king_in_check_by_bishop.legal == True
    assert isinstance(king_in_check_by_bishop.positions.get("d2", None), Queen)

def test_queen_moves_but_still_check(king_in_check_by_bishop: Board):
    king_in_check_by_bishop.move("d1d3")
    assert king_in_check_by_bishop.legal == False
    assert isinstance(king_in_check_by_bishop.positions.get("d1", None), Queen)

def test_invalid_pawn_moves_and_puts_king_in_check(board4: Board):
    board4.move("d2d3")
    assert board4.legal == False
    assert isinstance(board4.positions.get("d2", None), Pawn)

def test_invalid_king_goes_to_check(board5: Board):
    board5.move("e1e2")
    assert board5.legal == False
    assert isinstance(board5.positions.get("e1", None), King)