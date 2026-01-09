import asyncio
import queue
import threading
from board import Board
from keyboard_input import KeyboardInputPort
from machine_core import Action, DealerState, MovementMessage, MovementState, DealerStateHandler, MovementStateMachine, Players

from message_crossing import MessageCrossingFactory
from opponent_interface import OpponentInterface, PlayerInterface
from ports import GamePersistencePort, GameViewerPort

class CommandReader(DealerStateHandler):

    def __init__(self, keyboard: KeyboardInputPort):
        self.keyboard = keyboard
        
    def handle_command(self, msg):
        action = self.keyboard.read("What to do? play move, change game, start game, resign game or list games ").strip()
        msg.content = action
        msg.next_dealer_state = DealerState.FILTERING
        return msg

class CommandRouter(DealerStateHandler):
    movements: queue.Queue

    def __init__(self, user: str, game_viewer: GameViewerPort, persistence: GamePersistencePort, movements: queue.Queue):
        self.game_viewer = game_viewer
        self.persistence = persistence
        self.user = user
        self.movements = movements
        self.action_map = {value.value: value for value in Action}
        self.short_map = {f"{key[0]}{key[key.find("_")+1]}": value for key, value in self.action_map.items()}

    
    def handle_command(self, msg):
        if len(msg.content.upper().split(" ")) > 1:
            command = "_".join(msg.content.upper().split(" ")[0:2])
            if command in self.action_map.keys():
                if self.action_map[command] == Action.PLAY_MOVE:
                    self.movements.put(msg.content.split(" ")[2])
                    msg.content = ""
                    msg.next_dealer_state = DealerState.READING
                    return msg
                else:
                    msg.action = self.action_map[command]
                    msg.next_dealer_state = DealerState.EXECUTING
                    return msg
        command = msg.content.upper().split(" ")[0]
        if command in self.short_map:
            if self.short_map[command] == Action.PLAY_MOVE:
                self.movement = msg.content.split(" ")[1]
                msg.content = ""
                msg.next_dealer_state = DealerState.READING
                return msg
            else:
                msg.action = self.short_map[command]
                msg.next_dealer_state = DealerState.EXECUTING
                return msg
        msg.content = ""
        msg.action = Action.PRINT_HELP
        msg.next_dealer_state = DealerState.EXECUTING
        return msg
       
class DealerDispatcher(DealerStateHandler):

    def __init__(self, movements: list[str], persistence: GamePersistencePort, game_viewer: GameViewerPort, message_crossing_factory: MessageCrossingFactory, user: str, keyboard: KeyboardInputPort):
        self.user = user
        self.persistence = persistence
        self.movements = movements
        self.message_crossing_factory = message_crossing_factory
        self.keyboard = keyboard
        self.game_viewer = game_viewer
        self.movement_machine = None
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
        for game in self.persistence.list_games():
            game_data = self.persistence.get_board(game)
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
        against = board.black if board.white == self.user else board.white
        movement_message = MovementMessage(
            game=game_id,
            player_state=MovementState.YOUR_TURN if any(right_turn) else MovementState.THEIR_TURN
        )
        message_crossing = self.message_crossing_factory.build(against)
        self.movement_machine = MovementStateMachine({
            MovementState.THEIR_TURN: OpponentInterface(persistence=self.persistence, game_viewer=self.game_viewer, message_crossing=message_crossing),
            MovementState.YOUR_TURN: PlayerInterface(persistence=self.persistence, game_viewer=self.game_viewer, message_crossing=message_crossing, movements=self.movements)
        })
        self.game_viewer.display(game_id)
        self.stop_event = threading.Event()
        def start_async_movement():
            asyncio.run(self.movement_machine.main_loop(movement_message, self.stop_event))
        threading.Thread(target=start_async_movement, daemon=True).start()
    
    def start_game(self):
        black = self.keyboard.read("Who are you challenging? ").strip()
        players = Players(white=self.user, black=black)
        board = Board(white=players.white, black=players.black, game_id=self.persistence.next_id())
        self.persistence.burn(board)
