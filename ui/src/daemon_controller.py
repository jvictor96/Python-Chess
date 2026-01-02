import os
from ports import GamePersistencePort
from keyboard_input import KeyboardInputPort
from machine_core import DealerState, DealerMessage, Players, MovementMessage
from machine_core import MovementState
from dealer_interface import DealerInterface
from human_interface import HumanInterfacePort


class DealerInput():

    def __init__(self, 
                 keyboard: KeyboardInputPort, 
                 game_persistence_port: GamePersistencePort, 
                 dealer_interface: DealerInterface,
                 human_interface_port: HumanInterfacePort,
                 user: str):
        self.path = f"{os.environ['HOME']}/python_chess"
        self.keyboard = keyboard
        self.user = user
        self.human_interface_port = human_interface_port
        self.dealer_interface = dealer_interface
        self.game_persistence_port = game_persistence_port
        

    def new_game(self):
        black = self.keyboard.read("Who are you challenging? ").strip()
        players = Players(white=self.user, black=black)
        msg = DealerMessage(new_game=players, 
                      end_game=0,
                      dealer_state=DealerState.COMMAND_SENT)
        self.dealer_interface.send_message(msg)
        msg = MovementMessage(game=self.game_persistence_port.next_id(), player_state=MovementState.WHITE_TURN)
        self.human_interface_port.play(msg)

    def join_game(self):
        print("Available games:")
        for game in [file[5:-5] for file in os.listdir(self.path) if len([l for l in file if l == "_"]) == 1]:
            game_data = self.game_persistence_port.get_board(game)
            white = game_data.white
            black = game_data.black
            print(f"Game ID: {game}, White: {white}, Black: {black}")
        game_id = self.keyboard.read("Enter the Game ID you want to join: ").strip()
        msg = MovementMessage(game=game_id, player_state=MovementState.BLACK_TURN if len(game_data.movements) % 2 else MovementState.WHITE_TURN)
        self.human_interface_port.play(msg)

    def exit_program(self):
        print("Exiting program.")
        exit(0)

    def read_action(self):
        action = self.keyboard.read("1 for new game, 2 for joining a game, 3 exit ").strip()

        action_map = {
            "1": self.new_game,
            "2": self.join_game,
            "3": self.exit_program
        }

        action_map.get(action, self.exit_program)()