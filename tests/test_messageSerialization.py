import unittest

from app.entities import (
    simpleStringMessage,
    bulkStringMessage,
    simpleErrorMessage,
    integerMessage,
)

from app import exceptions
from app.entities import arrayMessage


class TestSimpleStringMessage(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_serializeBaseCase(self):
        msg = simpleStringMessage.SimpleStringMessage("OK")
        self.assertEqual(msg.serialize(), "+OK\r\n")

    def test_serializeEmptyCase(self):
        msg = simpleStringMessage.SimpleStringMessage("")
        self.assertEqual(msg.serialize(), "+\r\n")

    def test_serializeNoneCase(self):
        msg = simpleStringMessage.SimpleStringMessage(None)
        self.assertRaises(exceptions.NotValidMessageFormatException, msg.serialize)

    def test_serializeNotStringCase(self):
        msg = simpleStringMessage.SimpleStringMessage(["1"])
        self.assertRaises(exceptions.NotValidMessageFormatException, msg.serialize)


class TestBulkStringMessage(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_serializeBaseCase(self):
        msg = bulkStringMessage.BulkStringMessage("key")
        self.assertEqual(msg.serialize(), "$3\r\nkey\r\n")

    def test_serializeEmptyCase(self):
        msg = bulkStringMessage.BulkStringMessage("")
        self.assertEqual(msg.serialize(), "$0\r\n\r\n")

    def test_serializeNullCase(self):
        msg = bulkStringMessage.BulkStringMessage(None)
        self.assertEqual(msg.serialize(), "$-1\r\n")

    def test_serializeMinusOneCase(self):
        msg = bulkStringMessage.BulkStringMessage("-1")
        self.assertEqual(msg.serialize(), "$2\r\n-1\r\n")

    def test_serializeNotStringCase(self):
        msg = bulkStringMessage.BulkStringMessage(["1"])
        self.assertRaises(exceptions.NotValidMessageFormatException, msg.serialize)


class TestSimpleErrorMessage(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_serializeBaseCase(self):
        msg = simpleErrorMessage.SimpleErrorMessage("Error message")
        self.assertEqual(msg.serialize(), "-Error message\r\n")

    def test_serializeNotStringCase(self):
        msg = simpleErrorMessage.SimpleErrorMessage(["1"])
        self.assertRaises(exceptions.NotValidMessageFormatException, msg.serialize)


class TestIntegerMessage(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_serializeBaseCase(self):
        msg = integerMessage.IntegerMessage(5)
        self.assertEqual(msg.serialize(), ":5\r\n")

    def test_serializeMinusCase(self):
        msg = integerMessage.IntegerMessage(-5)
        self.assertEqual(msg.serialize(), ":-5\r\n")

    def test_serializeNotIntCase(self):
        msg = integerMessage.IntegerMessage("UU")
        self.assertRaises(exceptions.NotValidMessageFormatException, msg.serialize)


class TestArrayMessage(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_serializeEmptyArrayCase(self):
        msg = arrayMessage.ArrayMessage([])
        self.assertEqual(msg.serialize(), "*0\r\n")

    def test_serializeNonEmptySimpleStringCase(self):
        msg = arrayMessage.ArrayMessage(["echo", "hello world"])
        self.assertEqual(msg.serialize(), "*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n")

    def test_serializeNonEmptyBulkStringCase(self):
        msg = arrayMessage.ArrayMessage(["hello", "world"])
        self.assertEqual(msg.serialize(), "*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n")

    def test_serializeNonEmptyIntegerCase(self):
        msg = arrayMessage.ArrayMessage([1, 2, 3])
        self.assertEqual(msg.serialize(), "*3\r\n:1\r\n:2\r\n:3\r\n")

    def test_serializeNonEmptyMixCase(self):
        msg = arrayMessage.ArrayMessage([1, 2, 3, 4, "hello"])
        self.assertEqual(
            msg.serialize(), "*5\r\n:1\r\n:2\r\n:3\r\n:4\r\n$5\r\nhello\r\n"
        )

    # def test_serializeNonEmptyNestedCase(self):
    #     msg = arrayMessage.ArrayMessage([[1, 2, 3], ["Hello", "World"]])
    #     self.assertEqual(
    #         msg.serialize(), "*2\r\n*3\r\n:1\r\n:2\r\n:3\r\n*2\r\n+Hello\r\n-World\r\n"
    #     )

    def test_serializeNullArrayCase(self):
        msg = arrayMessage.ArrayMessage(None)
        self.assertEqual(msg.serialize(), "*-1\r\n")

    def test_serializeNullElementsCase(self):
        msg = arrayMessage.ArrayMessage(["hello", None, "world"])
        self.assertEqual(msg.serialize(), "*3\r\n$5\r\nhello\r\n$-1\r\n$5\r\nworld\r\n")


if __name__ == "__main__":
    unittest.main()
