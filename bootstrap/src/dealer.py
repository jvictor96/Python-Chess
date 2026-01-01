from chess_daemon import Moderator, Dealer, DealerCleanUp

from game_persistence import FileGamePersistenceAdapter

from player_input import ShellMovementInputUI
from game_viewer import TextViewerAdapter
from daemon_controller import DealerInput
from keyboard_input import PhysicalKeyboard

from opponent_listener import OpponentListener

from machine_core import MovementStateMachine, DealerStateMachine, MovementState, DealerState

movement_machine = MovementStateMachine()  # TODO: Start it at starting stage to load persistent data and decide if it's idle or at the player's turn
dealer_machine = DealerStateMachine()

file_persistence = FileGamePersistenceAdapter()
physical_keyboard = PhysicalKeyboard()
viewer_adapater = TextViewerAdapter()

opponent_listener = OpponentListener(
    movement_machine=movement_machine # This is actually to handle the idle, it has access to the machine to send a message for a new remote movements
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
    keyboard=physical_keyboard
)

dealer_input = DealerInput(
    game_persistence_port=file_persistence,
    keyboard=physical_keyboard,
    dealer_machine=dealer_machine     # This is actually to handle the idle, it has access to the machine to send a message for a new game
)                                     # TODO: maybe create a ExternalEventSource interface and a special register to link it to idle

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

dealer_machine.register(
    handler=dealer,
    state=DealerState.COMMAND_SENT
)

dealer_machine.register(
    handler=dealer_clean_up,
    state=DealerState.DIGESTED
)