from board import Board
from piece import Color, Knight, Pawn

def test_pawn_two_step():
    board = Board.move(0, "a2a4")
    assert board.legal == True
    assert isinstance(board.positions.get("a4", None), Pawn)

def test_pawn_one_step():
    board = Board.move(0, "a2a3")
    assert board.legal == True
    assert isinstance(board.positions.get("a3", None), Pawn)

def test_pawn_step_back():
    board = Board.move(0, "a2a3")
    board.keep_moving("a3a2")
    assert board.legal == False
    assert isinstance(board.positions.get("a3", None), Pawn)

def test_pawn_illegal_two_step():
    board: Board = Board.move(0, "a2a3")
    assert board.legal == True
    assert isinstance(board.positions.get("a3", None), Pawn)
    board.keep_moving("a7a6")
    board.keep_moving("a3a5")
    assert board.legal == False
    assert isinstance(board.positions.get("a3", None), Pawn)

def test_locked_pawn():
    board: Board = Board.move(0, "b1a3")
    assert board.legal == True
    assert isinstance(board.positions.get("a3", None), Knight)
    board.keep_moving("a7a6")
    board.keep_moving("a2a3")
    assert board.legal == False
    assert isinstance(board.positions.get("a2", None), Pawn)

def test_locked_pawn_two_step():
    board: Board = Board.move(0, "b1a3")
    assert board.legal == True
    assert isinstance(board.positions.get("a3", None), Knight)
    board.keep_moving("a7a6")
    board.keep_moving("a2a4")
    assert board.legal == False
    assert isinstance(board.positions.get("a2", None), Pawn)

def test_valid_pawn_takes():
    board: Board = Board.move(0, "a2a4")
    board.keep_moving("b7b5")
    board.keep_moving("a4b5")
    assert board.legal == True
    assert isinstance(board.positions.get("b5", None), Pawn)
    assert board.positions.get("b5", None).color == Color.WHITE

def test_invalid_pawn_takes():
    board: Board = Board.move(0, "a2a4")
    board.keep_moving("a7a5")
    board.keep_moving("a4a5")
    assert board.legal == False
    assert isinstance(board.positions.get("a5", None), Pawn)
    assert board.positions.get("a5", None).color == Color.BLACK