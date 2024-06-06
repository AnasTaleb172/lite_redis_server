from enum import Enum


class MessageSpecialChar(Enum):
    CRLF = "\r\n"


class MessagePrefix(Enum):
    SIMPLE_STRING = "+"
    BULK_STRING = "$"
    SIMPLE_ERROR = "-"
    INTEGER = ":"
    ARRAY = "*"

    @classmethod
    def list(cls, except_=[]) -> list:
        except_ = except_ if isinstance(except_, list) else [except_]
        return list(
            filter(lambda c: cls(c) not in except_, map(lambda c: c.value, cls))
        )
    
class CommandOptionKey(Enum):
    EX_KEY = "EX"
    PX_KEY = "PX"
    EAXT_KEY = "EXAT"
    PXAT_KEY = "PXAT"

class CommandHandlerKey(Enum):
    PING_KEY = "PING"
    ECHO_KEY = "ECHO"
    SET_KEY = "SET"
    GET_KEY = "GET"
    EXISTS_KEY = "EXISTS"
    DEL_KEY = "DEL"



"""
SIMPLE_STRING:
    - \+[A-Za-z0-9]+\\r\\n
BULK_STRING:
    - \$[0-9]+\\r\\n[A-Za-z0-9]+\\r\\n
    - \$-1\\r\\n
SIMPLE_ERROR:
    - -[A-Za-z0-9]+\\r\\n
INTEGER:
    - :[+-]?[0-9]+\\r\\n
ARRAY:
    - \*[0-9]+\\r\\n(\\+[A-Za-z0-9]+\\r\\n|\$[0-9]+\\r\\n[A-Za-z0-9]+\\r\\n|\$-1\\r\\n|-[A-Za-z0-9]+\\r\\n|:[+-]?[0-9]+\\r\\n)+
"""
