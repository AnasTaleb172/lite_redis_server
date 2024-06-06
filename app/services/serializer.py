from ..interfaces.message import Message
from ..factories.messageFactory import MessageFactory
from ..exceptions import (
    MessageNotStringException,
    MessageEmptyException,
)


class Serializer:

    def __init__(self, _message: Message) -> None:
        self._message = _message

    def serialize(self):
        return self._message.serialize()
