import json
import os
from pathlib import Path
from ports import GamePersistencePort
from keyboard_input import KeyboardInput


class DaemonController():

    def __init__(self, keyboard: KeyboardInput, game_persistence_port: GamePersistencePort):
        self.path = f"{os.environ['HOME']}/python_chess"
        self.keyboard = keyboard
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
        with open(f"{self.path}/daemon.json", "r+") as daemon:
            control_fields = json.load(daemon)
            control_fields["new_game"]["white"] = white
            control_fields["new_game"]["black"] = black
            game_id = control_fields["next_id"]
            daemon.seek(0)
            daemon.truncate()
            json.dump(control_fields, daemon)
        os.environ["GAME"] = str(game_id)
        os.environ["PLAYER"] = white
        os.environ["BOARD"] = "white"
        os.system(f"screen -c {self.path}/screenrc")

    def join_game(self):
        player = self.keyboard.read("Who are you? ").strip()
        with open(f"{self.path}/daemon.json", "r") as daemon:
            control_fields = json.load(daemon)
            print("Available games:")
            for game in control_fields["games"]:
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