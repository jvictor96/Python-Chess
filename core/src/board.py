import json
from movement import Movement
from piece import Color, Piece, piece_map, King
from position import Position

class BoardSerializer(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Position):
            return obj.__repr__()
        if isinstance(obj, Movement):
            return obj.__repr__()
        return json.JSONEncoder.default(self, obj)

class Board:
    movements: list[Movement]
    pieces: list[Piece]
    positions: dict[Position, Piece]
    legal: bool | None
    white: str
    black: str
    winner: str
    game_id: int

    def clone(self):
        pieces = []
        movements = []
        for piece in self.pieces:
            pos = Position(piece.position.x, piece.position.y)
            pieces.append(type(piece)(piece.color, pos))
        for movement in self.movements:
            move = Movement.from_string(repr(movement), self.positions)
            movements.append(move)
        return Board(pieces = pieces, movements=movements, white=self.white, black=self.black, game_id=self.game_id)

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
        self.winner = ""
        self.game_id = game_id

    def get_king(self, color: Color) -> King:
        return next(piece for piece in self.pieces if piece.color == color and piece_map[type(piece)] == "K")
    
    def is_color_in_check(self, color):
        king = self.get_king(color)
        catch_king_candidates:list[Movement] = [Movement.from_string(f"{piece.position}{king.position}", self.positions) for piece in self.pieces if piece.color != color]
        return any([movement.is_valid() for movement in catch_king_candidates])

    def is_color_in_check_mate(self, color):
        positions_and_destinations = [(piece.position, piece.get_all_possible_destinations()) for piece in self.pieces if piece.color == color]
        movement_candidates = [ [Movement(piece[0], destination, self.positions) for destination in piece[1]] for piece in positions_and_destinations]
        for piece in movement_candidates:
            for movement in piece:
                board = self.clone()
                board.move(repr(movement))
                if board.legal:
                    print(movement)
                    return False
        return True


    def update_positions(self: "Board", movement: str, bypass_movements_append: bool = False) -> "Board":
        movement: Movement = Movement.from_string(movement, self.positions)
        piece = self.positions.get(movement.start_pos)
        piece.position = movement.end_pos
        if not bypass_movements_append:
            self.movements.append(movement)
        self.positions.pop(movement.start_pos)
        self.positions[movement.end_pos] = piece
        self.pieces = [piece for pos, piece in self.positions.items()]
        return self

    def bypass_validation_move(self, movement: str) -> "Board":
        movement = Movement.from_string(movement, self.positions)
        self.update_positions(repr(movement), bypass_movements_append=True)

    def move(self: "Board", movement: str):
        movement: Movement = Movement.from_string(movement, self.positions)
        piece = self.positions.get(movement.start_pos)
        self.legal = movement.is_valid()
        if not self.legal:
            return
        right_turn = any([
            piece.color == Color.WHITE and len(self.movements) % 2 == 0,
            piece.color == Color.BLACK and len(self.movements) % 2 == 1])
        self.legal = right_turn
        if not self.legal:
            return
        board = self.clone()
        board.update_positions(repr(movement))
        if board.is_color_in_check(piece.color):
            self.legal = False
            return
        self.update_positions(repr(movement))
        board = self.clone()
        if (board.is_color_in_check({Color.BLACK: Color.WHITE, Color.WHITE: Color.BLACK}[piece.color]) and
            board.is_color_in_check_mate({Color.BLACK: Color.WHITE, Color.WHITE: Color.BLACK}[piece.color])):
            self.winner = {Color.BLACK: self.black, Color.WHITE: self.white}[piece.color]
            print("checkmate")
