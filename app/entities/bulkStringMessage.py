from ..interfaces.message import Message
from ..enums import MessageSpecialChar, MessagePrefix
from ..exceptions import NotValidMessageFormatException


class BulkStringMessage(Message):
    """
    Patterns are:
        - $<length>\r\n<data>\r\n
            - $3\r\n<data>\r\n -> <data>
            - $0\r\n\r\n    -> ''
        - $-1\r\n           -> None
    """

    def __init__(self, text: str) -> None:
        super().__init__(text)

    def deserialize(self) -> str:

        # remove prefix
        message = self.text.removeprefix(MessagePrefix.BULK_STRING.value)

        # discover pattern
        if message.startswith("-1"):
            msgResult = None
        else:
            # split the message & get message length
            splittedMessage = message.split(MessageSpecialChar.CRLF.value)
            messageLength = int(splittedMessage[0])

            # discover case for a pattern
            msgResult = splittedMessage[1] if messageLength > 0 else ""

        return msgResult

    def serialize(self) -> str:
        if not isinstance(self.text, str) and not self.text is None:
            raise NotValidMessageFormatException
        
        # handle null case
        if self.text is not None:
            messageText = self.text
            serializedMessage = f"{MessagePrefix.BULK_STRING.value}{len(messageText)}{MessageSpecialChar.CRLF.value}{messageText}{MessageSpecialChar.CRLF.value}"
        else:
            serializedMessage = "$-1\r\n"

        return serializedMessage