from abc import ABC, abstractmethod
from enum import Enum

from position import Position

class Color(Enum):
    WHITE = "W"
    BLACK = "B"

class Piece(ABC):
    color: Color
    position: Position

    def __init__(self, color, position):
        self.color = color
        self.position = position

    @abstractmethod
    def is_movement_valid(self, destination: dict[Position, "Piece"]) -> bool:
        pass

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
    def is_movement_valid(self, destination: dict[Position, "Piece"]) -> bool:
        pass

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
    def is_movement_valid(self, destination: dict[Position, "Piece"]) -> bool:
        pass

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
    def is_movement_valid(self, destination: dict[Position, "Piece"]) -> bool:
        pass

class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
    def is_movement_valid(self, destination: dict[Position, "Piece"]) -> bool:
        pass

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
    def is_movement_valid(self, destination: dict[Position, "Piece"]) -> bool:
        pass

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
    def is_movement_valid(self, destination: dict[Position, "Piece"]) -> bool:
        pass


piece_map = {
    "R": Rook,
    "N": Knight,
    "B": Bishop,
    "Q": Queen,
    "K": King,
    "P": Pawn,
    Rook: "R",
    Knight: "N",
    Bishop: "B",
    Queen: "Q",
    King: "K",
    Pawn: "P",
}

color_map = {
    "W": Color.WHITE,
    "B": Color.BLACK,
    Color.WHITE: "W",
    Color.BLACK: "B",
}

class PieceSerializer:
    @staticmethod
    def serialize(piece: Piece) -> str:
        piece_type = piece_map[type(piece)]
        return {"color": piece.color.value, "piece": piece_type, "position": piece.position}
    
    @staticmethod
    def deserialize(data: dict) -> Piece:
        color = color_map[data["color"]]
        piece_type = data["piece"]
        position = data["position"]
        return piece_map[piece_type](color, Position.from_string(position))