import os
from machine_core import MovementState, MovementMessage
from ports import GamePersistencePort
from keyboard_input import KeyboardInputPort
from opponent_interface import OpponentInterface

class ShellMovementInputUI():

    def __init__(self, persistence: GamePersistencePort, keyboard: KeyboardInputPort, opponent_interface: OpponentInterface):
        self.keyboard = keyboard
        self.persistence = persistence
        self.opponent_interface = opponent_interface

    def play(self, msg: MovementMessage, user: str):
        board = self.persistence.get_board(msg.game)
        color = "white" if user == board.white else "black"
        print(f"Game between {board.white} (White) and {board.black} (Black). You are playing as {color}.")
        right_turn = [
            msg.player_state == MovementState.BLACK_TURN and color == "black",
            msg.player_state == MovementState.WHITE_TURN and color == "white"
        ]

        if not any(right_turn):
            print("Waiting for opponent's move...")
            msg.pass_the_turn()
            return msg
        
        print("It's your turn.")
        movement = self.keyboard.read("Enter your move (e.g., e2e4): ").strip()
        msg.play(movement)
        self.opponent_interface.send_message(msg)
        return msg