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
        self.sending_batch = False
        self.testing = False
        if os.path.exists(self.path):
            os.remove(self.path)
        os.mkfifo(self.path)
        if os.path.exists(self.path_out):
            os.remove(self.path_out)
        os.mkfifo(self.path_out)

    def listen(self):
        def worker():
            while not self.stop.is_set():
                with open(self.path, "r") as ff:
                    for line in ff:
                        try:
                            line = line.strip()
                            if not line:
                                continue
                            self.queue.put(json.loads(line))
                        except Exception:
                            pass

        self._thread = threading.Thread(target=worker, daemon=True)
        self._thread.start()

    def send(self, data):
        if self.testing:
            return
        def worker():
            with open(f"{self.path_out}", "w") as ff:
                json.dump(data, ff)
                ff.write("\n")
                ff.flush()
        self._thread_send = threading.Thread(target=worker, daemon=True)
        self._thread_send.start()

    def send_batch(self, batch):
        self.sending_batch = True
        self.testing = True
        def worker():
            for data in batch:
                with open(f"{self.path}", "w") as ff:
                    json.dump(data, ff)
                    ff.write("\n")
                    ff.flush()
            self.sending_batch = False
        self._thread_send = threading.Thread(target=worker, daemon=True)
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