from board import Board
from piece import Bishop, Color, King, Knight, Pawn, Queen, Rook
from position import Position

def test_load():
    board = Board.get_board(0)
    assert isinstance(board.positions.get("a1", None), Rook)

def test_game_id_0_is_a_regular_starting_board():   # it will be the setup for every game in production
    board = Board.get_board(0)
    assert isinstance(board.positions.get("a1", None), Rook)
    assert isinstance(board.positions.get("a8", None), Rook)
    assert isinstance(board.positions.get("h1", None), Rook)
    assert isinstance(board.positions.get("h8", None), Rook)
    assert board.positions.get("a1", None).color == Color.WHITE
    assert board.positions.get("h1", None).color == Color.WHITE
    assert board.positions.get("a8", None).color == Color.BLACK
    assert board.positions.get("h8", None).color == Color.BLACK
    assert isinstance(board.positions.get("b1", None), Knight)
    assert isinstance(board.positions.get("b8", None), Knight)
    assert isinstance(board.positions.get("g1", None), Knight)
    assert isinstance(board.positions.get("g8", None), Knight)
    assert board.positions.get("b1", None).color == Color.WHITE
    assert board.positions.get("g1", None).color == Color.WHITE
    assert board.positions.get("b8", None).color == Color.BLACK
    assert board.positions.get("g8", None).color == Color.BLACK
    assert isinstance(board.positions.get("c1", None), Bishop)
    assert isinstance(board.positions.get("c8", None), Bishop)
    assert isinstance(board.positions.get("f1", None), Bishop)
    assert isinstance(board.positions.get("f8", None), Bishop)
    assert board.positions.get("c1", None).color == Color.WHITE
    assert board.positions.get("f1", None).color == Color.WHITE
    assert board.positions.get("c8", None).color == Color.BLACK
    assert board.positions.get("f8", None).color == Color.BLACK
    assert isinstance(board.positions.get("d1", None), Queen)
    assert isinstance(board.positions.get("d8", None), Queen)
    assert isinstance(board.positions.get("e1", None), King)
    assert isinstance(board.positions.get("e8", None), King)
    assert board.positions.get("d1", None).color == Color.WHITE
    assert board.positions.get("e1", None).color == Color.WHITE
    assert board.positions.get("d8", None).color == Color.BLACK
    assert board.positions.get("e8", None).color == Color.BLACK
    assert isinstance(board.positions.get("a2", None), Pawn)
    assert isinstance(board.positions.get("b2", None), Pawn)
    assert isinstance(board.positions.get("c2", None), Pawn)
    assert isinstance(board.positions.get("d2", None), Pawn)
    assert isinstance(board.positions.get("e2", None), Pawn)
    assert isinstance(board.positions.get("f2", None), Pawn)
    assert isinstance(board.positions.get("g2", None), Pawn)
    assert isinstance(board.positions.get("h2", None), Pawn)
    assert isinstance(board.positions.get("a7", None), Pawn)
    assert isinstance(board.positions.get("b7", None), Pawn)
    assert isinstance(board.positions.get("c7", None), Pawn)
    assert isinstance(board.positions.get("d7", None), Pawn)
    assert isinstance(board.positions.get("e7", None), Pawn)
    assert isinstance(board.positions.get("f7", None), Pawn)
    assert isinstance(board.positions.get("g7", None), Pawn)
    assert isinstance(board.positions.get("h7", None), Pawn)
    assert board.positions.get("a2", None).color == Color.WHITE
    assert board.positions.get("b2", None).color == Color.WHITE
    assert board.positions.get("c2", None).color == Color.WHITE
    assert board.positions.get("d2", None).color == Color.WHITE
    assert board.positions.get("e2", None).color == Color.WHITE
    assert board.positions.get("f2", None).color == Color.WHITE
    assert board.positions.get("g2", None).color == Color.WHITE
    assert board.positions.get("h2", None).color == Color.WHITE
    assert board.positions.get("a7", None).color == Color.BLACK
    assert board.positions.get("b7", None).color == Color.BLACK
    assert board.positions.get("c7", None).color == Color.BLACK
    assert board.positions.get("d7", None).color == Color.BLACK
    assert board.positions.get("e7", None).color == Color.BLACK
    assert board.positions.get("f7", None).color == Color.BLACK
    assert board.positions.get("g7", None).color == Color.BLACK
    assert board.positions.get("h7", None).color == Color.BLACK