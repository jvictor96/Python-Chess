from ports import GamePersistencePort
from board import Board
from machine_core import DaemonStateHandler, PlayerStateHandler, DaemonState, PlayerState

class ChessDaemon(DaemonStateHandler):
    def __init__(self, game_persistence_adapter: GamePersistencePort):
        self.game_persistence_adapter = game_persistence_adapter

    def __call__(self, msg):
        if msg.new_game != None:
            white = msg.new_game.white
            black = msg.new_game.black
            board = Board(white=white, black=black, game_id=msg.next_id)
            msg.next_id = msg.next_id + 1
            msg.new_game = None
            self.game_persistence_adapter.burn(board)
        if msg.end_game > 0:
            self.game_persistence_adapter.delete_game(msg.end_game)
            msg.end_game = 0
        msg.daemon_state = DaemonState.DIGESTED
        return msg

class ChessDealer(PlayerStateHandler):
    def __init__(self, game_persistence_adapter: GamePersistencePort):
        self.game_persistence_adapter = game_persistence_adapter

    def __call__(self, msg):
        board = self.game_persistence_adapter.get_board(msg.game)
        board.move(msg.move)
        self.game_persistence_adapter.burn(board)
        msg.move = ""
        msg.error = "Illegal movement"
        msg.player_state = PlayerState.PLAYED

class DaemonCleanUp(DaemonStateHandler):
    def __call__(self, msg):
        msg.daemon_state = DaemonStateHandler.IDLE