import json
import os

from keyboard_input import KeyboardInput


class DaemonController():

    def __init__(self, keyboard: KeyboardInput):
        self.path = f"{os.environ['HOME']}/python_chess"
        self.keyboard = keyboard

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
        os.system("screen -c screenrc")

    def join_game(self):
        player = self.keyboard.read("Who are you? ").strip()
        with open(f"{self.path}/daemon.json", "r") as daemon:
            control_fields = json.load(daemon)
            print("Available games:")
            for game in control_fields["games"]:
                with open(f"{self.path}/game_{game}.json", "r") as game_file:
                    game_data = json.load(game_file)
                    white = game_data["white"]
                    black = game_data["black"]
                    if player == white or player == black:
                        print(f"Game ID: {game}, White: {white}, Black: {black}")
        game_id = self.keyboard.read("Enter the Game ID you want to join: ").strip()
        os.environ["GAME"] = game_id
        os.environ["PLAYER"] = player
        os.environ["BOARD"] = "white" if player == white else "black"
        os.system("screen -c screenrc")
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