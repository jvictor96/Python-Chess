import asyncio
import threading
import time
from chess_daemon import Moderator, Dealer, DealerCleanUp

from game_persistence import FileGamePersistenceAdapter

from player_input import ShellMovementInputUI
from game_viewer import TextViewerAdapter
from daemon_controller import DealerInput
from keyboard_input import PhysicalKeyboard

from opponent_interface import FileOpponentInterface
from dealer_interface import FileDealerInterface
from human_interface import TerminalInterfaceAdapter

from machine_core import MovementStateMachine, DealerStateMachine, MovementState, DealerState

movement_machine = MovementStateMachine()
dealer_machine = DealerStateMachine()

file_persistence = FileGamePersistenceAdapter()
physical_keyboard = PhysicalKeyboard()
viewer_adapater = TextViewerAdapter(
    persistence=file_persistence
)

user = input("Enter your username ")
dealer_interface = FileDealerInterface()
opponent_interface = FileOpponentInterface(
    user=user,
    persistence=file_persistence
)

moderator = Moderator(
    game_persistence_adapter=file_persistence
)
dealer = Dealer(
    game_persistence_adapter=file_persistence
)
dealer_clean_up = DealerCleanUp()

movement_input = ShellMovementInputUI(
    persistence=file_persistence,
    keyboard=physical_keyboard,
    opponent_interface=opponent_interface
)

human_interface = TerminalInterfaceAdapter(
    user=user,
    game_viewer=viewer_adapater,
    player_input=movement_input,
    persistence=file_persistence
)

dealer_input = DealerInput(
    game_persistence_port=file_persistence,
    keyboard=physical_keyboard,
    dealer_interface=dealer_interface,
    human_interface_port=human_interface,
    user=user
)                                    


movement_machine.set_event_source(opponent_interface)

movement_machine.register(             # TODO: Put a to_states={MovementState.WHITE_TURN} at register
    handler=human_interface,
    state=MovementState.YOUR_TURN
)

dealer_machine.set_event_source(dealer_interface)

dealer_machine.register(
    handler=dealer,
    state=DealerState.COMMAND_SENT
)

dealer_machine.register(
    handler=dealer_clean_up,
    state=DealerState.DIGESTED
)

def start_async_dealer():
    asyncio.run(dealer_machine.main_loop())
threading.Thread(target=start_async_dealer, daemon=True).start()

movement_message = dealer_input.read_action()

def start_async_movement():
    asyncio.run(movement_machine.main_loop(movement_message))

threading.Thread(target=start_async_movement, daemon=True).start()

while True:
    time.sleep(10)