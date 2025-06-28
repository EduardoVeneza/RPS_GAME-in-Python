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
    
    def get_RPS_Values(self) -> tuple:
        return (self.RPS.ROCK.value, self.RPS.PAPER.value, self.RPS.SCISSORS.value)
    
    def get_menu() -> str: 
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
        self.name_choice_dict = {}
        self.who_win = {}

    def start_server(self) -> None:
        self.server.bind((self.host, self.port))    
        self.server.listen(1)
        print(f'Servidor Iniciado em ({self.host}, {self.port})')

        while True:
            conn, addr = self.server.accept()
            if len(self.players) >= 2:
                conn.send(b'SERVER_FULL') # This is going to be the key string to stop the client
                continue
            
            # Catch de nickname
            print(f'{addr} se conectou no jogo!')
            conn.send(b'Digite seu nick: ')
            # Player is going to send the nickname from client
            name = conn.recv(1024).decode()

            player = Player(conn, addr) # Jogador temporário para receber o socket OBJ e ip
            player.name = name

            # Adicionando jogador a lista de jogadores
            self.players.append(player)

            # Dando boas vindas
            conn.send(f"Olá! {player.name}, obrigado por se conectar ao RPS_GAME!".encode())

            thread = threading.Thread(target=self.handle_player, args=(player,))
            thread.start()

    def handle_player(self, player: Player):
        while True:
            if len(self.players) == 1:
                continue
            else:
                player.send_to_player("Jogo pronto! Outro jogador se conectou!")
                break

        player.send_to_player(Game.get_menu())
        try:
            player.choice = int(player.conn.recv(1024).decode())
        except (ConnectionResetError, ValueError):
            print(f"Jogador {player.name} desconectou ou enviou valor inválido.")
            # for p in self.players:
            #     if p.name == player.name:
            #         self.players.remove(p)
            player.exit()
            return

        if player.choice not in [rps.value for rps in Game.RPS]:
            player.exit()
            return
        
        self.name_choice_dict[player.name] = player.choice

        while self.name_choice_dict.__len__() < 2:
            continue
        
        choices = f'''
        {self.players[0].name} -> {self.name_choice_dict.get(self.players[0].name)}\n
        {self.players[1].name} -> {self.name_choice_dict.get(self.players[1].name)}\n
        '''
        print(choices)
        player.send_to_player(choices)

        if self.players[0].name == player.name:
            self.who_win = compare_choices(self.players[0], self.players[1], Game)
        
        if self.who_win[player.name]:
            player.send_to_player("Congrats! You Win 🥳")
        else:
            player.send_to_player("You lost! 😓")


def compare_choices(player1: Player, player2: Player, game: Game) -> dict:
    rock_value, paper_value, scissors_value = game.get_RPS_Values()
    
    player1_wins = (player1.choice == rock_value and player2.choice == scissors_value) or (player1.choice == paper_value and player2.choice == rock_value) or (player1.choice == scissors_value and player2.choice == paper_value)
    if player1_wins:
        return {player1.name : True, player2.name : False}
    else: 
        return {player1.name : False, player2.name : True}


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