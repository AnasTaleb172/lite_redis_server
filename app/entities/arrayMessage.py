import re

from ..interfaces.message import Message
from ..enums import MessageSpecialChar, MessagePrefix
from ..exceptions import NotValidMessageFormatException


class ArrayMessage(Message):
    """
    Patterns are:
        - *<number-of-elements>\r\n<Message>...<Message> -> non-empty array
            - *0\r\n                                     -> empty array
        - *-1\r\n                                        -> Null array
    """

    def __init__(self, text: str) -> None:
        super().__init__(text)

    def deserialize(self) -> list:

        from ..factories.messageFactory import MessageFactory

        # array regex pattern
        pattern = "\\*[+-]?\d+\\r\\n|\+.+\\r\\n|\$\d+\\r\\n.+\\r\\n|\$-1\\r\\n|-.+\\r\\n|:[+-]?\d+\\r\\n"
        splittedMessage = re.findall(pattern, self.text)

        # array definition
        arrayDef = splittedMessage.pop(0)  # '*23\\r\\' -> '\*([+-]?\d+)\\r\\n'
        arrayDefGroups = re.search(r"\*([+-]?\d+)\r\n", arrayDef)
        if arrayDefGroups:
            arrayLength = int(arrayDefGroups.group(1))

            match arrayLength:
                case -1:
                    message = None
                case 0:
                    message = []
                case _:  # has elements
                    message = []
                    offset = 0
                    for i, splitMsg in enumerate(splittedMessage):

                        # if not within array elements range
                        if i >= offset:
                            # if nested array
                            nestedArrayDef = re.search(r"\*([+-]?\d+)\r\n", splitMsg)
                            if nestedArrayDef:
                                nestedArrayLength = int(nestedArrayDef.group(1))
                                newElement = "".join(
                                    splittedMessage[i : i + 1 + nestedArrayLength]
                                )
                                offset = i + nestedArrayLength + 1
                            else:
                                newElement = splitMsg

                            DeserializedMessage = MessageFactory.create_message_by_text(
                                newElement
                            ).deserialize()
                            message.append(DeserializedMessage)

        else:
            raise NotValidMessageFormatException

        return message

    def serialize(self) -> str:

        from . import bulkStringMessage, integerMessage
        from ..factories.messageFactory import MessageFactory

        if not self.text is None and not iter(self.text):
            raise NotValidMessageFormatException

        if self.text is None:
            return "*-1\r\n"
        else:
            # form the messageText
            messageText = ""
            for el in self.text:
                if isinstance(el, str):
                    messageText = (
                        messageText
                        + f"{bulkStringMessage.BulkStringMessage(el).serialize()}"
                    )
                elif isinstance(el, int):
                    messageText = (
                        messageText + f"{integerMessage.IntegerMessage(el).serialize()}"
                    )
                elif el is None:
                    messageText = messageText + "$-1\r\n"
                elif iter(el):
                    messageText = messageText + f"{ArrayMessage(el).serialize()}"

            return f"{MessagePrefix.ARRAY.value}{len(self.text)}{MessageSpecialChar.CRLF.value}{messageText}"  # ["echo", "hello world"] --> "*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n"
