import json
import queue
from message_crossing import MessageCrossing
from ports import GamePersistencePort, GameViewerPort
from machine_core import MovementMessage, MovementState, MovementStateHandler

class OpponentInterface(MovementStateHandler):
    def __init__(self, persistence: GamePersistencePort, game_viewer: GameViewerPort, message_crossing: MessageCrossing):
        self.persistence = persistence
        self.game_viewer = game_viewer
        self.message_crossing = message_crossing
        self.message_crossing.listen()
    
    def handle_movement(self, msg) -> MovementMessage:    
        msg.next_player_state = MovementState.THEIR_TURN   
        if message:=self.message_crossing.pop():
            if message == "":
                return msg
            message = json.loads(message)
            board = self.persistence.get_board(msg.game)
            board.move(message["move"])
            self.game_viewer.display(msg.game)
            self.persistence.burn(board)
            msg.next_player_state = MovementState.YOUR_TURN
        return msg

class PlayerInterface(MovementStateHandler):

    def __init__(self, message_crossing: MessageCrossing, game_viewer: GameViewerPort, persistence: GamePersistencePort, movements: queue.Queue):
        self.game_viewer = game_viewer
        self.persistence = persistence
        self.movements = movements
        self.message_crossing = message_crossing

    def handle_movement(self, msg):
        board = self.persistence.get_board(msg.game)
        try:
            board.move(self.movements.get_nowait())
        except queue.Empty:
            msg.next_player_state = MovementState.YOUR_TURN
            return msg
        self.persistence.burn(board)
        self.game_viewer.display(msg.game)
        self.send_message(msg)
        msg.next_player_state = MovementState.THEIR_TURN
        return msg
    
    def send_message(self, message: MovementMessage) -> None:    
        self.message_crossing.send(message.as_json_string())