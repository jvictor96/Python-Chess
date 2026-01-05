from ports import GamePersistencePort
from board import Board
from machine_core import DealerStateHandler, MovementStateHandler

class Dealer(DealerStateHandler):
    def __init__(self, game_persistence_adapter: GamePersistencePort):
        self.game_persistence_adapter = game_persistence_adapter

    def __call__(self, msg):
        if new_game:=msg.consume_new_game():
            board = Board(white=new_game.white, black=new_game.black, game_id=self.game_persistence_adapter.next_id())
            self.game_persistence_adapter.burn(board)
        if end_game:=msg.consume_end_game():
            self.game_persistence_adapter.delete_game(end_game)
        msg.free()
        return msg

class Moderator(MovementStateHandler):
    def __init__(self, game_persistence_adapter: GamePersistencePort):
        self.game_persistence_adapter = game_persistence_adapter

    def __call__(self, msg):
        board = self.game_persistence_adapter.get_board(msg.game)
        board.move(msg.move)
        self.game_persistence_adapter.burn(board)
        msg.move = ""
        msg.error = "" if board.legal else "Illegal movement"
        msg.change_turn() if board.legal else msg.return_turn()
        
class DealerCleanUp(DealerStateHandler):
    def __call__(self, msg):
        msg.free()