import json
import os
from board import Board, BoardSerializer
from ports import GamePersistencePort
from piece import PieceSerializer

class FileGamePersistenceAdapter(GamePersistencePort):

    def get_path(self) -> str:
        return f"{os.environ['HOME']}/python_chess"

    def get_board(self, game_id: int) -> "Board":
        if game_id == 0:
            return Board()
        board: Board
        with open(f"{self.get_path()}/game_{game_id}.json", "r") as file:
            game = json.load(file)
            board = Board(
                [PieceSerializer.deserialize(piece) for piece in game["pieces"]], 
                game["movements"],
                game["white"],
                game["black"],
                game_id)
        return board

    def burn(self, board: "Board"):
        with open(f"{self.get_path()}/game_{board.game_id}.json", "w") as file:
            game = {
                "pieces": [PieceSerializer.serialize(piece) for piece in board.pieces],
                "movements": board.movements,
                "white": board.white,
                "black": board.black,
            }
            json.dump(game, file, cls=BoardSerializer)