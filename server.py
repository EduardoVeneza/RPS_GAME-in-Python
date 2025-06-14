import socket
import threading
from enum import Enum
import sys

# Holds the game Logic
class Game:
    class RPS(Enum):
        ROCK = 1
        PAPER = 2
        SCISSORS = 3

    def __init__(self):
        pass
    
    def show_menu(self) -> None: 
        title = " ROCK, PAPER AND SCISSORS "
        print(title.center(54, "="))
        menu = f'''Please, enter the respective number:
        1 - ROCK
        2 - PAPER
        3 - SCISSORS
        [Another Number] - EXIT GAME'''
        print(menu)

    def verify_choice(choice: int) -> None:
        if choice < 1 or choice > 3:
            sys.exit()

    def run_game():
        pass

# Holds the game server
class Game_Server:
    def __init__(self, host = 'localhost', port = 5555) -> None:
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []  # Lista de clientes conectados

    def start_server(self) -> None:
        self.server.bind((self.host, self.port))    
        self.server.listen(1)
        print(f'Servidor Iniciado em ({self.host}, {self.port})')

        while True:
            conn, addr = self.server.accept()
            if len(self.clients) >= 2:
                conn.send(b'SERVER_FULL') # This is going to be the key string to stop the client
                continue

            print(f'{addr} se conectou no chat!')
            self.clients.append(conn)

            conn.send(f"Olá! {addr}, obrigado por se conectar ao RPS_GAME!".encode())

            thread = threading.Thread(target=self.handle_player, args=(conn, addr))
            thread.start()

    def handle_player(self, conn: socket.socket, addr):
        print(f'Thread para novo cliente iniciada. Cliente {addr}')

# Função que descobre o IPV4 da maquina e printa na dela
def get_local_ipv4():
    try:
        # Cria um socket UDP "falso" apenas para descobrir o IP real
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Conecta para um endereço qualquer (não precisa estar disponível)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return f"Erro ao obter IP: {e}"
        
if __name__ == "__main__":
    game_server = Game_Server(get_local_ipv4())
    game_server.start_server()