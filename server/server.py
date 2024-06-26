
"""
This module is the entry point of the application.
"""

import socket
import selectors

from server.handlers.requestHandler import RequestHandler
from db.dbAdapter import DbAdapter, LocalDbAdapter

class RedisServer:
    """
    This class is the TCP server that handles socket initialization and concurrency.
    """
    def __init__(self, dbAdapter: DbAdapter, host='127.0.0.1', port=6380):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.selector = selectors.DefaultSelector()
        self.dbAdapter = dbAdapter
        self.requestHandler = RequestHandler(self.dbAdapter)
        self.connectionsCount = 0

    def start(self):
        """Runs the server to start listening to incoming requests."""

        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.sock.setblocking(False)
        self.selector.register(self.sock, selectors.EVENT_READ, data=None)

        print(f"Redis server listening on {self.host}:{self.port}")

        try:
            while True:
                events = self.selector.select()
                for key, mask in events:
                    if key.data is None:
                        self.accept_connection(key.fileobj)
                        self.connectionsCount += 1
                    else:
                        self.serve_connection(key, mask)
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
            print(f"Total # of connections: {self.connectionsCount}")
        finally:
            self.sock.close()

    def _handle_data(self, data: bytes) -> bytes:
        """Calls the request handler and returns the handled data."""

        return self.requestHandler.handle(data)

    def accept_connection(self, sock: socket.socket):
        """Accepts the connection and register it in the global selector."""

        conn, addr = sock.accept()
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        self.selector.register(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, data=b'')

    def serve_connection(self, key, mask):
        """Handles a connection in case of the socket is ready to read or write."""

        sock: socket.socket = key.fileobj
        data = key.data

        # Socket is ready to read -> Receive from buffer & Write to socket
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)
            if recv_data and recv_data != b'*2\r\n$7\r\nCOMMAND\r\n$4\r\nDOCS\r\n':
                data += recv_data
            else:
                self.selector.unregister(sock)
                sock.close()

        # Socket is ready to write -> Read from socket & send to buffer
        if mask & selectors.EVENT_WRITE:
            if data:
                handledData = self._handle_data(data)
                sent = sock.send(handledData)
                data = data[sent:]

if __name__ == "__main__":
    server = RedisServer(dbAdapter=LocalDbAdapter())
    server.start()
