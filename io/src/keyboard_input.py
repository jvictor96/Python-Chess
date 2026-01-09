from abc import ABC, abstractmethod


class KeyboardInputPort(ABC):
    @abstractmethod
    def read(self, prompt: str) -> str:
        pass

class PhysicalKeyboard(KeyboardInputPort):
    def read(self, prompt: str):
        return input(prompt)
    
class InMemoryKeyboard(KeyboardInputPort):
    outputs: list[str]

    def __init__(self):
        self.outputs = []
    
    def read(self, prompt):
        return self.outputs.pop(0) if self.outputs else ""
    
    def append_output(self, text):
        self.outputs.append(text)
