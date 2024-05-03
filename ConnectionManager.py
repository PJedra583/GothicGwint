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
        self.player1_turn = None
        self.player2_turn = None
        self.all_Cards = None
        self.cardInstance = Card.getInstance()
        self.start = 1
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

        #Battle row
        self.player1_frontRow = []
        self.player1_middleRow = []
        self.player1_backRow = []

        self.player2_frontRow = []
        self.player2_middleRow = []
        self.player2_backRow = []


    def start_server(self):
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5)
        self.cardInstance.load_cards()
        self.all_Cards = self.cardInstance.getSortedDeck()
        self.PrepareGame()
        while True:
            client_socket, client_address = self.server_socket.accept()
            client_thread = Thread(target=self.handle_client, args=(client_socket,len(self.client_threads)))
            self.client_threads.append(client_thread)
            client_thread.start()

    def handle_client(self, client_socket,counter):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode("utf-8")
              #  print("Zapytanie od gracza " + str(counter) + message)
                if message == "Hello\n":
                    self.start = 2
                elif message == "GetMyTurn\n":
                    if counter == 1:
                        client_socket.send((str(self.player1_turn) + "\n").encode("utf-8"))
                    if counter == 2:
                        client_socket.send((str(self.player2_turn) + "\n").encode("utf-8"))
                elif message == "GetOppCardsLength\n":
                    print(str(len(self.player2_cards)) + " || " + str(len(self.player1_cards)))
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
                elif message == "GetMyHP\n":
                    if counter == 1:
                        client_socket.send((str(self.player1_lifes) + "\n").encode("utf-8"))
                    if counter == 2:
                        client_socket.send((str(self.player2_lifes) + "\n").encode("utf-8"))
                elif message == "GetOppHP\n":
                    if counter == 1:
                        client_socket.send((str(self.player2_lifes) + "\n").encode("utf-8"))
                    if counter == 2:
                        client_socket.send((str(self.player1_lifes) + "\n").encode("utf-8"))
                elif message[0] == "M":
                    #rzucanie karty
                    card_id = int(message.split(";")[1])
                    row = message.split(";")[2]
                    if counter == 1:
                        self.player1_cards.remove(self.all_Cards[card_id])
                        if row == "f":
                            self.player1_frontRow.append(self.all_Cards[card_id])
                        elif row == "m":
                            self.player1_middleRow.append(self.all_Cards[card_id])
                        elif row == "b":
                            self.player1_backRow.append(self.all_Cards[card_id])
                    if counter == 2:
                        self.player2_cards.remove(self.all_Cards[card_id])
                        if row == "f":
                            self.player2_frontRow.append(self.all_Cards[card_id])
                        elif row == "m":
                            self.player2_middleRow.append(self.all_Cards[card_id])
                        elif row == "b":
                            self.player2_backRow.append(self.all_Cards[card_id])
                    if self.player1_turn == 1:
                        self.player1_turn = 0
                        self.player2_turn = 1
                    else:
                        self.player1_turn = 1
                        self.player2_turn = 0
                    client_socket.send(("OK\n").encode("utf-8"))
                elif message == "GetMyFrontRow\n":
                    if counter == 1:
                        s = self.get_cards_as_string(self.player1_frontRow)
                        client_socket.send((s + "\n").encode("utf-8"))
                    if counter == 2:
                        s = self.get_cards_as_string(self.player2_frontRow)
                        client_socket.send((s + "\n").encode("utf-8"))
                elif message == "GetMyMiddleRow\n":
                    if counter == 1:
                        s = self.get_cards_as_string(self.player1_middleRow)
                        client_socket.send((s + "\n").encode("utf-8"))
                    if counter == 2:
                        s = self.get_cards_as_string(self.player2_middleRow)
                        client_socket.send((s + "\n").encode("utf-8"))
                elif message == "GetMyBackRow\n":
                    if counter == 1:
                        s = self.get_cards_as_string(self.player1_backRow)
                        client_socket.send((s + "\n").encode("utf-8"))
                    if counter == 2:
                        s = self.get_cards_as_string(self.player2_backRow)
                        client_socket.send((s + "\n").encode("utf-8"))

                elif message == "GetOppFrontRow\n":
                    if counter == 2:
                        s = self.get_cards_as_string(self.player1_frontRow)
                        client_socket.send((s + "\n").encode("utf-8"))
                    if counter == 1:
                        s = self.get_cards_as_string(self.player2_frontRow)
                        client_socket.send((s + "\n").encode("utf-8"))
                elif message == "GetOppMiddleRow\n":
                    if counter == 2:
                        s = self.get_cards_as_string(self.player1_middleRow)
                        client_socket.send((s + "\n").encode("utf-8"))
                    if counter == 1:
                        s = self.get_cards_as_string(self.player2_middleRow)
                        client_socket.send((s + "\n").encode("utf-8"))
                elif message == "GetOppBackRow\n":
                    if counter == 1:
                        s = self.get_cards_as_string(self.player2_backRow)
                        client_socket.send((s + "\n").encode("utf-8"))
                    if counter == 2:
                        s = self.get_cards_as_string(self.player1_backRow)
                        client_socket.send((s + "\n").encode("utf-8"))
                elif message == "GetMyScore\n":
                    if counter == 1:
                        self.player1_score = self.calculate_power(1)
                        s = str(self.player1_score)
                        client_socket.send((s + "\n").encode("utf-8"))
                    if counter == 2:
                        self.player2_score = self.calculate_power(2)
                        s = str(self.player2_score)
                        client_socket.send((s + "\n").encode("utf-8"))
                elif message == "GetOppScore\n":
                    if counter == 1:
                        self.player2_score = self.calculate_power(2)
                        s = str(self.player2_score)
                        client_socket.send((s + "\n").encode("utf-8"))
                    if counter == 2:
                        self.player1_score = self.calculate_power(1)
                        s = str(self.player1_score)
                        client_socket.send((s + "\n").encode("utf-8"))
                else:
                    client_socket.send("Wrong Message\n".encode("utf-8"))

        except Exception as e:
            print("Server excp: " + str(e))
        finally:
            client_socket.close()
    def PrepareGame(self):
        #tossing the coin
        coin = random.randint(0, 1)
        if coin == 1:
            self.player1_turn = 0
            self.player2_turn = 1
        else:
            self.player1_turn = 1
            self.player2_turn = 0

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

    def get_cards_as_string(self, card_list):
        s = ""
        for card in card_list:
            s += str(card.id) + ";"
        return s

    def calculate_power(self,counter):
        sum = 0
        if counter == 1:
            for card in self.player1_frontRow:
                sum += card.power
            for card in self.player1_middleRow:
                sum += card.power
            for card in self.player1_backRow:
                sum += card.power
        if counter == 2:
            for card in self.player2_frontRow:
                sum += card.power
            for card in self.player2_middleRow:
                sum += card.power
            for card in self.player2_backRow:
                sum += card.power
        return sum