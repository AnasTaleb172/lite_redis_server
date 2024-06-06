import sys

# set package path
sys.path.insert(0, "/home/anas/DEV/redis/redis_server")

from app.services.deserializer import Deserializer
from app.services.serializer import Serializer
from app.factories.commandHandlerFactory import CommandHandlerFactory
from db.dbAdapter import DbAdapter
from app.entities.simpleErrorMessage import SimpleErrorMessage
from app.exceptions import FunctionalException

class RequestHandler():
    def __init__(self, dbAdapter: DbAdapter) -> None:
        self.dbAdapter = dbAdapter

    def handle(self, data: bytes):
        try:
            decoded = self._decode(data)
            deserialized = Deserializer(decoded).deserialize() # -> list [COMMAND, args, ....]
            cmdHandler = CommandHandlerFactory.create_command_handler_by_text(self.dbAdapter, deserialized)
            messageResponse = cmdHandler.handle()
        except FunctionalException as e:
            messageResponse = SimpleErrorMessage(e.message)
        except Exception as e:
            messageResponse = SimpleErrorMessage("Internal Server Error")

        return self._encode(Serializer(messageResponse).serialize())

    def _decode(self, data: bytes) -> str:
        return data.decode()

    def _encode(self, data: str) -> bytes:
        return data.encode()