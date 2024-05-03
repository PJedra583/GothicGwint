import socket
import threading
import random
from Card import Card
from threading import Thread

class ConnectionManager:
    def __init__(self, server_ip, port):
        self.ip = server_ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_threads = []
        self.turn = 1
        self.cardInstance = Card.getInstance()
        self.heroPool = []
        self.player1_card_Deck = []
        self.player2_card_Deck = []
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
        self.cardInstance.load_cards()
        self.PrepareGame()
        while True:
            client_socket, client_address = self.server_socket.accept()
            client_thread = Thread(target=self.handle_client, args=(client_socket,len(self.client_threads)))
            self.client_threads.append(client_thread)
            client_thread.start()

    def handle_client(self, client_socket,counter):
        try:
            while True:
                print("Zapytanie od gracza " + str(counter))
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode("utf-8")

                if message == "Hello\n":
                    self.turn = 2
                elif message == "Prepare\n":
                    self.PrepareGame()
                elif message == "GetOppCardsLength\n":
                    if counter == 1:
                        client_socket.send((str(len(self.player2_cards)) + "\n").encode("utf-8"))
                    if counter == 2:
                        client_socket.send((str(len(self.player1_cards)) + "\n").encode("utf-8"))

                elif message == "GetMyCards\n":
                    s = ""
                    if counter == 1:
                        for card in self.player1_cards:
                            s += str(card.id) + ";"
                        client_socket.send((s + "\n").encode("utf-8"))
                    if counter == 2:
                        for card in self.player2_cards:
                            s += str(card.id) + ";"
                        client_socket.send((s + "\n").encode("utf-8"))
                elif message == "GetMyHeroCard\n":
                    if counter == 1:
                        client_socket.send((str(self.player1_hero.id)+"\n").encode("utf-8"))
                    if counter == 2:
                        client_socket.send((str(self.player2_hero.id) + "\n").encode("utf-8"))
                elif message == "GetOppHeroCard\n":
                    if counter == 1:
                        client_socket.send((str(self.player2_hero.id)+"\n").encode("utf-8"))
                    if counter == 2:
                        client_socket.send((str(self.player1_hero.id) + "\n").encode("utf-8"))
                else:
                    client_socket.send("Wrong Message\n".encode("utf-8"))




        except Exception as e:
            print(e)
        finally:
            client_socket.close()
    def PrepareGame(self):
        for card in self.cardInstance.getDeck():
            self.player1_card_Deck.append(card)
            self.player2_card_Deck.append(card)

        random.shuffle(self.player1_card_Deck)
        random.shuffle(self.player2_card_Deck)

        for i in range(10):
            self.player1_cards.append(self.player1_card_Deck.pop())
            self.player2_cards.append(self.player2_card_Deck.pop())

        #przygotowanie bohaterów
        self.heroPool = Card.getInstance().getHeroes()

        random.shuffle(self.heroPool)
        self.player1_hero = self.heroPool[0]

        random.shuffle(self.heroPool)
        self.player2_hero = self.heroPool[0]


    def stop_server(self):
        for thread in self.client_threads:
            thread.join()
        self.server_socket.close()

    def get_turn(self):
        return self.turn
