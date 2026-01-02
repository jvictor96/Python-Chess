import os, json
from dataclasses import asdict
from ports import GamePersistencePort
from abc import ABC, abstractmethod
from machine_core import MovementMessage
from external_event_source import ExternalEventSource
from typing import Iterable

class OpponentInterface(ExternalEventSource[MovementMessage], ABC):
    @abstractmethod
    def poll(self) -> Iterable[MovementMessage]:
        pass

    @abstractmethod
    def send_message(self, message: MovementMessage) -> None:
        pass

class FileOpponentInterface(OpponentInterface):
    def __init__(self, user: str, persistence: GamePersistencePort):
        self.path = f"{os.environ['HOME']}/python_chess"
        self.persistence = persistence
        self.user = user
        if f"{user}.fifo" not in os.listdir(self.path):
            os.mkfifo(f"{self.path}/{self.user}.fifo")
    
    def poll(self) -> Iterable[MovementMessage]:          # I know this implementation blocks the flow
        with open(f"{self.path}/{self.user}.fifo", "r") as ff:
            content = json.load(ff)
        return [MovementMessage(
            move=content["move"],
            game=content["game"],)
            ]
    
    def send_message(self, message: MovementMessage) -> None:          # I know this implementation blocks the flow
        board = self.persistence.get_board(message.game)
        other_user = [player for player in [board.black, board.white] if player != self.user][0]
        if not (f"{other_user}.fifo" in os.listdir(self.path)):
            os.mkfifo(f"{self.path}/{other_user}.fifo")
        with open(f"{self.path}/{other_user}.fifo", "w") as ff:
            data = asdict(message)
            data.pop("player_state", None)
            json.dump(data, ff)