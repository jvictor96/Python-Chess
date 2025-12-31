import json
import os
import time

path = f"{os.environ["HOME"]}/python_chess"

while True:
    time.sleep(2)
    color = ""
    len_movements = -1
    with open(f"{path}/game_{os.environ['GAME']}.json", "r+") as game_file:
        game_data = json.load(game_file)
        white = game_data["white"]
        black = game_data["black"]
        print(f"Game between {white} (White) and {black} (Black). You are playing as {os.environ['BOARD']}.")
        right_turn = [
            len(game_data["movements"]) % 2 == 0 and os.environ['BOARD'] == "white",
            len(game_data["movements"]) % 2 == 1 and os.environ['BOARD'] == "black"
        ]
        if any(right_turn):
            print("It's your turn.")
            movement = input("Enter your move (e.g., e2e4): ").strip()
            with open(f"{path}/game_{os.environ['GAME']}_input.json", "r+") as input_file:
                game_control_fields = json.load(input_file)
                game_control_fields["move"] = movement
                input_file.seek(0)
                input_file.truncate()
                json.dump(game_control_fields, input_file)
            game_file.seek(0)
            game_file.truncate()
            game_data["state"] = "WAITING"
            json.dump(game_data, game_file)
        else:
            print("Waiting for opponent's move...")