from abc import ABC, abstractmethod
import asyncio
import os, json
from dataclasses import asdict
from queue import Empty, Queue
import threading
from ports import GamePersistencePort, GameViewerPort
from machine_core import MovementMessage, MovementState, MovementStateHandler

class MessageCrossing(ABC):
    @abstractmethod
    def listen(self):
        pass
    @abstractmethod
    def pop(self):
        pass
    @abstractmethod
    def close(self):
        pass
    @abstractmethod
    def send(self, content: str):
        pass


class FileMessageCrossing(MessageCrossing):
    def __init__(self, addr, addr_out):
        self.queue = Queue()
        self.stop = threading.Event()
        self.path = f"{os.environ['HOME']}/python_chess/{addr}.fifo"
        self.path_out = f"{os.environ['HOME']}/python_chess/{addr_out}.fifo"
        self._thread = None
        self._thread_send = None
        if not os.path.exists(self.path):
            os.mkfifo(self.path)
        if not os.path.exists(self.path_out):
            os.mkfifo(self.path_out)

    def listen(self):
        def start_async_listen():
            while not self.stop.is_set():
                with open(self.path, "r") as ff:
                    try:
                        content = json.load(ff)
                        self.queue.put(content)
                    except Exception:
                        break
        self._thread = threading.Thread(target=start_async_listen, daemon=True)
        self._thread.start()

    def send(self, data):
        def start_async_send():
            with open(f"{self.path}", "w") as ff:
                json.dump(data, ff)
        self._thread_send = threading.Thread(target=start_async_send, daemon=True)
        self._thread_send.start()

    def pop(self):
        try:
            return self.queue.get_nowait()
        except Empty:
            return None
        
    def close(self):
        self.stop.set()
        try:
            with open(self.path, "w") as fw:
                fw.write("\n")  
        except Exception:
            pass

        if self._thread_send:
            with open(self.path_out, "r") as ff:
                try:
                    content = json.load(ff)
                    self.queue.put(content)
                except Exception:
                    pass
        
        if self._thread:
            self._thread.join(timeout=1)

class FileOpponentInterface(MovementStateHandler):
    def __init__(self, persistence: GamePersistencePort, game_viewer: GameViewerPort, message_crossing: MessageCrossing):
        self.persistence = persistence
        self.game_viewer = game_viewer
        self.message_crossing = message_crossing   # Here I'm counting that message crossing and game viewer know the user and the opponent
    
    def handle_movement(self, msg) -> MovementMessage:    
        msg.next_player_state = MovementState.THEIR_TURN   
        if message:=self.message_crossing.pop():
            board = self.persistence.get_board(msg.game)
            board.move(message["move"])
            self.game_viewer.display(msg.game)
            self.persistence.burn(board)
            msg.next_player_state = MovementState.YOUR_TURN
        return msg
    
    def send_message(self, message: MovementMessage) -> None:     
        data = asdict(message)
        data.pop("player_state", None)
        self.message_crossing.send(message)
