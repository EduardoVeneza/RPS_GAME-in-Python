#Cliente do RPS
import socket
import threading

# 1. User is going to choose an IP and port to connect!
# 2. Client Receives from server the "Choose your nickname"
# 3. User choose his Nickname after that!
# 4. Client Receives a welcome message from server!
# 5. Client receives a message from server with the menu!
# 6. User make his choice!
# 7. Wait until both choose
# 8. Client get the choices from server
# 9. Client Reveives the notice if he wins or not

# thread = threading.Thread(target=self.handle_player, args=(player))
            # thread.start()

class Client():
    def __init__(self, server_ip, port) -> None:
        self.server_ip = server_ip
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self) -> None:
        try:
            self.client.connect((self.server_ip, self.port))
            print("Conectado ao servidor!")

            # if self.client.recv(1024) == "SERVER_FULL":
            #     print('Server Full')
            #     exit(1)
            #Criando uma thread para receber mensagens
            self.comunicate_to_server()

        except:
            print("Não foi possível conectar ao servidor")

    def comunicate_to_server(self) -> None:

        choose_nickname_message = self.receive() # Recebe do server
        print(choose_nickname_message)
        self.client.send(input().encode())

        welcome_message = self.receive() # Recebe do server
        print(welcome_message)
        while True:
            self.receive_and_print() # Menu
            user_choice = input("Choice: ")
            self.client.send(user_choice.encode())
            self.receive_and_print()
            self.receive_and_print()
            self.receive_and_print()
            self.receive_and_print()
            self.receive_and_print()
            self.receive_and_print()
            

    def receive(self):
        return self.client.recv(1024).decode()
    
    def receive_and_print(self):
        server_package = self.receive()
        print(server_package)

    def send(self, message):
        message.encode()
        self.client.send(message)


if __name__ == "__main__":
    server_ip = input("Server IP: ")
    port = int(input("Server Port: "))
    client = Client(server_ip, port)
    client.connect()