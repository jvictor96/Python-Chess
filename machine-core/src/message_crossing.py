from abc import ABC, abstractmethod
import os, json
from queue import Empty, Queue
import threading

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
    @abstractmethod
    def send_batch(self, content: str):
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

    def send_batch(self, batch):
        def start_async_send():
            for data in batch:
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

class MessageCrossingFactory(ABC):
    @abstractmethod
    def build(opponent: str) -> MessageCrossing:
        pass

class FileMessageCrossingFactory(MessageCrossingFactory):
    def __init__(self, user: str):
        self.user = user

    def build(self, opponent):
        return FileMessageCrossing(self.user, opponent)