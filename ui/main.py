import json
import os

def read_action():
    return input("1 for new game, 2 for listing games, 3 for joining game, 4 exit ").strip()

def new_game():
    game_id = 0
    white = input("Who are you? ").strip()
    black = input("Who are you challenging? ").strip()
    with open("../app/daemon.txt", "r+") as daemon:
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

def list_games():
    print("Listing games is not implemented yet.")
    exit(0)

def join_game():
    player = input("Who are you? ").strip()
    with open("../app/daemon.txt", "r") as daemon:
        control_fields = json.load(daemon)
        print("Available games:")
        for game in control_fields["games"]:
            with open(f"../app/games/game_{game}.txt", "r") as game_file:
                game_data = json.load(game_file)
                white = game_data["white"]
                black = game_data["black"]
                if player == white or player == black:
                    print(f"Game ID: {game}, White: {white}, Black: {black}")
    game_id = input("Enter the Game ID you want to join: ").strip()
    os.environ["GAME"] = game_id
    os.environ["PLAYER"] = player
    os.environ["BOARD"] = "white" if player == white else "black"
    os.system("screen -c screenrc")
    exit(0)

def exit_program():
    print("Exiting program.")
    exit(0)

action_map = {
    "1": new_game,
    "2": list_games,
    "3": join_game,
    "4": exit_program
}

action_map.get(read_action(), exit_program)()