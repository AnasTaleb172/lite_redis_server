from abc import ABC, abstractmethod


class CommandOption(ABC):
    def __init__(self, value: str = "") -> None:
        self._key = None
        self._value = self.set_value(value)

    # Getter for key
    @property
    def key(self) -> str:
        return self._key

    # Setter for key
    @key.setter
    def key(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("Key must be a string")
        self._key = value

    # Getter for value
    @property
    def value(self) -> str | int:
        return self._value

    # Setter for value
    @abstractmethod
    def set_value(self, value: str | int) -> None:
        return
    
    @abstractmethod
    def execute(self):
        return


    def to_dict(self) -> dict:
        return {self.key: self.value}
