from abc import ABC, abstractmethod


class KeyboardInput(ABC):
    @abstractmethod
    def read(self, prompt: str) -> str:
        pass

class PhysicalKeyboard(KeyboardInput):
    def read(self, prompt: str):
        return input(prompt)
    
class InMemoryKeyboard(KeyboardInput):
    outputs: list[str]

    def __init__(self):
        self.outputs = []
    
    def read(self, prompt):
        return self.outputs.pop(0)
    
    def push_output(self, text):
        self.outputs.append(text)
