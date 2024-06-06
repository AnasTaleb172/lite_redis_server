import unittest

from app.factories.commandHandlerFactory import CommandHandlerFactory
from app.services import commandHandler
from db.dbAdapter import LocalDbAdapter
from app.exceptions import FunctionalException

class TestCommandHandlerFactory(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_isPingCommand(self):
        self.assertIsInstance(CommandHandlerFactory.create_command_handler_by_text(LocalDbAdapter(), ["ping"]), commandHandler.PingCommandHandler)

    def test_isEchoCommand(self):
        self.assertIsInstance(CommandHandlerFactory.create_command_handler_by_text(LocalDbAdapter(), ["echo"]), commandHandler.EchoCommandHandler)

    def test_isSetCommand(self):
        self.assertIsInstance(CommandHandlerFactory.create_command_handler_by_text(LocalDbAdapter(), ["set"]), commandHandler.SetCommandHandler)

    def test_isGetCommand(self):
        self.assertIsInstance(CommandHandlerFactory.create_command_handler_by_text(LocalDbAdapter(), ["get"]), commandHandler.GetCommandHandler)

    def test_notValidCommandString(self):
        with self.assertRaises(FunctionalException) as ex:
            CommandHandlerFactory.create_command_handler_by_text(LocalDbAdapter(), ["test"])
        self.assertEqual(ex.exception.message, 'Command handler has invalid text!!')

    def test_EmptyCommand(self):
        with self.assertRaises(FunctionalException) as ex:
            CommandHandlerFactory.create_command_handler_by_text(LocalDbAdapter(), [])
        self.assertEqual(ex.exception.message, 'Not valid Command')

if __name__ == "__main__":
    unittest.main()
