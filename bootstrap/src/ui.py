from daemon_controller import DaemonController
from keyboard_input import PhysicalKeyboard
from game_persistence import FileGamePersistenceAdapter

DaemonController(PhysicalKeyboard(), FileGamePersistenceAdapter()).read_action()