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

    def __init__(self, new_game: NewGame, end_game: int, state: State, games: list[int]):
        self.new_game = new_game
        self.end_game = end_game
        self.state = state
        self.games = games
        self.state = State.IDLE
    
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
        old_state = DaemonState(
            end_game = self.end_game,
            new_game = self.new_game,
            state = self.state,
        )
        self.end_game = 0
        self.new_game = NewGame("", "")
        self.state = State.IDLE
        return old_state

    def burn(self):
        with open(f"{DaemonState.get_path()}/daemon.json", "w") as daemon:
            json.dump({"new_game": self.new_game,
                       "end_game": self.end_game,
                       "state": self.state,
                       "games": self.games
                       }, daemon)
        return self