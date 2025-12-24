import json
from movement import Movement
from piece import Piece, PieceSerializer
from position import Position


class Board:
    movements: list[Movement]
    pieces: list[Piece]
    positions: dict[Position, Piece]

    def __init__(self, pieces: list[Piece] = None, movements=None):
        self.pieces: list[Piece] = pieces
        self.movements: list[Movement] = movements
        self.positions = {piece.position: piece for piece in pieces} 

    def display(self) -> list[str]:
        board_representation = []
        for y in range(8, 0, -1):
            row = ""
            for x in range(1, 9):
                pos = Position(x, y)
                piece = self.positions.get(pos)
                if piece:
                    piece_symbol = PieceSerializer.serialize(piece)["piece"]
                    row += piece_symbol + " "
                else:
                    row += ". "
            board_representation.append(row.strip())
        return board_representation
        

    @staticmethod
    def get_board(address: str) -> "Board":
        board: Board
        with open(address, "r") as file:
            game = json.load(file)
            board = Board(
                [PieceSerializer.deserialize(piece) for piece in game["pieces"]], game["movements"])
        return board
    
    def save_board(self, address: str):
        with open(address, "w") as file:
            game = {
                "pieces": [PieceSerializer.serialize(piece) for piece in self.pieces],
                "movements": self.movements
            }
            json.dump(game, file)

    
    def add_piece(self, piece: Piece):
        self.pieces.append(piece)
    
    def add_movement(self, movement: Movement):
        if not movement.is_valid(): return
        self.movements.append(movement)