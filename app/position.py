from abc import abstractmethod

from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    @abstractmethod
    def from_string(p: str):
        return Position(ord(p[0]) - ord('a') + 1, int(p[1]))

    def __repr__(self):
        return chr(self.x + ord('a') - 1) + str(self.y)