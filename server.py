import socket
import threading
from player import Player
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
    
    def get_menu(self) -> str: 
        menu = f'''
        /-/-/-/-/-/ ROCK PAPER SCISSOR /-/-/-/-/-/
        Please, enter the respective number:
        1 - ROCK
        2 - PAPER
        3 - SCISSORS
        [Another Number] - EXIT GAME'''
        return menu

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
        self.players: list[Player] = []  # Lista de jogadores conectados

    def start_server(self) -> None:
        self.server.bind((self.host, self.port))    
        self.server.listen(1)
        print(f'Servidor Iniciado em ({self.host}, {self.port})')

        while True:
            player = Player() # Jogador temporário para receber o socket OBJ e ip
            conn, addr = self.server.accept()
            if len(self.player) >= 2:
                conn.send(b'SERVER_FULL') # This is going to be the key string to stop the client
                continue
            
            # Catch de nickname
            print(f'{addr} se conectou no jogo!')
            conn.send(b'Digite seu nick: ')
            name = conn.recv(1024).decode()

            # Recebendo informações do jogador
            player.addr = addr
            player.conn = conn
            player.name = name

            # Adicionando jogador a lista de jogadores
            self.players.append(player)

            # Dando boas vindas
            conn.send(f"Olá! {player.name}, obrigado por se conectar ao RPS_GAME!".encode())

            thread = threading.Thread(target=self.handle_player, args=(player))
            thread.start()

    def handle_player(self, player: Player):
        while True:
            if len(self.players == 1):
                continue
            else:
                player.send_to_player("Jogo pronto!")
                break

        player.send_to_player(Game.get_menu())
        player_choice = player.receive_from_player()
        



# Função que descobre o IPV4
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