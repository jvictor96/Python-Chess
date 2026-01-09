from abc import ABC, abstractmethod
from message_crossing import FileMessageCrossing, MessageCrossing
from ports import GamePersistencePort, GameViewerPort
from machine_core import MovementMessage, MovementState, MovementStateHandler

class OpponentInterface(MovementStateHandler):
    def __init__(self, persistence: GamePersistencePort, game_viewer: GameViewerPort, message_crossing: MessageCrossing):
        self.persistence = persistence
        self.game_viewer = game_viewer
        self.message_crossing = message_crossing
    
    def handle_movement(self, msg) -> MovementMessage:    
        msg.next_player_state = MovementState.THEIR_TURN   
        if message:=self.message_crossing.pop():
            board = self.persistence.get_board(msg.game)
            board.move(message["move"])
            self.game_viewer.display(msg.game)
            self.persistence.burn(board)
            msg.next_player_state = MovementState.YOUR_TURN
        return msg

class PlayerInterface(MovementStateHandler):

    def __init__(self, message_crossing: MessageCrossing, game_viewer: GameViewerPort, persistence: GamePersistencePort, movements: list[str]):
        self.game_viewer = game_viewer
        self.persistence = persistence
        self.movements = movements
        self.message_crossing = message_crossing

    def handle_movement(self, msg):
        if not self.movements:
            msg.next_player_state = MovementState.YOUR_TURN
            return msg
        board = self.persistence.get_board(msg.game)
        board.move(self.movements.pop(0))
        self.persistence.burn(board)
        self.game_viewer.display(msg.game)
        self.send_message(msg)
        msg.next_player_state = MovementState.THEIR_TURN
        return msg
    
    def send_message(self, message: MovementMessage) -> None:    
        self.message_crossing.send(message.as_json_string())