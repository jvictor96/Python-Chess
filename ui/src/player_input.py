import os
from machine_core import PlayerStateHandler, PlayerState
from ports import GamePersistencePort
from keyboard_input import KeyboardInputPort

class CrudeShellPlayerInputUI(PlayerStateHandler):

    def __init__(self, persistence: GamePersistencePort, keyboard: KeyboardInputPort):
        self.keyboard = keyboard
        self.persistence = persistence

    def __call__(self, msg):
        os.system('clear')
        board = self.persistence.get_board(msg.game)
        print(f"Game between {board.white} (White) and {board.black} (Black). You are playing as {os.environ['BOARD']}.")
        right_turn = [
            msg.player_state == PlayerState.BLACK_TURN and os.environ['BOARD'] == "black",
            msg.player_state == PlayerState.WHITE_TURN and os.environ['BOARD'] == "white"
        ]
        if not any(right_turn):
            print("Waiting for opponent's move...")
            return msg
        print("It's your turn.")
        movement = self.keyboard.read("Enter your move (e.g., e2e4): ").strip()
        msg.play(movement)
        return msg