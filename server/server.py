import socket
import selectors

from handlers.requestHandler import RequestHandler
from db.dbAdapter import DbAdapter, LocalDbAdapter, TTLDbAdapter

class RedisServer:
    def __init__(self, dbAdapter: DbAdapter, host='127.0.0.1', port=6379):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.selector = selectors.DefaultSelector()
        self.dbAdapter = dbAdapter
        self.requestHandler = RequestHandler(self.dbAdapter)

    def start(self):
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
                    else:
                        self.serve_connection(key, mask)
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            self.sock.close()
    
    def _handle_data(self, data: bytes) -> bytes:
        return self.requestHandler.handle(data)
        
    def accept_connection(self, sock: socket.socket):
        conn, addr = sock.accept()
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        self.selector.register(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, data=b'')

    def serve_connection(self, key, mask):
        sock: socket.socket = key.fileobj
        data = key.data

        # Socket is ready to read -> Receive from buffer & Write to socket
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)
            if recv_data and recv_data != b'*2\r\n$7\r\nCOMMAND\r\n$4\r\nDOCS\r\n':
                print(f"Received data: {recv_data}")
                data += recv_data
            else:
                print(f"Closing connection to ....")
                self.selector.unregister(sock)
                sock.close()

        # Socket is ready to write -> Read from socket & send to buffer
        if mask & selectors.EVENT_WRITE:
            if data:
                print(f"Responding To a client ....")
                handledData = self._handle_data(data)
                print(f"Handled data: {handledData}")
                sent = sock.send(handledData)
                data = data[sent:]

if __name__ == "__main__":
    server = RedisServer(dbAdapter=TTLDbAdapter())
    server.start()