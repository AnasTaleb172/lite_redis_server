from abc import ABC, abstractmethod

from .message import Message
from db.dbAdapter import DbAdapter

class CommandHandler(ABC):
    def __init__(self, dbAdapter: DbAdapter=None ,*args) -> None:
        self.dbAdapter = dbAdapter
        self.args = args
        self.options = []

    @abstractmethod
    def _set_options(self):
        return

    @abstractmethod
    def _execute_command(self):
        return

    @abstractmethod
    def handle(self) -> Message:
        return