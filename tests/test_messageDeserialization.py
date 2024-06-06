import unittest

from app.entities import (
    simpleStringMessage,
    bulkStringMessage,
    simpleErrorMessage,
    integerMessage,
)
from app.entities import arrayMessage


class TestSimpleStringMessage(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_deserializeBaseCase(self):
        msg = simpleStringMessage.SimpleStringMessage("+OK\r\n")
        self.assertEqual(msg.deserialize(), "OK")


class TestBulkStringMessage(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_deserializeBaseCase(self):
        msg = bulkStringMessage.BulkStringMessage("$3\r\nkey\r\n")
        self.assertEqual(msg.deserialize(), "key")

    def test_deserializeEmptyCase(self):
        msg = bulkStringMessage.BulkStringMessage("$0\r\n\r\n")
        self.assertEqual(msg.deserialize(), "")

    def test_deserializeNullCase(self):
        msg = bulkStringMessage.BulkStringMessage("$-1\r\n")
        self.assertEqual(msg.deserialize(), None)


class TestSimpleErrorMessage(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_deserializeBaseCase(self):
        msg = simpleErrorMessage.SimpleErrorMessage("-Error message\r\n")
        self.assertEqual(msg.deserialize(), "Error message")


class TestIntegerMessage(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_deserializeBaseCase(self):
        msg = integerMessage.IntegerMessage(":+5\r\n")
        self.assertEqual(msg.deserialize(), 5)

    def test_deserializeMinusCase(self):
        msg = integerMessage.IntegerMessage(":-5\r\n")
        self.assertEqual(msg.deserialize(), -5)


class TestArrayMessage(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_deserializeEmptyArrayCase(self):
        msg = arrayMessage.ArrayMessage("*0\r\n")
        self.assertEqual(msg.deserialize(), [])

    def test_deserializeNonEmptySimpleStringCase(self):
        msg = arrayMessage.ArrayMessage("*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n")
        self.assertEqual(msg.deserialize(), ["echo", "hello world"])

    def test_deserializeNonEmptyBulkStringCase(self):
        msg = arrayMessage.ArrayMessage("*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n")
        self.assertEqual(msg.deserialize(), ["hello", "world"])

    def test_deserializeNonEmptyIntegerCase(self):
        msg = arrayMessage.ArrayMessage("*3\r\n:1\r\n:2\r\n:3\r\n")
        self.assertEqual(msg.deserialize(), [1, 2, 3])

    def test_deserializeNonEmptyMixCase(self):
        msg = arrayMessage.ArrayMessage("*5\r\n:1\r\n:2\r\n:3\r\n:4\r\n$5\r\nhello\r\n")
        self.assertEqual(msg.deserialize(), [1, 2, 3, 4, "hello"])

    def test_deserializeNonEmptyNestedCase(self):
        msg = arrayMessage.ArrayMessage(
            "*2\r\n*3\r\n:1\r\n:2\r\n:3\r\n*2\r\n+Hello\r\n-World\r\n"
        )
        self.assertEqual(msg.deserialize(), [[1, 2, 3], ["Hello", "World"]])

    def test_deserializeNullArrayCase(self):
        msg = arrayMessage.ArrayMessage("*-1\r\n")
        self.assertEqual(msg.deserialize(), None)

    def test_deserializeNullElementsCase(self):
        msg = arrayMessage.ArrayMessage("*3\r\n$5\r\nhello\r\n$-1\r\n$5\r\nworld\r\n")
        self.assertEqual(msg.deserialize(), ["hello", None, "world"])


if __name__ == "__main__":
    unittest.main()
