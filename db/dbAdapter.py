from abc import ABC, abstractmethod

from db.database import Database, LocalDatabase, TTLDatabase
from app.interfaces.commandOption import CommandOption
from app.exceptions import FunctionalException

class DbAdapter(ABC):
    def __init__(self, db: Database) -> None:
        self.db = db
        super().__init__()

    @abstractmethod
    def get(self, key):
        return
    
    @abstractmethod
    def set(self, key, value):
        return

    @abstractmethod
    def delete(self, key):
        return
    
    @abstractmethod
    def exists(self, key) -> bool:
        return

class LocalDbAdapter(DbAdapter):
    def __init__(self) -> None:
        super().__init__(LocalDatabase())

    def get(self, key) -> str | None:
        value, options = self.db.repo.get(key) or (None, [])

        # apply conditional command options
        for option in options or []:
            condition = option.execute()
            if not condition:
                value = None
                self.delete(key)
                break

        return value
    
    def set(self, key, value, options: list[CommandOption] = []):
        self.db.repo[key] = (value, options)
        return True
    
    def delete(self, key):
        try:
            del self.db.repo[key]
            return True
        except KeyError as e:
            return False

    def exists(self, key) -> bool:
        return bool(self.db.repo.get(key))
    
class TTLDbAdapter(DbAdapter):
    def __init__(self) -> None:
        super().__init__(TTLDatabase())

    def get(self, key):
        value, _ = self.db.repo.get(key) or (None, [])
        return value
    
    def set(self, key, value, options: list[CommandOption] = []):
        self.db.repo[key] = (value, options)
        return True

    def delete(self, key):
        try:
            del self.db.repo[key]
            return True
        except KeyError as e:
            return False

    def exists(self, key) -> bool:
        return bool(self.db.repo.get(key))
