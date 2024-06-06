from ..interfaces.message import Message
from ..enums import MessageSpecialChar, MessagePrefix
from ..exceptions import NotValidMessageFormatException


class SimpleErrorMessage(Message):
    """
    Patterns are:
        - -<data>\r\n
    """

    def __init__(self, text: str) -> None:
        super().__init__(text)

    def deserialize(self) -> str:
        # remove prefix
        message = self.text.removeprefix(MessagePrefix.SIMPLE_ERROR.value)
        return message.replace(MessageSpecialChar.CRLF.value, "")

    def serialize(self) -> str:
        if self.text is None or not isinstance(self.text, str):
            raise NotValidMessageFormatException

        return f"{MessagePrefix.SIMPLE_ERROR.value}{self.text}{MessageSpecialChar.CRLF.value}"
