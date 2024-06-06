import unittest

from app.services.deserializer import Deserializer
from app.exceptions import (
    MessageNotStringException,
    MessageEmptyException,
    NotValidMessageFormatException,
)


class TestDeserialization(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_messageNotStringRaisesException(self):
        self.assertRaises(MessageNotStringException, Deserializer, 33)

    def test_messageEmptyRaisesException(self):
        self.assertRaises(MessageEmptyException, Deserializer, "")

    def test_messageHasNoValidPrefixRaisesException(self):
        self.assertRaises(NotValidMessageFormatException, Deserializer, "(OK\r\n")


if __name__ == "__main__":
    unittest.main()
