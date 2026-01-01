import os
from board import Board
from ports import GameViewerPort
from piece import PieceSerializer, Color
from position import Position
from machine_core import PlayerStateHandler
from game_persistence import GamePersistencePort

class TextViewerAdapter(GameViewerPort, PlayerStateHandler):

    def __init__(self, persistence: GamePersistencePort):
        self.persistence = persistence

    def __call__(self, msg):
        self.display(self.persistence.get_board(msg.show()))


    def get_path(self) -> str:
        return f"{os.environ['HOME']}/python_chess"
    
    def display(self, board: Board) -> list[str]:
        white_representation = ["   a b c d e f g h"]
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
            white_representation.append(row.strip())
        black_representation = [white_representation[index][::-1] for index in range(len(white_representation)-1, -1, -1)]
        representation = white_representation if os.environ["BOARD"] == "white" else black_representation
        [print(line) for line in representation]
            