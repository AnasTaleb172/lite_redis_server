from app.interfaces.commandHandler import CommandHandler
from app.interfaces.message import Message
from app.entities import (simpleStringMessage, bulkStringMessage, integerMessage)
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
        return simpleStringMessage.SimpleStringMessage("PONG")
    
class EchoCommandHandler(CommandHandler):
    def __init__(self, dbAdapter: DbAdapter, *args) -> None:
        super().__init__(dbAdapter, *args)

    def _set_options(self):
        pass

    def _execute_command(self):
        pass

    def handle(self) -> Message:
        return bulkStringMessage.BulkStringMessage(" ".join(self.args))
    
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
        return simpleStringMessage.SimpleStringMessage("OK")
    
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
        return bulkStringMessage.BulkStringMessage(response if response else "nil")
    

class ExistsCommandHandler(CommandHandler):
    def __init__(self, dbAdapter: DbAdapter, *args) -> None:
        super().__init__(dbAdapter, *args)

    def _set_options(self):
        pass

    def _execute_command(self):
        if not (isinstance(self.args, tuple) and len(self.args) > 0):
            raise FunctionalException("Not valid command arguments length")

        # return the count of existing keys
        return sum((1 for key in self.args if self.dbAdapter.exists(key)), start=0)

    def handle(self) -> Message:
        response = self._execute_command()
        return integerMessage.IntegerMessage(response)

class DelCommandHandler(CommandHandler):
    def __init__(self, dbAdapter: DbAdapter, *args) -> None:
        super().__init__(dbAdapter, *args)

    def _set_options(self):
        pass

    def _execute_command(self):
        if not (isinstance(self.args, tuple) and len(self.args) > 0):
            raise FunctionalException("Not valid command arguments length")

        # return the count of existing keys
        return sum((1 for key in self.args if self.dbAdapter.delete(key)), start=0)

    def handle(self) -> Message:
        response = self._execute_command()
        return integerMessage.IntegerMessage(response)
    
class IncrCommandHandler(CommandHandler):
    def __init__(self, dbAdapter: DbAdapter, *args) -> None:
        super().__init__(dbAdapter, *args)

    def _set_options(self):
        pass

    def _execute_command(self):
        if not (isinstance(self.args, tuple) and len(self.args) == 1):
            raise FunctionalException("Not valid command arguments length")
        
        storedValue = self.dbAdapter.get(self.args[0]) # get stored key

        if isinstance(storedValue, int): # pass if storedValue is int
            pass
        elif storedValue is None: # set to 0 if storedValue is None
            storedValue = 0
        elif isinstance(storedValue, str) and storedValue.isnumeric(): # parse to int if storedValue is numeric
            storedValue = int(storedValue)
        else:
            raise FunctionalException("Stored value is not int")

        updatedValue = storedValue + 1
        self.dbAdapter.set(self.args[0], str(updatedValue)) # update the value in db

        # return the count of existing keys
        return updatedValue

    def handle(self) -> Message:
        response = self._execute_command()
        return integerMessage.IntegerMessage(response)
    
class DecrCommandHandler(CommandHandler):
    def __init__(self, dbAdapter: DbAdapter, *args) -> None:
        super().__init__(dbAdapter, *args)

    def _set_options(self):
        pass

    def _execute_command(self):
        if not (isinstance(self.args, tuple) and len(self.args) == 1):
            raise FunctionalException("Not valid command arguments length")
        
        storedValue = self.dbAdapter.get(self.args[0]) # get stored key

        if isinstance(storedValue, int): # pass if storedValue is int
            pass
        elif storedValue is None: # set to 0 if storedValue is None
            storedValue = 0
        elif isinstance(storedValue, str) and storedValue.isnumeric(): # parse to int if storedValue is numeric
            storedValue = int(storedValue)
        else:
            raise FunctionalException("Stored value is not int")

        updatedValue = storedValue - 1
        self.dbAdapter.set(self.args[0], str(updatedValue)) # update the value in db

        # return the count of existing keys
        return updatedValue

    def handle(self) -> Message:
        response = self._execute_command()
        return integerMessage.IntegerMessage(response)