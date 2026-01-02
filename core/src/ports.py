from abc import ABC, abstractmethod
from board import Board

class GameViewerPort(ABC):
    
    @abstractmethod
    def display():
        pass

class GamePersistencePort(ABC):
    
    @abstractmethod
    def get_board(self, game_id: int) -> Board:
        pass
        
    @abstractmethod
    def delete_game(self, board: int):
        pass
        
    @abstractmethod
    def burn(self, board: Board):
        pass
        
    @abstractmethod
    def next_id(self):
        pass 