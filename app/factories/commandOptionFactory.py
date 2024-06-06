from ..interfaces.commandOption import CommandOption
from ..entities import commandOption
from ..enums import CommandOptionKey
from ..exceptions import NotValidOptionKeyException


class CommandOptionFactory:
    @staticmethod
    def create_command_by_text(text: str, value) -> CommandOption:
        match text.upper():
            case CommandOptionKey.EX_KEY.value:
                return commandOption.EXCommandOption(value)
            case CommandOptionKey.PX_KEY.value:
                return commandOption.PXCommandOption(value)
            case CommandOptionKey.EAXT_KEY.value:
                return commandOption.EAXTCommandOption(value)
            case CommandOptionKey.PXAT_KEY.value:
                return commandOption.PXATCommandOption(value)
            case _:
                raise NotValidOptionKeyException