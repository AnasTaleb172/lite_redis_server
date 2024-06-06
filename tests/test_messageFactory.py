import unittest

from app.factories.messageFactory import MessageFactory
from app.entities import simpleStringMessage, bulkStringMessage


class TestMessageFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.factory = MessageFactory()
        return super().setUp()

    def test_isSimpleStringMessageType(self):

        self.assertIsInstance(
            self.factory.create_message_by_text("+OK\r\n"),
            simpleStringMessage.SimpleStringMessage,
        )

    def test_isBulkStringMessageType(self):
        self.assertIsInstance(
            self.factory.create_message_by_text("$3\r\nkey\r\n"),
            bulkStringMessage.BulkStringMessage,
        )

    def tearDown(self) -> None:
        return super().tearDown()
