import unittest

from app.exceptions import FunctionalException
from db.dbAdapter import LocalDbAdapter, TTLDbAdapter
from db.database import TTLDatabase
from app.entities.commandOption import EXCommandOption
import threading
import time

class TestLocalDBAdapter(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = LocalDbAdapter()
        return super().setUp()
    
    def test_setAndGet(self):
        self.adapter.set("x", 5)
        self.assertEqual(self.adapter.get("x"), 5)

    def test_setWithOptions(self):
        options = [
            EXCommandOption(10)
        ]
        self.adapter.set("x", 5, options)

        self.assertEqual(self.adapter.get("x"), 5)

    def test_setAndGetWithExpiredOptions(self):
        options = [
            EXCommandOption(0)
        ]
        self.adapter.set("x", 5, options)

        self.assertEqual(self.adapter.get("x"), None)

    def test_delete(self):
        self.adapter.set("x", 5)
        deleted = self.adapter.delete("x")

        self.assertEqual(self.adapter.get("x"), None)
        self.assertTrue(deleted)

    def test_deleteNotExistingKey(self):
        self.assertFalse(self.adapter.delete("x"))


class TestTTLDB(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_ttlDB(self):
        db = TTLDatabase()
        cmd = EXCommandOption(10)
        db.repo['x'] = (10, [cmd])

        self.assertEqual(db.repo.get("x"), (10, [cmd]))

    # def test_ttlDBAsExpiredKey(self):
    #     db = TTLDatabase()
    #     cmd = EXCommandOption(0)
    #     db.repo['x'] = (10, [cmd])

    #     self.assertEqual(db.repo.get("x"), None)
    
class TestTTLDBAdapter(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = TTLDbAdapter()
        return super().setUp()
    
    def test_setAndGet(self):
        self.adapter.set("x", 5)
        self.assertEqual(self.adapter.get("x"), 5)

    def test_setWithOptions(self):
        options = [
            EXCommandOption(10)
        ]
        self.adapter.set("x", 5, options)

        self.assertEqual(self.adapter.get("x"), 5)

    # def test_setAndGetWithExpiredOptions(self):
    #     options = [
    #         EXCommandOption(0)
    #     ]
    #     self.adapter.set("x", 5, options)

    #     self.assertEqual(self.adapter.get("x"), None)

    def test_delete(self):
        self.adapter.set("x", 5)
        self.adapter.delete("x")

        self.assertEqual(self.adapter.get("x"), None)

    def test_deleteNotExistingKey(self):
        self.assertFalse(self.adapter.delete("x"))