import asyncio
import os
import threading
from board import Board
from keyboard_input import KeyboardInputPort
from machine_core import Action, DealerState, MovementMessage, MovementState, DealerStateHandler, MovementStateHandler, MovementStateMachine, Players

from ports import GamePersistencePort, GameViewerPort

class CommandReader(DealerStateHandler):

    def __init__(self,keyboard: KeyboardInputPort):
        self.keyboard = keyboard
        
    def handle_command(self, msg):
        action = self.keyboard.read("What to do? play move, change game, start game, resign game or list games ").strip()
        msg.content = action
        msg.next_dealer_state = DealerState.FILTERING
        return super().handle_command(msg)

class CommandRouter(DealerStateHandler, MovementStateHandler):
    movement: list[str]

    def __init__(self, user: str, game_viewer: GameViewerPort, persistence: GamePersistencePort):
        self.game_viewer = game_viewer
        self.persistence = persistence
        self.user = user
        self.movement = ""
        self.action_map = {value.value: value.name for value in Action}

    
    def handle_command(self, msg):
        if len(msg.content.upper().split(" ")) > 2:
            command = "_".join(msg.content.upper().split(" ")[0:2])
            if command in self.action_map.keys():
                if self.action_map[command] == Action.PLAY_MOVE:
                    self.movement = msg.content.split(" ")[2]
                    msg.content = ""
                    msg.next_dealer_state = DealerState.READING
                    return msg
                else:
                    msg.action = self.action_map[command]
                    msg.next_dealer_state = DealerState.EXECUTING
                    return msg
        msg.content = ""
        msg.action = Action.PRINT_HELP
        msg.next_dealer_state = DealerState.EXECUTING
        return msg
    
    async def handle_movement(self, msg):
        if not self.movement:
            return msg
        board = self.persistence.get_board(msg.game)
        board.move(self.movement)
        self.persistence.burn(board)
        self.game_viewer.display(msg.game, self.user)
        msg.next_player_state = MovementState.THEIR_TURN
        return msg
    
class DealerDispatcher(DealerStateHandler):

    def __init__(self, persistence: GamePersistencePort, movement_machine: MovementStateMachine, user: str, keyboard: KeyboardInputPort):
        self.user = user
        self.movement_machine = movement_machine
        self.persistence = persistence
        self.keyboard = keyboard
        self.stop_event : threading.Event | None = None
        self.action_map = {
            Action.LIST_GAMES: self.list_games,
            Action.CHANGE_GAME: self.change_game,
            Action.RESIGN_GAME: self.resign_game,
            Action.START_GAME: self.start_game,
            Action.PRINT_HELP: self.print_help,
        }

    def handle_command(self, msg):
        self.action_map[msg.action]()
        msg.next_dealer_state = DealerState.READING
        return msg
    
    def print_help(self):
        pass
    
    def list_games(self):
        print("Available games:")
        for game in [file[5:-5] for file in os.listdir(self.path) if len([l for l in file if l == "_"]) == 1]:
            game_data = self.game_persistence_port.get_board(game)
            white = game_data.white
            black = game_data.black
            print(f"Game ID: {game}, White: {white}, Black: {black}")
    
    def resign_game(self):
        pass
    
    def change_game(self):
        self.list_games()
        game_id = int(self.keyboard.read("What game ID to do to ").strip())
        if self.stop_event:
            self.stop_event.set()

        board = self.persistence.get_board(game_id=game_id)
        right_turn = [
            len(board.movements) % 2 == 1 and board.black == self.user,
            len(board.movements) % 2 == 0 and board.white == self.user
        ]
        movement_message = MovementMessage(
            game=game_id,
            player_state=MovementState.YOUR_TURN if any(right_turn) else MovementState.THEIR_TURN
        )

        self.stop_event = threading.Event()
        def start_async_movement():
            asyncio.run(self.movement_machine.main_loop(movement_message, self.stop_event))
        threading.Thread(target=start_async_movement, daemon=True).start()
    
    def start_game(self):
        black = self.keyboard.read("Who are you challenging? ").strip()
        players = Players(white=self.user, black=black)
        board = Board(white=players.white, black=players.black, game_id=self.persistence.next_id())
        self.persistence.burn(board)

dealer_map = {
    DealerState.READING: CommandReader,
    DealerState.FILTERING: CommandRouter,
    DealerState.EXECUTING: DealerDispatcher
}