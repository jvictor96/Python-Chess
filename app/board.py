from abc import abstractmethod
import json
from movement import Movement
from piece import Piece, PieceSerializer
from position import Position


class Board:
    movements: list[Movement]
    pieces: list[Piece]
    positions: dict[Position, Piece]
    legal: bool

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
    def get_board(game_id: int) -> "Board":
        board: Board
        with open(f"app/games/game_{game_id}.txt", "r") as file:
            game = json.load(file)
            board = Board(
                [PieceSerializer.deserialize(piece) for piece in game["pieces"]], game["movements"])
        return board
    
    def bypass_validation_move(self, movement: str):
        movement = Movement.from_string(movement, self.positions)
        piece = self.positions.get(movement.start_pos)
        self.movements.append(movement)
        self.positions.pop(movement.start_pos)
        self.positions[movement.end_pos] = piece
        self.pieces = [piece for pos, piece in self.positions.items()]
        return self

    def save_board(self, game_id: int):
        with open(f"app/games/game_{game_id}.txt", "w") as file:
            game = {
                "pieces": [PieceSerializer.serialize(piece) for piece in self.pieces],
                "movements": self.movements
            }
            json.dump(game, file)

    
    def add_piece(self, piece: Piece):
        self.pieces.append(piece)

    def validate_move(self, movement: Movement) -> bool:
        piece = self.positions.get(movement.start_pos)
        if piece is None:
            return False
        return piece.is_movement_valid(movement.end_pos)

    @abstractmethod
    def move(game_id: str, movement: str):
        board = Board.get_board(game_id)
        movement = Movement.from_string(movement, board.positions)
        if movement.is_valid():
            board.legal = True
        else:
            board.legal = False 
        if board.legal:
            piece = board.positions.get(movement.start_pos)
            board.movements.append(movement)
            board.positions.pop(movement.start_pos)
            board.positions[movement.end_pos] = piece
            board.pieces = [piece for pos, piece in board.positions.items()]
        if game_id > 0:
            board.save_board(game_id)
        return board

    def keep_moving(self, movement: str):
        movement = Movement.from_string(movement, self.positions)
        if movement.is_valid():
            self.legal = True
        else:
            self.legal = False 
        if self.legal:
            piece = self.positions.get(movement.start_pos)
            self.movements.append(movement)
            self.positions.pop(movement.start_pos)
            self.positions[movement.end_pos] = piece
            self.pieces = [piece for pos, piece in self.positions.items()]
        return self