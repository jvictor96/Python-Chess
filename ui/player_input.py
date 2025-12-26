import json
import os

while True:
    movement = input("Enter your move (e.g., e2e4): ").strip()
    with open(f"../app/games/game_{os.environ['GAME']}_input.txt", "r+") as game_file:
        game_control_fields = json.load(game_file)
        game_control_fields["move"] = movement
        game_file.seek(0)
        game_file.truncate()
        json.dump(game_control_fields, game_file)