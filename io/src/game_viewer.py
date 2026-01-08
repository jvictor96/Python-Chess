import os
from board import Board
from ports import GameViewerPort
from piece import PieceSerializer, Color
from position import Position
from game_persistence import GamePersistencePort

class TextViewerAdapter(GameViewerPort):

    def __init__(self, persistence: GamePersistencePort, user: str):
        self.persistence = persistence
        self.user = user
    
    def display(self, game_id: int) -> list[str]:
        board = self.persistence.get_board(game_id)
        os.system('clear')
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
        color = "white" if self.user == board.white else "black"
        right_turn = [
            len(board.movements) % 2 == 1 and board.black == self.user,
            len(board.movements) % 2 == 0 and board.white == self.user
        ]
        turn = "your" if any(right_turn) else "their"
        black_representation = [white_representation[index][::-1] for index in range(len(white_representation)-1, -1, -1)]
        representation = white_representation if color == "white" else black_representation
        print(f"game id: {game_id}")
        print(f"you are playing with the {color} pieces")
        print(f"it's {turn} turn")
        [print(line) for line in representation]
            