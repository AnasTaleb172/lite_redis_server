from app.interfaces.commandHandler import CommandHandler
from app.services import commandHandler
from ..enums import CommandHandlerKey
from db.dbAdapter import DbAdapter
from app.exceptions import FunctionalException, NotValidCommandHandlerException

class CommandHandlerFactory:
    @staticmethod
    def create_command_handler_by_text(dbAdapter: DbAdapter, commandMessage: list) -> CommandHandler:
        if len(commandMessage) < 1:
            raise FunctionalException("Not valid Command")
        cmd, args = commandMessage.pop(0).lower(), commandMessage

        match cmd.upper():
            case CommandHandlerKey.PING_KEY.value:
                return commandHandler.PingCommandHandler(dbAdapter, *args)
            case CommandHandlerKey.ECHO_KEY.value:
                return commandHandler.EchoCommandHandler(dbAdapter, *args)
            case CommandHandlerKey.SET_KEY.value:
                return commandHandler.SetCommandHandler(dbAdapter, *args)
            case CommandHandlerKey.GET_KEY.value:
                return commandHandler.GetCommandHandler(dbAdapter, *args)
            case CommandHandlerKey.EXISTS_KEY.value:
                return commandHandler.ExistsCommandHandler(dbAdapter, *args)
            case CommandHandlerKey.DEL_KEY.value:
                return commandHandler.DelCommandHandler(dbAdapter, *args)
            case CommandHandlerKey.INCR_KEY.value:
                return commandHandler.IncrCommandHandler(dbAdapter, *args)
            case CommandHandlerKey.DECR_KEY.value:
                return commandHandler.DecrCommandHandler(dbAdapter, *args)
            case CommandHandlerKey.LPUSH_KEY.value:
                return commandHandler.LpushCommandHandler(dbAdapter, *args)
            case CommandHandlerKey.RPUSH_KEY.value:
                return commandHandler.RpushCommandHandler(dbAdapter, *args)
            case _:
                raise NotValidCommandHandlerException