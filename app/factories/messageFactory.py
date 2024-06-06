from ..entities import arrayMessage
from ..interfaces.message import Message
from ..entities import (
    simpleStringMessage,
    bulkStringMessage,
    simpleErrorMessage,
    integerMessage,
)
from ..enums import MessagePrefix
from ..exceptions import NotValidMessageFormatException


class MessageFactory:
    @staticmethod
    def create_message_by_text(text: str) -> Message:
        prefix = text[:1] if text else ""
        match prefix:
            case MessagePrefix.SIMPLE_STRING.value:
                return simpleStringMessage.SimpleStringMessage(text)
            case MessagePrefix.BULK_STRING.value:
                return bulkStringMessage.BulkStringMessage(text)
            case MessagePrefix.SIMPLE_ERROR.value:
                return simpleErrorMessage.SimpleErrorMessage(text)
            case MessagePrefix.INTEGER.value:
                return integerMessage.IntegerMessage(text)
            case MessagePrefix.ARRAY.value:
                return arrayMessage.ArrayMessage(text)
            case _:
                raise NotValidMessageFormatException
