from ..interfaces.message import Message
from ..enums import MessageSpecialChar, MessagePrefix

from ..exceptions import NotValidMessageFormatException


class SimpleStringMessage(Message):
    """
    Patterns are:
        - +<data>\r\n -> <data>
    """

    def __init__(self, text: str) -> None:
        super().__init__(text)

    def deserialize(self) -> str:
        # remove prefix
        message = self.text.removeprefix(MessagePrefix.SIMPLE_STRING.value).replace(
            MessageSpecialChar.CRLF.value, ""
        )
        return message

    def serialize(self) -> str:

        if self.text is None or not isinstance(self.text, str):
            raise NotValidMessageFormatException

        return f"{MessagePrefix.SIMPLE_STRING.value}{self.text}{MessageSpecialChar.CRLF.value}"
