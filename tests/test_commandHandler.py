import unittest
import time

from app.services import commandHandler
from app.entities import (simpleStringMessage, bulkStringMessage)
from db.dbAdapter import LocalDbAdapter, TTLDbAdapter
from app.exceptions import FunctionalException

class TestCommandHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.dbAdapter = LocalDbAdapter()
        return super().setUp()

    def test_PingHandle(self):
        handler = commandHandler.PingCommandHandler(self.dbAdapter, [])
        self.assertEqual(handler.handle().serialize(), simpleStringMessage.SimpleStringMessage("PONG").serialize())

    def test_EchoHandle(self):
        handler = commandHandler.EchoCommandHandler(self.dbAdapter, "hello", "world")
        self.assertEqual(handler.handle().serialize(), bulkStringMessage.BulkStringMessage("hello world").serialize())

    def test_GetHandle(self):
        # set first
        setter = commandHandler.SetCommandHandler(self.dbAdapter, "x", "5")
        setter.handle()

        handler = commandHandler.GetCommandHandler(self.dbAdapter, "x")
        self.assertEqual(handler.handle().serialize(), bulkStringMessage.BulkStringMessage("5").serialize())

    def test_NotValidGetHandleCommandArguments(self):
        handler = commandHandler.GetCommandHandler(self.dbAdapter)
        with self.assertRaises(FunctionalException) as ex:
            handler.handle()
        self.assertEqual(ex.exception.message, "Not valid command arguments length")

    def test_SetHandle(self):
        handler = commandHandler.SetCommandHandler(self.dbAdapter, "x", "5")
        handler.handle()

        # get first
        getter = commandHandler.GetCommandHandler(self.dbAdapter, "x")
        self.assertEqual(getter.handle().serialize(), bulkStringMessage.BulkStringMessage("5").serialize())

        self.assertEqual(handler.handle().serialize(), simpleStringMessage.SimpleStringMessage("OK").serialize())

    def test_NotValidSetHandleCommandArguments(self):
        handler = commandHandler.SetCommandHandler(self.dbAdapter)
        with self.assertRaises(FunctionalException) as ex:
            handler.handle()
        self.assertEqual(ex.exception.message, 'Not valid command arguments length')

    def test_SetHandleWithOptions(self):
        handler = commandHandler.SetCommandHandler(self.dbAdapter, "x", "5", "EX", 5)
        handler.handle()

        # sleep
        time.sleep(4)

        # get first
        getter = commandHandler.GetCommandHandler(self.dbAdapter, "x")
        self.assertEqual(getter.handle().serialize(), bulkStringMessage.BulkStringMessage("5").serialize())

        self.assertEqual(handler.handle().serialize(), simpleStringMessage.SimpleStringMessage("OK").serialize())

    def test_SetHandleWithExpiredSecOptions(self):
        handler = commandHandler.SetCommandHandler(self.dbAdapter, "x", "5", "EXAT", 1716990969)
        handler.handle()

        # get first
        getter = commandHandler.GetCommandHandler(self.dbAdapter, "x")
        self.assertEqual(getter.handle().serialize(), bulkStringMessage.BulkStringMessage("nil").serialize())

        self.assertEqual(handler.handle().serialize(), simpleStringMessage.SimpleStringMessage("OK").serialize())

    def test_SetHandleWithNoOptionValue(self):
        handler = commandHandler.SetCommandHandler(self.dbAdapter, "x", "5", "EX")
        with self.assertRaises(FunctionalException) as ex:
            handler.handle()
        self.assertEqual(ex.exception.message, "Invalid command option arguments")