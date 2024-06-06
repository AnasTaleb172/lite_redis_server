from app.interfaces.commandHandler import CommandHandler
from app.interfaces.message import Message
from app.entities.simpleStringMessage import SimpleStringMessage
from app.entities.bulkStringMessage import BulkStringMessage
from db.dbAdapter import DbAdapter
from app.factories.commandOptionFactory import CommandOptionFactory
from app.exceptions import FunctionalException

class PingCommandHandler(CommandHandler):
    def __init__(self, dbAdapter: DbAdapter, *args) -> None:
        super().__init__(dbAdapter, *args)

    def _set_options(self):
        pass

    def _execute_command(self):
        pass

    def handle(self) -> Message:
        return SimpleStringMessage("PONG")
    
class EchoCommandHandler(CommandHandler):
    def __init__(self, dbAdapter: DbAdapter, *args) -> None:
        super().__init__(dbAdapter, *args)

    def _set_options(self):
        pass

    def _execute_command(self):
        pass

    def handle(self) -> Message:
        return BulkStringMessage(" ".join(self.args))
    
class SetCommandHandler(CommandHandler):
    def __init__(self, dbAdapter: DbAdapter, *args) -> None:
        super().__init__(dbAdapter, *args)

    def _set_options(self):
        optionsPart = self.args[2:]
        for i in range(0, len(optionsPart), 2):
            if i + 1 > len(optionsPart) - 1:
                raise FunctionalException("Invalid command option arguments")
            self.options.append(CommandOptionFactory.create_command_by_text(optionsPart[i], optionsPart[i + 1]))

    def _execute_command(self):
        if not (isinstance(self.args, tuple) and len(self.args) > 1):
            raise FunctionalException("Not valid command arguments length")
        
        self._set_options()

        return self.dbAdapter.set(self.args[0], self.args[1], self.options)
        
    def handle(self) -> Message:
        self._execute_command()
        return SimpleStringMessage("OK")
    
class GetCommandHandler(CommandHandler):
    def __init__(self, dbAdapter: DbAdapter, *args) -> None:
        super().__init__(dbAdapter, *args)

    def _set_options(self):
        pass

    def _execute_command(self):

        if not (isinstance(self.args, tuple) and len(self.args) > 0):
            raise FunctionalException("Not valid command arguments length")

        return self.dbAdapter.get(self.args[0])

    def handle(self) -> Message:
        response = self._execute_command()
        return BulkStringMessage(response if response else "nil")