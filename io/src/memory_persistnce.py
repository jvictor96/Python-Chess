import json
import os
from board import Board
from ports import GamePersistencePort

class MemoryGamePersistenceAdapter(GamePersistencePort):
    boards: dict[int, Board]
    id: int

    def __init__(self):
        self.boards = {}
        self.id = 0

    def get_board(self, game_id: int) -> "Board":
        if game_id == 0:
            return Board()
        return self.boards[game_id] if game_id in self.boards.keys() else None

    def burn(self, board: "Board"):
        self.boards[board.game_id] = board

    def delete_game(self, board):
        self.boards.pop()

    def next_id(self):
        self.id=self.id+1
        return self.id
    
    def list_games(self):
        return [key for key, value in self.boards.items()]