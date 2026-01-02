from abc import ABC, abstractmethod

from typing import Iterable, TypeVar, Generic

class Message(ABC):
    pass

TMessage = TypeVar("TMessage", bound=Message)

class ExternalEventSource(ABC, Generic[TMessage]):
    @abstractmethod
    def poll() -> Iterable[TMessage]:
        pass