import unittest
import time

from app.services import commandHandler
from app.entities import (simpleStringMessage, bulkStringMessage, integerMessage)
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

    def test_GetHandleNegativeValue(self):
        # set first
        setter = commandHandler.SetCommandHandler(self.dbAdapter, "x", "-5")
        setter.handle()

        handler = commandHandler.GetCommandHandler(self.dbAdapter, "x")
        self.assertEqual(handler.handle().serialize(), bulkStringMessage.BulkStringMessage("-5").serialize())

    def test_GetHandleNegativeOne(self):
        # set first
        setter = commandHandler.SetCommandHandler(self.dbAdapter, "x", "-1")
        setter.handle()

        handler = commandHandler.GetCommandHandler(self.dbAdapter, "x").handle()
        self.assertEqual(handler.serialize(), bulkStringMessage.BulkStringMessage("-1").serialize())

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

    def test_existsHandle(self):
        # set first
        handler = commandHandler.SetCommandHandler(self.dbAdapter, "x", "5")
        handler.handle()

        exister = commandHandler.ExistsCommandHandler(self.dbAdapter, "x")
        self.assertTrue(exister.handle().serialize(), integerMessage.IntegerMessage(1).serialize())

    def test_notExistsHandle(self):
        exister = commandHandler.ExistsCommandHandler(self.dbAdapter, "x")
        self.assertEqual(exister.handle().serialize(), integerMessage.IntegerMessage(0).serialize())

    def test_multipleExistsHandle(self):
        # set first
        commandHandler.SetCommandHandler(self.dbAdapter, "x", "5").handle()
        commandHandler.SetCommandHandler(self.dbAdapter, "y", "10").handle()
        commandHandler.SetCommandHandler(self.dbAdapter, "z", "15").handle()

        handler = commandHandler.ExistsCommandHandler(self.dbAdapter, "x", "y", "z").handle()
        self.assertEqual(handler.serialize(), integerMessage.IntegerMessage(3).serialize())

    def test_multipleExistsAndNotHandle(self):
        # set first
        commandHandler.SetCommandHandler(self.dbAdapter, "x", "5").handle()

        handler = commandHandler.ExistsCommandHandler(self.dbAdapter, "x", "y", "z").handle()
        self.assertEqual(handler.serialize(), integerMessage.IntegerMessage(1).serialize())

    def test_delHandle(self):
        # set first
        commandHandler.SetCommandHandler(self.dbAdapter, "x", "5").handle()

        deleter = commandHandler.DelCommandHandler(self.dbAdapter, "x").handle()
        self.assertEqual(deleter.serialize(), integerMessage.IntegerMessage(1).serialize())

    def test_multipleDelHandle(self):
        # set first
        commandHandler.SetCommandHandler(self.dbAdapter, "x", "5").handle()
        commandHandler.SetCommandHandler(self.dbAdapter, "y", "5").handle()
        commandHandler.SetCommandHandler(self.dbAdapter, "z", "5").handle()

        deleter = commandHandler.DelCommandHandler(self.dbAdapter, "x", "y", "z").handle()
        self.assertEqual(deleter.serialize(), integerMessage.IntegerMessage(3).serialize())

    def test_multipleDelHandle_mix_exists_and_not(self):
        # set first
        commandHandler.SetCommandHandler(self.dbAdapter, "x", "5").handle()
        commandHandler.SetCommandHandler(self.dbAdapter, "y", "5").handle()

        deleter = commandHandler.DelCommandHandler(self.dbAdapter, "x", "y", "z").handle()
        self.assertEqual(deleter.serialize(), integerMessage.IntegerMessage(2).serialize())

    def test_delNotExistHandle(self):
        # set first
        commandHandler.SetCommandHandler(self.dbAdapter, "x", "5").handle()

        deleter = commandHandler.DelCommandHandler(self.dbAdapter, "y").handle()
        self.assertEqual(deleter.serialize(), integerMessage.IntegerMessage(0).serialize())

    def test_incrHandle(self):
        # set first
        commandHandler.SetCommandHandler(self.dbAdapter, "x", 3).handle()
        incrementer = commandHandler.IncrCommandHandler(self.dbAdapter, "x").handle()

        self.assertEqual(incrementer.serialize(), integerMessage.IntegerMessage(4).serialize())

    def test_incrHandleNotExist(self):
        incrementer = commandHandler.IncrCommandHandler(self.dbAdapter, "x").handle()
        self.assertEqual(incrementer.serialize(), integerMessage.IntegerMessage(1).serialize())

    def test_incrHandleNotExistThenStore(self):
        commandHandler.IncrCommandHandler(self.dbAdapter, "x").handle()
        getter = commandHandler.GetCommandHandler(self.dbAdapter, "x").handle()
        self.assertEqual(getter.serialize(), bulkStringMessage.BulkStringMessage("1").serialize())

    def test_incrHandleNotIntButNumeric(self):
        # set first
        commandHandler.SetCommandHandler(self.dbAdapter, "x", "1").handle()
        incrementer = commandHandler.IncrCommandHandler(self.dbAdapter, "x").handle()

        self.assertEqual(incrementer.serialize(), integerMessage.IntegerMessage(2).serialize())

    def test_incrHandleNotNumeric(self):
        commandHandler.SetCommandHandler(self.dbAdapter, "x", "YY").handle()
        incrementer = commandHandler.IncrCommandHandler(self.dbAdapter, "x")

        with self.assertRaises(FunctionalException) as ex:
            incrementer.handle()
        self.assertEqual(ex.exception.message, "Stored value is not int")

    def test_decrHandle(self):
        # set first
        commandHandler.SetCommandHandler(self.dbAdapter, "x", 3).handle()
        decrementer = commandHandler.DecrCommandHandler(self.dbAdapter, "x").handle()

        self.assertEqual(decrementer.serialize(), integerMessage.IntegerMessage(2).serialize())

    def test_decrHandleNotExist(self):
        decrementer = commandHandler.DecrCommandHandler(self.dbAdapter, "x").handle()
        self.assertEqual(decrementer.serialize(), integerMessage.IntegerMessage(-1).serialize())

    def test_decrHandleNotExistThenStore(self):
        commandHandler.DecrCommandHandler(self.dbAdapter, "x").handle()
        getter = commandHandler.GetCommandHandler(self.dbAdapter, "x").handle()
        self.assertEqual(getter.serialize(), bulkStringMessage.BulkStringMessage("-1").serialize())

    def test_decrHandleNotIntButNumeric(self):
        # set first
        commandHandler.SetCommandHandler(self.dbAdapter, "x", "2").handle()
        decrementer = commandHandler.DecrCommandHandler(self.dbAdapter, "x").handle()

        self.assertEqual(decrementer.serialize(), integerMessage.IntegerMessage(1).serialize())

    def test_decrHandleNotNumeric(self):
        commandHandler.SetCommandHandler(self.dbAdapter, "x", "YY").handle()
        decrementer = commandHandler.DecrCommandHandler(self.dbAdapter, "x")

        with self.assertRaises(FunctionalException) as ex:
            decrementer.handle()
        self.assertEqual(ex.exception.message, "Stored value is not int")

    def test_lpushHandle(self):
        commandHandler.LpushCommandHandler(self.dbAdapter, "x", 1, 2, 3).handle()
        self.assertEqual(self.dbAdapter.get("x"), [3,2,1])

    def test_lpushHandleAlreadyExists(self):
        commandHandler.LpushCommandHandler(self.dbAdapter, "x", 1, 2, 3).handle()
        commandHandler.LpushCommandHandler(self.dbAdapter, "x", 4, 5, 6).handle()
        self.assertEqual(self.dbAdapter.get("x"), [6,5,4,3,2,1])

    def test_lpushHandleAlreadyExistsButNotList(self):
        commandHandler.SetCommandHandler(self.dbAdapter, "x", 1).handle()
        handler = commandHandler.LpushCommandHandler(self.dbAdapter, "x", 4, 5, 6)

        with self.assertRaises(FunctionalException) as ex:
            handler.handle()
        self.assertEqual(ex.exception.message, "WRONGTYPE Operation against a key holding the wrong kind of value")

    def test_rpushHandle(self):
        commandHandler.RpushCommandHandler(self.dbAdapter, "x", 1, 2, 3).handle()
        self.assertEqual(self.dbAdapter.get("x"), [1,2,3])

    def test_rpushHandleAlreadyExists(self):
        commandHandler.RpushCommandHandler(self.dbAdapter, "x", 1, 2, 3).handle()
        commandHandler.RpushCommandHandler(self.dbAdapter, "x", 4,5,6).handle()
        self.assertEqual(self.dbAdapter.get("x"), [1,2,3,4,5,6])

    def test_rpushHandleAlreadyExistsButNotList(self):
        commandHandler.SetCommandHandler(self.dbAdapter, "x", 1).handle()
        handler = commandHandler.RpushCommandHandler(self.dbAdapter, "x", 4, 5, 6)

        with self.assertRaises(FunctionalException) as ex:
            handler.handle()
        self.assertEqual(ex.exception.message, "WRONGTYPE Operation against a key holding the wrong kind of value")


