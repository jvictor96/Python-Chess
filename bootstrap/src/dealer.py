from chess_daemon import ChessDaemon
from game_persistence import FileGamePersistenceAdapter, TextViewerAdapter

ChessDaemon(FileGamePersistenceAdapter(), TextViewerAdapter()).main_loop()