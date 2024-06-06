
from abc import ABC
import threading
import logging
import time

class Database(ABC):
    def __init__(self, repo):
        self.repo = repo

class LocalDatabase(Database):
    def __init__(self):
        super().__init__({})

class TTLDatabase(Database):
    def __init__(self):
        super().__init__({})

        # Logging
        logging.basicConfig(level=logging.INFO, filename='multi-thread.log', filemode='w', format='%(message)s')
        logging.getLogger( "SomeTest.testSomething" ).setLevel(logging.DEBUG)
        self.log = logging.getLogger("SomeTest.testSomething")

        self.lock = threading.Lock()
        self.run_ttl_thread()

    def run_ttl_thread(self):
        self.log.debug("run_ttl_thread")
        checkThread = threading.Thread(target=self.check_expired_key, name="CheckExpiredKeys")
        checkThread.daemon = True
        checkThread.start()

    def delete_expired_keys(self):
        self.log.debug("delete_expired_keys")
        with self.lock:
            self.log.debug("slef.lock")
            for key, (_, options) in list(self.repo.items()):
                for option in options:
                    condition = option.execute()
                    if not condition:
                        del self.repo[key]

    # checking expired keys function
    def check_expired_key(self):
        self.log.debug("check_expired_key")
        while True:
            self.delete_expired_keys()
            time.sleep(1)