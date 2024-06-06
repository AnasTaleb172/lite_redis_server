from abc import ABC, abstractmethod


class Message(ABC):
    def __init__(self, text: str) -> None:
        self.text = text

    @abstractmethod
    def deserialize(self):
        return

    @abstractmethod
    def serialize(self) -> str:
        return
