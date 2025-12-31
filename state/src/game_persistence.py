import json
import os
from board import Board, BoardSerializer
from ports import GamePersistencePort, GameViewerPort
from piece import PieceSerializer, Color
from position import Position

class TextViewerAdapter(GameViewerPort):

    def get_path(self) -> str:
        return f"{os.environ['HOME']}/python_chess"
    
    def display(self, board: Board) -> list[str]:
        path = board
        board_representation = ["   a b c d e f g h"]
        for y in range(8, 0, -1):
            row = f"{y}  "
            for x in range(1, 9):
                pos = Position(x, y)
                piece = board.positions.get(pos)
                if piece:
                    piece_symbol = PieceSerializer.serialize(piece)["piece"].upper() if piece.color == Color.WHITE else PieceSerializer.serialize(piece)["piece"].lower()
                    row += piece_symbol + " "
                else:
                    row += ". "
            board_representation.append(row.strip())
        with open(f"{self.get_path()}/game_{board.game_id}_white.json", "w") as output_file:
            [output_file.write(line + "\n") for line in board_representation]
        with open(f"{self.get_path()}/game_{board.game_id}_black.json", "w") as output_file:
            [output_file.write(board_representation[index][::-1] + "\n") for index in range(len(board_representation)-1, -1, -1)]

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