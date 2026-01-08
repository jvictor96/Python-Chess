from game_persistence import FileGamePersistenceAdapter

from game_viewer import TextViewerAdapter
from keyboard_input import PhysicalKeyboard

from dealer_interface import CommandReader, CommandRouter, DealerDispatcher

from machine_core import DealerStateMachine, DealerState

user = input("Enter your username ")

file_persistence = FileGamePersistenceAdapter()
physical_keyboard = PhysicalKeyboard()
viewer_adapater = TextViewerAdapter(
    persistence=file_persistence,
    user=user
)

command_router = CommandRouter(user=user, game_viewer=viewer_adapater, persistence=file_persistence)
                   
dealer_machine = DealerStateMachine({
    DealerState.READING: CommandReader(keyboard=physical_keyboard),
    DealerState.FILTERING: command_router,
    DealerState.EXECUTING: DealerDispatcher(command_router= command_router,game_viewer=viewer_adapater, keyboard=physical_keyboard, persistence=file_persistence, user=user)
})

dealer_machine.main_loop()  # It's syncronous now and actually bootstraps the movement machine at DealerDispatcher. It only picks the implementation for FileOpponentInterface and MessageCrossing
                            # Maybe a Factory will solve it, the issue is these both ports depend on the opponent name and it's known during the dealer main loop