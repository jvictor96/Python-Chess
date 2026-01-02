import asyncio
import time
from chess_daemon import Moderator, Dealer, DealerCleanUp

from game_persistence import FileGamePersistenceAdapter

from player_input import ShellMovementInputUI
from game_viewer import TextViewerAdapter
from daemon_controller import DealerInput
from keyboard_input import PhysicalKeyboard

from opponent_interface import FileOpponentInterface
from dealer_interface import FileDealerInterface

from machine_core import MovementStateMachine, DealerStateMachine, MovementState, DealerState

movement_machine = MovementStateMachine()
dealer_machine = DealerStateMachine()

file_persistence = FileGamePersistenceAdapter()
physical_keyboard = PhysicalKeyboard()
viewer_adapater = TextViewerAdapter()


dealer_interface = FileDealerInterface()
opponent_interface = FileOpponentInterface(
    user=input("Enter your username"),
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

dealer_input = DealerInput(
    game_persistence_port=file_persistence,
    keyboard=physical_keyboard,
    dealer_interface=dealer_interface     
)                                    

movement_machine.set_event_source(opponent_interface)

movement_machine.register(             # TODO: Put a to_states={MovementState.WHITE_TURN} at register
    handler=movement_input,
    state=MovementState.BLACK_TURN
)

movement_machine.register(
    handler=movement_input,
    state=MovementState.WHITE_TURN
)

movement_machine.register(
    handler=viewer_adapater,
    state=MovementState.WHITE_PLAYED
)

movement_machine.register(
    handler=viewer_adapater,
    state=MovementState.BLACK_PLAYED
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

# TODO: Load persisted games here

asyncio.create_task(dealer_machine.main_loop())
asyncio.create_task(movement_machine.main_loop())

while True:
    time.sleep(10)