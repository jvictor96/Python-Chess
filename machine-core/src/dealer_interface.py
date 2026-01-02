import os, json
from dataclasses import asdict
from abc import ABC, abstractmethod
from machine_core import DealerMessage, NewGame
from external_event_source import ExternalEventSource
from typing import Iterable

class DealerInterface(ExternalEventSource[DealerMessage], ABC):
    @abstractmethod
    def poll(self) -> Iterable[DealerMessage]:
        pass

    @abstractmethod
    def send_message(self, message: DealerMessage) -> None:
        pass

class FileDealerInterface(DealerMessage):
    def __init__(self):
        self.path = f"{os.environ['HOME']}/python_chess"
        if f"dealer.fifo" not in os.listdir(self.path):
            os.mkfifo(f"{self.path}/dealer.fifo")
    
    def poll(self) -> Iterable[DealerMessage]:          # I know this implementation blocks the flow
        with open(f"{self.path}/dealer.fifo", "r") as ff:
            content = json.load(ff)
        return [DealerMessage(
            new_game=NewGame(white=content["white"], black=content["black"]),
            end_game=content["end_game"],
            next_id=content["next_id"])
            ]
    
    def send_message(self, message: DealerMessage) -> None:          # I know this implementation blocks the flow
        with open(f"{self.path}/dealer.fifo", "w") as ff:
            data = asdict(message)
            data.pop("dealer_state", None)
            json.dump(data, ff)