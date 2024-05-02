import socket
import threading

from Card import Card
from threading import Thread

class ConnectionManager:
    def __init__(self, server_ip, port):
        self.ip = server_ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_threads = []
        self.turn = 1
        self.player1_card_obj =  Card(None, None, None, None)
        self.player2_card_obj =  Card(None, None, None, None)
        self.player1_cards = []
        self.player2_cards = []
        self.player1_hero = None
        self.player2_hero = None
        self.player1_lifes = 2
        self.player2_lifes = 2
        self.player1_score = 0
        self.player2_score = 0
        self.player1_isHeroActive = True
        self.player2_isHeroActive = True
    def start_server(self):
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5)
        while True:
            client_socket, client_address = self.server_socket.accept()
            client_thread = Thread(target=self.handle_client, args=(client_socket,len(self.client_threads)+1))
            self.client_threads.append(client_thread)
            client_thread.start()

    def handle_client(self, client_socket,counter):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode("utf-8")
                if message == "Hello\n":
                    self.turn = 2
                elif message == "GetOppCard\n":
                    if counter == 1 :
                        pass
                    if counter == 2 :
                        pass
        except Exception as e:
            print(e)
        finally:
            client_socket.close()
    def PrepareGame(self):
        self.player1_card_obj.load_cards()
        for i in range(10):
            self.player1_cards.append(self.player1_card_obj.getCard())
        self.player1_hero = self.player1_card_obj.getHeroCard()

        self.player2_card_obj.load_cards()
        for i in range(10):
            self.player2_cards.append(self.player2_card_obj.getCard())
        self.player2_hero = self.player2_card_obj.getHeroCard()
    def stop_server(self):
        for thread in self.client_threads:
            thread.join()
        self.server_socket.close()

    def get_turn(self):
        return self.turn
