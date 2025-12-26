import json
import os

def read_action():
    return input("1 for new game, 2 for list games, 3 for resume game, 4 exit ").strip()

def new_game():
    game_id = 0
    with open("../app/daemon.txt", "r+") as daemon:
        control_fields = json.load(daemon)
        control_fields["new_game"] = True
        game_id = control_fields["next_id"]
        daemon.seek(0)
        daemon.truncate()
        json.dump(control_fields, daemon)
    os.environ["GAME"] = str(game_id)
    os.system("screen -c screenrc")

def list_games():
    print("Listing games is not implemented yet.")
    exit(0)

def resume_game():
    print("Resuming game is not implemented yet.")
    exit(0)

def exit_program():
    print("Exiting program.")
    exit(0)

action_map = {
    "1": new_game,
    "2": list_games,
    "3": resume_game,
    "4": exit_program
}

action_map.get(read_action(), exit_program)()