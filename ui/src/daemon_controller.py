import json
import os
from pathlib import Path
from ports import GamePersistencePort
from keyboard_input import KeyboardInput
from machine_core import DaemonState, DaemonStateMachine, DaemonMessage, NewGame


class DaemonController():

    def __init__(self, keyboard: KeyboardInput, game_persistence_port: GamePersistencePort, state_machine: DaemonStateMachine):
        self.path = f"{os.environ['HOME']}/python_chess"
        self.keyboard = keyboard
        self.state_machine = state_machine
        self.game_persistence_port = game_persistence_port
        self.print_screenrc()
        

    def print_screenrc(self):
        try:
            with open(f"{self.path}/screenrc", "r+") as rc:
                pass
        except Exception as e:
            script_dir = Path(__file__).parent.resolve()
            with open(f"{self.path}/screenrc", "x+") as rc:
                rc.write("split -v\n")
                rc.write("screen -t board 1 watch cat ${HOME}/python_chess/game_${GAME}_${BOARD}.json\n")
                rc.write("select window2\n")
                rc.write("focus\n")
                rc.write(f"screen -t bash 2 python {script_dir}/player_input.py")

    def new_game(self):
        game_id = 0
        white = self.keyboard.read("Who are you? ").strip()
        black = self.keyboard.read("Who are you challenging? ").strip()
        msg = DaemonMessage(new_game=NewGame(white=white, black=black), 
                      next_id=self.state_machine.message.next_id,
                      end_game=0,
                      daemon_state=DaemonState.COMMAND_SENT)
        self.state_machine.post_task(msg)
        os.environ["GAME"] = str(game_id)
        os.environ["PLAYER"] = white
        os.environ["BOARD"] = "white"
        os.system(f"screen -c {self.path}/screenrc")

    def join_game(self):
        player = self.keyboard.read("Who are you? ").strip()
        print("Available games:")
        for game in [file[5:-5] for file in os.listdir("python_chess") if len([l for l in file if l == "_"]) == 1]:
            game_data = self.game_persistence_port.get_board(game)
            white = game_data.white
            black = game_data.black
            if player == white or player == black:
                print(f"Game ID: {game}, White: {white}, Black: {black}")
        game_id = self.keyboard.read("Enter the Game ID you want to join: ").strip()
        os.environ["GAME"] = game_id
        os.environ["PLAYER"] = player
        os.environ["BOARD"] = "white" if player == white else "black"
        os.system(f"screen -c {self.path}/screenrc")
        exit(0)

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