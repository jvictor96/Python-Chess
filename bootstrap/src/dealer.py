import queue
from game_persistence import FileGamePersistenceAdapter

from game_viewer import TextViewerAdapter
from keyboard_input import PhysicalKeyboard

from dealer_interface import CommandReader, CommandRouter, DealerDispatcher

from machine_core import DealerStateMachine, DealerState
from message_crossing import FileMessageCrossingFactory

user = input("Enter your username ")

file_persistence = FileGamePersistenceAdapter()
physical_keyboard = PhysicalKeyboard()
viewer_adapter = TextViewerAdapter(
    persistence=file_persistence,
    user=user
)
message_crossing_factory = FileMessageCrossingFactory()
movements = queue.Queue()
                   
dealer_machine = DealerStateMachine({
    DealerState.READING: CommandReader(keyboard=physical_keyboard),
    DealerState.FILTERING: CommandRouter(movements=movements, user=user, game_viewer=viewer_adapter, persistence=file_persistence),
    DealerState.EXECUTING: DealerDispatcher(message_crossing_factory=message_crossing_factory, game_viewer=viewer_adapter, keyboard=physical_keyboard)
})

dealer_machine.main_loop()
