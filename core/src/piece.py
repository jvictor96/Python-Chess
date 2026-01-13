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
    def is_movement_valid(self, destination: tuple[Position, "Piece"]) -> bool:
        pass

    @abstractmethod
    def get_middle_places(self, destination: dict[Position, "Piece"]) -> list[Position]:
        pass

    @abstractmethod
    def get_all_possible_destinations(self) -> list[Position]:
        pass

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)

    def is_movement_valid(self, destination: tuple[Position, "Piece"]) -> bool:
        verifications = [
            destination[0].x == self.position.x,
            destination[0].y == self.position.y,
        ]
        return any(verifications)
    
    def get_middle_places(self, destination: dict[Position, "Piece"]) -> list[Position]:
        min_x = min(destination[0].x, self.position.x)
        max_x = max(destination[0].x, self.position.x)
        min_y = min(destination[0].y, self.position.y)
        max_y = max(destination[0].y, self.position.y)
        possibilities = {
            destination[0].x == self.position.x: lambda: [Position(self.position.x, i) for i in range(min_y + 1, max_y)],
            destination[0].y == self.position.y: lambda: [Position(i, self.position.y) for i in range(min_x + 1, max_x)]
        }
        return possibilities[True]()
    
    def get_all_possible_destinations(self):
        result = [Position(self.position.x, i) for i in range(1,9) if i != self.position.y]
        result.extend([Position(i, self.position.y) for i in range(1,9) if i != self.position.x])
        return [pos for pos in result if pos.is_valid()]

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)

    def is_movement_valid(self, destination: tuple[Position, "Piece"]) -> bool:
        verifications = [
            abs(destination[0].x - self.position.x) == 2 and abs(destination[0].y - self.position.y) == 1,
            abs(destination[0].x - self.position.x) == 1 and abs(destination[0].y - self.position.y) == 2,
        ]
        return any(verifications)
    
    def get_middle_places(self, destination: dict[Position, "Piece"]) -> list[Position]:
        return []
    
    def get_all_possible_destinations(self):
        destinations = []
        delta_map = {
            0: [1,2],
            1: [-1,2],
            2: [1,-2],
            3: [-1,-2],
            4: [2,1],
            5: [2,-1],
            6: [-2,1],
            7: [-2,-1],
        }
        for i in range(8):
            destinations.append(Position(self.position.x+delta_map[i][0], self.position.y+delta_map[i][1]))
        return [pos for pos in destinations if pos.is_valid()]

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)

    def is_movement_valid(self, destination: tuple[Position, "Piece"]) -> bool:
        return abs(destination[0].x - self.position.x) == abs(destination[0].y - self.position.y)
    
    def get_middle_places(self, destination: dict[Position, "Piece"]) -> list[Position]:
        min_x = min(destination[0].x, self.position.x)
        max_x = max(destination[0].x, self.position.x)
        min_y = min(destination[0].y, self.position.y)
        max_y = max(destination[0].y, self.position.y)
        possibilities = {
            destination[0].x - destination[0].y == self.position.x - self.position.y: lambda: [Position(min_x + i, min_y + i) for i in range(1, max_x - min_x)],
            destination[0].x - destination[0].y != self.position.x - self.position.y: lambda: [Position(min_x + i, max_y - i) for i in range(1, max_x - min_x)]
        }
        return possibilities[True]()
    
    def get_all_possible_destinations(self):
        min_diag_1 = Position(1, self.position.y - self.position.x + 1)
        min_diag_2 = Position(1, self.position.y + self.position.x - 1)
        result = [Position(min_diag_1.x+i, min_diag_1.y+i) for i in range(0,9-min_diag_1.y) if min_diag_1.x+i != self.position.x]
        result.extend([Position(min_diag_2.x+i, min_diag_2.y-i) for i in range(0,min_diag_2.y) if min_diag_2.x+i != self.position.x])
        return [pos for pos in result if pos.is_valid()]


class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)

    def is_movement_valid(self, destination: tuple[Position, "Piece"]) -> bool:
        verifications = [
            destination[0].x == self.position.x,
            destination[0].y == self.position.y,
            abs(destination[0].x - self.position.x) == abs(destination[0].y - self.position.y)
        ]
        return any(verifications)
    
    def get_middle_places(self, destination: dict[Position, "Piece"]) -> list[Position]:
        min_x = min(destination[0].x, self.position.x)
        max_x = max(destination[0].x, self.position.x)
        min_y = min(destination[0].y, self.position.y)
        max_y = max(destination[0].y, self.position.y)
        possibilities = {
            destination[0].x == self.position.x or destination[0].y == self.position.y: {
                destination[0].x == self.position.x: lambda: [Position(self.position.x, i) for i in range(min_y + 1, max_y)],
                destination[0].y == self.position.y: lambda: [Position(i, self.position.y) for i in range(min_x + 1, max_x)],
            },
                destination[0].x != self.position.x and destination[0].y != self.position.y: {destination[0].x - destination[0].y == self.position.x - self.position.y: lambda: [Position(min_x + i, min_y + i) for i in range(1, max_x - min_x)],
                destination[0].x - destination[0].y != self.position.x - self.position.y: lambda: [Position(min_x + i, max_y - i) for i in range(1, max_x - min_x)]
            }
        }
        return possibilities[True][True]()
    
    def get_all_possible_destinations(self):
        min_diag_1 = Position(1, self.position.y - self.position.x + 1)
        min_diag_2 = Position(1, self.position.y + self.position.x - 1)
        result = [Position(min_diag_1.x+i, min_diag_1.y+i) for i in range(0,9-min_diag_1.y) if min_diag_1.x+i != self.position.x]
        result.extend([Position(min_diag_2.x+i, min_diag_2.y-i) for i in range(0,min_diag_2.y) if min_diag_2.x+i != self.position.x])
        result.extend([Position(self.position.x, i) for i in range(1,9) if i != self.position.y])
        result.extend([Position(i, self.position.y) for i in range(1,9) if i != self.position.x])
        return [pos for pos in result if pos.is_valid()]

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)

    def is_movement_valid(self, destination: tuple[Position, "Piece"]) -> bool:
        verifications = [
            abs(destination[0].x - self.position.x) <= 1,
            abs(destination[0].y - self.position.y) <= 1
        ]
        return all(verifications)
    
    def get_middle_places(self, destination: dict[Position, "Piece"]) -> list[Position]:
        return []
    
    def get_all_possible_destinations(self):
        destinations = []
        delta_map = {
            0: [1,0],
            1: [1,1],
            2: [0,1],
            3: [1,-1],
            4: [-1,1],
            5: [-1,0],
            6: [-1,-1],
            7: [0,-1],
        }
        for i in range(8):
            destinations.append(Position(self.position.x+delta_map[i][0], self.position.y+delta_map[i][1]))
        return [pos for pos in destinations if pos.is_valid()]

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)

    def is_movement_valid(self, destination: tuple[Position, "Piece"]) -> bool:
        verifications = [
            destination[1] == None and self.color == Color.WHITE and destination[0].y - self.position.y == 1 and destination[0].x == self.position.x,
            destination[1] == None and self.color == Color.WHITE and destination[0].y - self.position.y == 2 and self.position.y == 2 and destination[0].x == self.position.x,
            destination[1] == None and self.color == Color.BLACK and destination[0].y - self.position.y == -1 and destination[0].x == self.position.x,
            destination[1] == None and self.color == Color.BLACK and destination[0].y - self.position.y == -2 and self.position.y == 7 and destination[0].x == self.position.x,
            destination[1] != None and destination[1].color == Color.BLACK and self.color == Color.WHITE and destination[0].y - self.position.y == 1  and abs(destination[0].x - self.position.x) == 1,
            destination[1] != None and destination[1].color == Color.WHITE and self.color == Color.BLACK and destination[0].y - self.position.y == -1 and abs(destination[0].x - self.position.x) == 1,
            
        ]
        return any(verifications)
    
    def get_middle_places(self, destination: dict[Position, "Piece"]) -> list[Position]:
        return [] if abs(destination[0].y - self.position.y) == 1 else [Position(self.position.x, (self.position.y + destination[0].y) // 2)]

    
    def get_all_possible_destinations(self):
        destinations = [
            Position(self.position.x,self.position.y + 1),
            Position(self.position.x,self.position.y + 2),
            Position(self.position.x+1,self.position.y + 1),
            Position(self.position.x-1,self.position.y + 1),
            ]
        return [pos for pos in destinations if pos.is_valid()]

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