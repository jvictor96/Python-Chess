from abc import abstractmethod

from dataclasses import dataclass


class Position:
    x: int
    y: int

    @abstractmethod
    def from_string(p: str):
        return Position(ord(p[0]) - ord('a') + 1, int(p[1]))

    def __repr__(self):
        return f"{chr(self.x + ord('a') - 1) + str(self.y)}"
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        if isinstance(other, str):
            return self.__repr__() == other
        return False
        
    
    def __hash__(self):
        return hash(self.__repr__())