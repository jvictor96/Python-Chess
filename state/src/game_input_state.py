from enum import Enum
import json
import os


class State(Enum):
    IDLE = "IDLE"
    JUST_WRITTEN = "JUST_WRITTEN"

class GameInputState():
    game_id: int
    move: str
    error: str

    def __init__(self, game_id: int, move: str, error: str):
        self.move = move
        self.error = error
        self.game_id = game_id
        self.state = State.IDLE
    
    @staticmethod
    def get_path() -> str:
        return f"{os.environ['HOME']}/python_chess"
    
    @staticmethod
    def get_state(game_id: int) -> "GameInputState":
        with open(f"{GameInputState.get_path()}/game_{game_id}_input.json", "r+") as input:
            control_fields = json.load(input)
            return GameInputState(
                game_id=game_id,
                move = control_fields["move"],
                error = control_fields["error"])

    def move(self, move: str):
        self.move = move
        self.state = State.JUST_WRITTEN
        return self

    def clear(self, error: list[str] = ""):
        old_state = GameInputState(
            move=self.move,
            error=self.error,
            state=self.state,
        )
        self.error = error
        self.move = ""
        self.state = State.IDLE
        return old_state

    def burn(self):
        with open(f"{GameInputState.get_path()}/game_{self.game_id}_input.json", "w") as input:
            json.dump({"move": self.move,
                       "error": self.error,
                       "state": self.state,
                       }, input)
        return self