import json
import os
import time
from board import Board, BoardSerializer
from ports import GamePersistencePort
from piece import PieceSerializer

class FileGamePersistenceAdapter(GamePersistencePort):
    def __init__(self):
        self.path = f"{os.environ['HOME']}/python_chess"
        if f"dealer.json" not in os.listdir(self.path):
            with open(f"{self.path}/dealer.json", "w") as file:
                json.dump({"next_id": 1}, file)

    def get_board(self, game_id: int) -> "Board":
        if game_id == 0:
            return Board()
        board: Board
        while f"game_{game_id}.json" not in os.listdir(self.path):
            print(f"waiting game game_{game_id}.json creation at {os.listdir(self.path)}")
            time.sleep(1)
        with open(f"{self.path}/game_{game_id}.json", "r") as file:
            game = json.load(file)
            board = Board(
                [PieceSerializer.deserialize(piece) for piece in game["pieces"]], 
                game["movements"],
                game["white"],
                game["black"],
                game_id)
        return board

    def burn(self, board: "Board"):
        with open(f"{self.path}/game_{board.game_id}.json", "w") as file:
            game = {
                "pieces": [PieceSerializer.serialize(piece) for piece in board.pieces],
                "movements": board.movements,
                "white": board.white,
                "black": board.black,
            }
            json.dump(game, file, cls=BoardSerializer)

    def delete_game(self, board):
        os.remove(f"{self.path}/game_{board.game_id}.json")

    def next_id(self):
        with open(f"{self.path}/dealer.json", "r") as file:
            game = json.load(file)
            game["next_id"]+=1
        with open(f"{self.path}/dealer.json", "w") as file:
            json.dump(game,file)
        return game["next_id"]