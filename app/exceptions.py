
class FunctionalException(Exception):
    """
    Functional Exception.

    Attributes:
        inputMessage -> optional : message input
    """

    def __init__(self, message: str = None) -> None:
        self.message = message or "Error Not Specified"
        super().__init__(self.message)

class MessageNotStringException(FunctionalException):
    """
    Exception raised when message is not string.

    Attributes:
        inputMessage -> optional : message input
    """

    def __init__(self, inputMessage="") -> None:
        self.inputMessage = inputMessage
        self.message = "Message input is not string!!"
        super().__init__(self.message)


class MessageEmptyException(FunctionalException):
    """
    Exception raised when message empty.
    """

    def __init__(self) -> None:
        self.message = "Message input empty!!"
        super().__init__(self.message)


class NotValidMessageFormatException(FunctionalException):
    """
    Exception raised when message has invalid prefix.
    """

    def __init__(self) -> None:
        self.message = "Message has invalid prefix!!"
        super().__init__(self.message)

class NotValidOptionKeyException(FunctionalException):
    """
    Exception raised when message has invalid prefix.
    """

    def __init__(self) -> None:
        self.message = "Option has invalid key!!"
        super().__init__(self.message)


class NotValidCommandHandlerException(FunctionalException):
    """
    Exception raised when message has invalid prefix.
    """

    def __init__(self) -> None:
        self.message = "Command handler has invalid text!!"
        super().__init__(self.message)
