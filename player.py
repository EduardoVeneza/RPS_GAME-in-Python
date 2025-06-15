import socket

class Player:
    def __init__(self, conn: socket.socket, addr):
        self.choice: int
        self.name: str
        self.addr = addr
        self.conn = conn

    def send_to_player(self, message) -> None:
        self.conn.send(message.encode())

    def receive_from_player(self):
        return self.conn.recv(1024).decode()