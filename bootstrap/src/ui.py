from daemon_controller import DealerInput
from keyboard_input import PhysicalKeyboard
from game_persistence import FileGamePersistenceAdapter

DealerInput(PhysicalKeyboard(), FileGamePersistenceAdapter()).read_action()