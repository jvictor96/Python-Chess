from abc import abstractmethod
from piece import Piece
from position import Position


class Movement:
    start_pos: Position
    end_pos: Position
    positions: dict[Position, Piece]
    roque: bool
    roque_rook_movement: Piece

    @abstractmethod
    def from_string(p: str, positions: dict[Position, Piece]) -> "Movement":
        return Movement(
            Position(ord(p[0]) - ord('a') + 1, int(p[1])), 
            Position(ord(p[2]) - ord('a') + 1, int(p[3])),
            positions)
    
    def clone(self):
        movement = Movement.from_string(repr(self), [])
        movement.roque = self.roque
        return movement

    def __init__(self, start_pos: Position, end_pos: Position, positions: list[Position]):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.positions = positions
        self.roque = False

    def __repr__(self):
        return f"{self.start_pos}{self.end_pos}"

    def reverse(self):
        return Movement.from_string(f"{self.end_pos}{self.start_pos}", self.positions)

    def is_valid(self):
        piece = self.get_piece_in_the_origin()
        if piece is None:
            return False
        if not piece.moved:
            if self.end_pos == self.start_pos.add(x=2) and piece.is_valid_roque([self.positions], self.end_pos):
                self.roque = True
                self.roque_rook_movement = Movement.from_string(f"{self.start_pos.add(x=3)}{self.start_pos.add(x=1)}")
                return True
            if self.end_pos == self.start_pos.add(x=-2) and piece.is_valid_roque([self.positions], self.end_pos):
                self.roque = True
                self.roque_rook_movement = Movement.from_string(f"{self.start_pos.add(x=-4)}{self.start_pos.add(x=-1)}")
                return True
        return all([
            self.is_the_path_clear(),
            self.is_the_destination_different_from_origin_and_in_the_board(),
            self.is_destinarion_free()])

    def get_piece_in_the_origin(self):
        return self.positions.get(self.start_pos, None)

    def is_the_path_clear(self):
        piece = self.get_piece_in_the_origin()
        if piece is None:
            return False
        if piece.is_movement_valid((self.end_pos, self.positions.get(self.end_pos))) is False:
            return False
        if any([place in self.positions.keys() for place in piece.get_middle_places((self.end_pos, self.positions.get(self.end_pos)))]):
            return False
        return True

    def is_the_destination_different_from_origin_and_in_the_board(self):
        return self.start_pos != self.end_pos

    def is_destinarion_free(self):
        return self.positions.get(self.end_pos, None) is None or self.positions.get(self.end_pos, None).color != self.get_piece_in_the_origin().color
    