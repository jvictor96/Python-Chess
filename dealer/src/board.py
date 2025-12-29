import json
import time
from movement import Movement
from piece import Color, Piece, PieceSerializer, piece_map
from position import Position
import os

    
class BoardSerializer(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Position):
            return obj.__repr__()
        if isinstance(obj, Movement):
            return obj.__repr__()
        return json.JSONEncoder.default(self, obj)
    
class ChessDaemon:
    def main_loop(self):
        self.path = BoardIO.get_path()
        try:
            os.mkdir(self.path)
        except Exception as e:
            pass
        while True:
            time.sleep(0.1)
            try:
                with open(f"{self.path}/daemon.json", "r+") as daemon:
                    control_fields = json.load(daemon)
                    for game in control_fields["games"]:
                        self.update_game(game)
                    if control_fields["new_game"]["white"] != "":
                        white = control_fields["new_game"]["white"]
                        black = control_fields["new_game"]["black"]
                        control_fields["new_game"] = { "white": "", "black": "" }
                        control_fields["games"].append(control_fields["next_id"])
                        board = BoardIO.get_board(0)
                        board.white = white
                        board.black = black
                        BoardIO.save_board(
                            board = board,
                            game_id=control_fields["next_id"])
                        self.reprint_input_output(
                            game_id=control_fields["next_id"],
                            board=BoardIO.get_board(0))
                        control_fields["next_id"] += 1
                    if control_fields["end_game"] > 0:
                        control_fields["games"].remove(control_fields["end_game"])
                        control_fields["end_g.txtame"] = 0
                    daemon.seek(0)
                    daemon.truncate()
                    json.dump(control_fields, daemon)
            except FileNotFoundError as e:
                with open(f"{self.path}/daemon.json", "x+") as daemon:
                    if len(daemon.readlines()) == 0:
                        control_fields = {
                            "games": [],
                            "new_game": { "white": "", "black": "" },
                            "next_id": 1,
                            "end_game": 0
                        }
                        daemon.seek(0)
                        daemon.truncate()
                        json.dump(control_fields, daemon)

    def update_game(self, game: int):
        with open(f"{self.path}/game_{game}_input.json", "r+") as game_file:
            game_control_fields = json.load(game_file)
            if game_control_fields["move"] != "":
                board = BoardIO.get_board(game)
                board = board.move(game_control_fields["move"])
                BoardIO.save_board(board, game)
                self.reprint_input_output(game, board, "" if board.legal else "Illegal move")

    def reprint_input_output(self, game_id: int, board: "Board", error: str = ""):
        display = BoardIO.display(board)
        with open(f"{self.path}/game_{game_id}_white.json", "w") as output_file:
            [output_file.write(line + "\n") for line in display]
        with open(f"{self.path}/game_{game_id}_black.json", "w") as output_file:
            [output_file.write(display[index][::-1] + "\n") for index in range(len(display)-1, -1, -1)]
        game_control_fields = json.loads("{}")
        game_control_fields["move"] = ""
        game_control_fields["error"] = error
        with open(f"{self.path}/game_{game_id}_input.json", "w") as input_file:
            json.dump(game_control_fields, input_file)

class BoardIO:
    def display(self) -> list[str]:
        board_representation = ["   a b c d e f g h"]
        for y in range(8, 0, -1):
            row = f"{y}  "
            for x in range(1, 9):
                pos = Position(x, y)
                piece = self.positions.get(pos)
                if piece:
                    piece_symbol = PieceSerializer.serialize(piece)["piece"].upper() if piece.color == Color.WHITE else PieceSerializer.serialize(piece)["piece"].lower()
                    row += piece_symbol + " "
                else:
                    row += ". "
            board_representation.append(row.strip())
        return board_representation

    @staticmethod
    def get_new_board() -> "Board":
        board: Board
        with open(f"res/new_game.json", "r") as file:
            game = json.load(file)
            board = Board(
                [PieceSerializer.deserialize(piece) for piece in game["pieces"]], game["movements"])
            board.white = game["white"]
            board.black = game["black"]
        return board

    @staticmethod
    def get_path() -> str:
        return f"{os.environ["HOME"]}/python_chess"

    @staticmethod
    def get_board(game_id: int) -> "Board":
        if game_id == 0:
            return BoardIO.get_new_board()
        board: Board
        with open(f"{BoardIO.get_path()}/game_{game_id}.json", "r") as file:
            game = json.load(file)
            board = Board(
                [PieceSerializer.deserialize(piece) for piece in game["pieces"]], game["movements"])
            board.white = game["white"]
            board.black = game["black"]
        return board

    @staticmethod
    def save_board(board: "Board", game_id: int):
        with open(f"{BoardIO.get_path()}/game_{game_id}.json", "w") as file:
            game = {
                "pieces": [PieceSerializer.serialize(piece) for piece in board.pieces],
                "movements": board.movements,
                "white": board.white,
                "black": board.black,
                "state": "FREE"
            }
            json.dump(game, file, cls=BoardSerializer)

class Board:
    movements: list[Movement]
    pieces: list[Piece]
    positions: dict[Position, Piece]
    legal: bool
    white: str
    black: str

    def __init__(self, pieces: list[Piece] = None, movements=None):
        self.pieces: list[Piece] = pieces
        self.movements: list[Movement] = movements
        self.positions = {piece.position: piece for piece in pieces}

    def get_king(self, color: Color) -> Piece:
        return next(piece for piece in self.pieces if piece.color == color and piece_map[type(piece)] == "K")

    @staticmethod
    def update_state(board: "Board", movement: Movement, bypass_movements_append: bool = False) -> "Board":
        piece = board.positions.get(movement.start_pos)
        piece.position = movement.end_pos
        if not bypass_movements_append:
            board.movements.append(movement)
        board.positions.pop(movement.start_pos)
        board.positions[movement.end_pos] = piece
        board.pieces = [piece for pos, piece in board.positions.items()]
        return board

    def bypass_validation_move(self, movement: str) -> "Board":
        movement = Movement.from_string(movement, self.positions)
        return Board.update_state(self, movement, bypass_movements_append=True)

    def move(board: "Board", movement: str):
        movement: Movement = Movement.from_string(movement, board.positions)
        piece = board.positions.get(movement.start_pos)
        right_turn = any([
            piece.color == Color.WHITE and len(board.movements) % 2 == 0,
            piece.color == Color.BLACK and len(board.movements) % 2 == 1])
        board.legal = all([movement.is_valid(), right_turn])
        return Board.update_state(board, movement) if board.legal else board