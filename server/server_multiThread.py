import socket
import threading

from handlers.requestHandler import RequestHandler
from db.dbAdapter import DbAdapter, LocalDbAdapter, TTLDbAdapter

class RedisServer:
    def __init__(self, dbAdapter: DbAdapter=LocalDbAdapter, host='127.0.0.1', port=6381):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dbAdapter = dbAdapter
        self.requestHandler = RequestHandler(self.dbAdapter)
        self.noOfConnections = 0

    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        # self.sock.setblocking(False)

        # print(f"Redis server listening on {self.host}:{self.port}")

        try:
            while True:
                conn, addr = self.sock.accept()
                self.noOfConnections += 1
                threading.Thread(target=self.serve_connection, args=(conn, addr)).start()
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            self.sock.close()
            # print(f"# Of Connections: {self.noOfConnections}")
    
    def _handle_data(self, data: bytes) -> bytes:
        return self.requestHandler.handle(data)

    def serve_connection(self, conn, addr):
        # print(f"Accepted Connection From: {addr}")
        try:
            while True:
                recv_data = conn.recv(1024)
                if not (recv_data and recv_data != b'*2\r\n$7\r\nCOMMAND\r\n$4\r\nDOCS\r\n'): break
                
                handledData = self._handle_data(recv_data)
                sent = conn.send(handledData)
        finally:
            conn.close()
            # print(f"Closed Connection From: {addr}")

if __name__ == "__main__":
    server = RedisServer(dbAdapter=LocalDbAdapter())
    server.start()