import json
from movement import Movement
from piece import Piece, PieceSerializer


class Board:
    movements: list[Movement]
    pieces: list[Piece]
    
    def __init__(self):
        pieces: list[Piece] = []
        movements: list[Movement] = []

    @staticmethod
    def get_board(address: str) -> "Board":
        board = Board()
        with open(address, "r") as file:
            game = json.load(file)
            board.pieces = game["pieces"]
            board.movements = game["movements"]
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