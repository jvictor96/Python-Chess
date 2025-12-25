from abc import abstractmethod
from piece import Piece
from position import Position


class Movement:
    start_pos: Position
    end_pos: Position
    positions: dict[Position, Piece]

    @abstractmethod
    def from_string(p: str, positions: dict[Position, Piece]):
        return Movement(
            Position(ord(p[0]) - ord('a') + 1, int(p[1])), 
            Position(ord(p[2]) - ord('a') + 1, int(p[3])),
            positions)

    def __init__(self, start_pos: Position, end_pos: Position, positions: list[Position]):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.positions = positions

    def __repr__(self):
        return f"{self.start_pos}{self.end_pos}"

    def is_valid(self):
        return all([
            self.is_the_path_clear(),
            self.is_the_destination_different_from_origin_and_in_the_board(),
            self.is_destinarion_free(),
            self.is_the_player_turn(),
            self.king_wont_be_in_check()])

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

    def is_the_player_turn(self):
        # Placeholder for turn validation logic
        return True

    def king_wont_be_in_check(self):
        # Placeholder for check validation logic
        return True