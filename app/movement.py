from abc import abstractmethod
from position import Position


class Movement:
    start_pos: Position
    end_pos: Position

    @abstractmethod
    def from_string(p: str):
        return Movement(Position(ord(p[0]) - ord('a') + 1, int(p[1])), Position(ord(p[2]) - ord('a') + 1, int(p[3])))

    def __init__(self, start_pos: Position, end_pos: Position):
        self.start_pos = start_pos
        self.end_pos = end_pos

    def __repr__(self):
        return self.start_pos + self.end_pos

    def is_valid(self):
        # Placeholder for movement validation logic
        return True
    
    def is_there_a_piece_in_the_origin(self):
        # Placeholder for origin piece validation logic
        return True

    def is_the_destination_different_from_origin_and_in_the_board(self):
        return self.start_pos != self.end_pos

    def is_the_player_turn(self):
        # Placeholder for turn validation logic
        return True

    def will_be_the_king_in_check(self):
        # Placeholder for check validation logic
        return False