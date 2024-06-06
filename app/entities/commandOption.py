from app.interfaces.commandOption import CommandOption
from app import helpers

class EXCommandOption(CommandOption):
    def __init__(self, value: str = "") -> None:
        super().__init__(value)

    # Setter for value
    def set_value(self, value: str | int) -> None:
        return helpers.get_now_timestamp_in_seconds() + int(value)

    def execute(self):
        return self._value > helpers.get_now_timestamp_in_seconds()
    

class PXCommandOption(CommandOption):
    def __init__(self, value: str = "") -> None:
        super().__init__(value)

    # Setter for value
    def set_value(self, value: str | int) -> None:
        return helpers.get_now_timestamp_in_milliseconds() + (int(value) / 1000)

    def execute(self):
        return self._value > helpers.get_now_timestamp_in_milliseconds()

class EAXTCommandOption(CommandOption):
    def __init__(self, value: str = "") -> None:
        super().__init__(value)

    # Setter for value
    def set_value(self, value: str | int) -> None:
        return int(value)

    def execute(self):
        return self._value > helpers.get_now_timestamp_in_seconds()

class PXATCommandOption(CommandOption):
    def __init__(self, value: str = "") -> None:
        super().__init__(value)

    # Setter for value
    def set_value(self, value: str | int) -> None:
        return helpers.get_now_timestamp_in_milliseconds()

    def execute(self):
        return self._value > helpers.get_now_timestamp_in_milliseconds()
