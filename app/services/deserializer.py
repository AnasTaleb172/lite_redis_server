from ..interfaces.message import Message
from ..factories.messageFactory import MessageFactory
from ..exceptions import (
    MessageNotStringException,
    MessageEmptyException,
)


class Deserializer:

    def __init__(self, text: str) -> None:

        # set the str attribute
        self.text = text

        # validate the text
        self._validate_text()

        # create the message by its text
        self._message = MessageFactory.create_message_by_text(text)

    def deserialize(self):
        return self._message.deserialize()

    def _validate_text(self):
        if not isinstance(self.text, str):
            raise MessageNotStringException
        if not self.text:
            raise MessageEmptyException
