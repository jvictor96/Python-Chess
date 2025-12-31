from abc import ABC, abstractmethod
import json
import time
from movement import Movement
from piece import Color, Piece, piece_map
from position import Position
import os

class GameViewerPort(ABC):
    
    @abstractmethod
    def display():
        pass

class BoardSerializer(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Position):
            return obj.__repr__()
        if isinstance(obj, Movement):
            return obj.__repr__()
        return json.JSONEncoder.default(self, obj)

class ChessDaemon:

    def __init__(self, game_persistence_adapter: "GamePersistencePort", game_viewer_adapter: GameViewerPort):
        self.game_persistence_adapter = game_persistence_adapter
        self.game_viewer_adapter = game_viewer_adapter
        
    def main_loop(self):
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
                        board = Board(white=white, black=black)
                        self.game_persistence_adapter.burn(board)
                        self.reprint_input(
                            game_id=control_fields["next_id"])
                        self.game_viewer_adapter.display(board)
                        control_fields["next_id"] += 1
                    if control_fields["end_game"] > 0:
                        control_fields["games"].remove(control_fields["end_game"])
                        control_fields["end_game"] = 0
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
                board = self.game_persistence_adapter.get_board(game).move(game_control_fields["move"])
                self.game_persistence_adapter.burn(board)
                self.reprint_input_output(game, board, "" if board.legal else "Illegal move")

    def reprint_input(self, game_id: int, error: str = ""):
        game_control_fields = json.loads("{}")
        game_control_fields["move"] = ""
        game_control_fields["error"] = error
        with open(f"{self.path}/game_{game_id}_input.json", "w") as input_file:
            json.dump(game_control_fields, input_file)

class Board:
    movements: list[Movement]
    pieces: list[Piece]
    positions: dict[Position, Piece]
    legal: bool | None
    white: str
    black: str
    game_id: int

    def __init__(self, pieces: list[Piece] | None = None, movements = None, white: str = None, black: str = None, game_id: int = None):
        if pieces == None:
            pieces = []
            for i in range(1,9):
                pieces.append(piece_map["P"](Color.WHITE, Position(i, 2)))
                pieces.append(piece_map["P"](Color.BLACK, Position(i, 7)))
            pieces.append(piece_map["R"](Color.WHITE, Position(1,1)))
            pieces.append(piece_map["N"](Color.WHITE, Position(2,1)))
            pieces.append(piece_map["B"](Color.WHITE, Position(3,1)))
            pieces.append(piece_map["Q"](Color.WHITE, Position(4,1)))
            pieces.append(piece_map["K"](Color.WHITE, Position(5,1)))
            pieces.append(piece_map["B"](Color.WHITE, Position(6,1)))
            pieces.append(piece_map["N"](Color.WHITE, Position(7,1)))
            pieces.append(piece_map["R"](Color.WHITE, Position(8,1)))
            pieces.append(piece_map["R"](Color.BLACK, Position(1,8)))
            pieces.append(piece_map["N"](Color.BLACK, Position(2,8)))
            pieces.append(piece_map["B"](Color.BLACK, Position(3,8)))
            pieces.append(piece_map["Q"](Color.BLACK, Position(4,8)))
            pieces.append(piece_map["K"](Color.BLACK, Position(5,8)))
            pieces.append(piece_map["B"](Color.BLACK, Position(6,8)))
            pieces.append(piece_map["N"](Color.BLACK, Position(7,8)))
            pieces.append(piece_map["R"](Color.BLACK, Position(8,8)))
        self.pieces: list[Piece] = pieces
        self.movements: list[Movement] = movements if movements != None else []
        self.positions = {piece.position: piece for piece in pieces}
        self.black = black
        self.white = white
        self.game_id = game_id

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

    def move(self: "Board", movement: str):
        movement: Movement = Movement.from_string(movement, self.positions)
        piece = self.positions.get(movement.start_pos)
        right_turn = any([
            piece.color == Color.WHITE and len(self.movements) % 2 == 0,
            piece.color == Color.BLACK and len(self.movements) % 2 == 1])
        self.legal = all([movement.is_valid(), right_turn])
        return Board.update_state(self, movement) if self.legal else self

class GamePersistencePort(ABC):
    
    @abstractmethod
    def get_board(self, game_id: int) -> Board:
        pass
        
    @abstractmethod
    def burn(self, board: Board):
        pass