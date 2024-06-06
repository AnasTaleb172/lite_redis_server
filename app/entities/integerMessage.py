from ..interfaces.message import Message
from ..enums import MessageSpecialChar, MessagePrefix
from ..exceptions import NotValidMessageFormatException


class IntegerMessage(Message):
    """
    Patterns are:
        - :[<+|->]<value>\r\n
    """

    def __init__(self, text: str) -> None:
        super().__init__(text)

    def deserialize(self) -> int:
        # remove prefix
        message = int(
            self.text.removeprefix(MessagePrefix.INTEGER.value).replace(
                MessageSpecialChar.CRLF.value, ""
            )
        )

        return message

    def serialize(self) -> str:
        if not isinstance(self.text, int):
            raise NotValidMessageFormatException

        return (
            f"{MessagePrefix.INTEGER.value}{self.text}{MessageSpecialChar.CRLF.value}"
        )
