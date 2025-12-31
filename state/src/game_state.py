from enum import Enum
import json
import os


class State(Enum):
    JUST_UPDATED = "JUST_UPDATED"
    JUST_ACKNOWLEDGED = "JUST_ACKNOWLEDGED"

class Piece():
    piece: str
    color: str
    position: str

    def __init__(self, piece: str, color: str, position: str):
        self.piece = piece
        self.color = color
        self.position = position

class DaemonState():
    movements: list[str]
    state: State
    black: str
    white: str
    game_id: int
    pieces: list[Piece]
    old_state: "DaemonState"

    def __init__(self, game_id: int, movements: list[str], black: str, white: str, pieces: list[Piece]):
        self.movements = movements
        self.black = black
        self.white = white
        self.game_id = game_id
        self.pieces = pieces
        self.state = State.UPDATED
    
    @staticmethod
    def get_path() -> str:
        return f"{os.environ['HOME']}/python_chess"
    
    @staticmethod
    def get_state(game_id: int) -> "DaemonState":
        with open(f"{DaemonState.get_path()}/game_{game_id}.json", "r+") as game:
            control_fields = json.load(game)
            return DaemonState(
                game_id=game_id,
                movements = control_fields["movements"],
                black = control_fields["black"],
                white = control_fields["white"],
                pieces = [Piece(piece["piece"], piece["color"], piece["position"]) for piece in control_fields["pieces"]])

    def pieces(self, pieces: list[Piece]):
        self.pieces = pieces
        self.state = State.JUST_UPDATED
        return self

    def movements(self, movements: list[str]):
        self.movements = movements
        self.state = State.JUST_UPDATED
        return self
    
    def acknowledge(self):
        self.state = State.JUST_ACKNOWLEDGED
        return self
        
    def burn(self):
        with open(f"{DaemonState.get_path()}/game_{self.game_id}.json", "w") as game:
            json.dump({"movements": self.movements,
                        "pieces": self.pieces,
                        "state": self.state,
                        "black": self.black,
                        "white": self.white}, game)
        return self.old_state