from enum import Enum
import json
import os


class State(Enum):
    IDLE = "IDLE"
    JUST_WRITTEN = "JUST_WRITTEN"

class NewGame():
    white: str
    black: str

    def __init__(self, white: str, black: str):
        self.white = white
        self.black = black

class DaemonState():
    new_game: NewGame
    end_game: int
    state: State
    games: list[int]
    old_state: "DaemonState"

    def __init__(self, new_game: NewGame, end_game: int, state: State, games: list[int]):
        self.new_game = new_game
        self.end_game = end_game
        self.state = state
        self.games = games
    
    @staticmethod
    def get_path() -> str:
        return f"{os.environ['HOME']}/python_chess"
    
    @staticmethod
    def get_state() -> "DaemonState":
        try:
            with open(f"{DaemonState.get_path()}/daemon.json", "r+") as daemon:
                control_fields = json.load(daemon)
                return DaemonState(
                    new_game = NewGame(
                        control_fields["new_game"]["white"],
                        control_fields["new_game"]["black"]
                    ),
                    end_game = control_fields["end_game"],
                    games = control_fields["games"])
        except FileNotFoundError as e:
                return DaemonState(
                    new_game = NewGame(
                        "",
                        ""
                    ),
                    end_game = 0,
                    games = [])
    
    def new_game(self, new_game: NewGame):
        if self.state != State.IDLE:
            self.new_game = new_game
            self.state = State.JUST_WRITTEN
        return self

    
    def end_game(self, end_game: int):
        if self.state != State.IDLE:
            self.end_game = end_game
            self.state = State.JUST_WRITTEN
        return self
    
    def clear(self):
        self.old_state.end_game = self.end_game
        self.old_state.new_game = self.new_game
        self.old_state.state = self.state
        self.end_game = 0
        self.new_game = NewGame("", "")
        self.state = State.IDLE
        return self

    def burn(self):
        with open(f"{DaemonState.get_path()}/daemon.json", "w") as daemon:
            json.dump({"new_game": self.new_game,
                       "end_game": self.end_game,
                       "state": self.state,
                       "games": self.games
                       })
        return self.old_state