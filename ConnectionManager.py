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
        self.all_Heroes = None
        self.cardInstance = Card.getInstance()
        self.start = 1
        self.heroPool = []
        self.player1_card_Deck = []
        self.player2_card_Deck = []
        self.player1_cards = []
        self.player2_cards = []
        self.player1_stack = []
        self.player2_stack = []
        self.player1_hero = None
        self.player2_hero = None
        self.player1_lifes = 2
        self.player2_lifes = 2
        self.player1_score = 0
        self.player2_score = 0
        self.player1_isHeroActive = "T"
        self.player2_isHeroActive = "T"

        self.player1_choosing = False
        self.player2_choosing = False
        self.player1_pass = False
        self.player2_pass = False
        #upgrades
        self.player1_upgrade_f = 0
        self.player2_upgrade_f = 0
        self.player1_upgrade_m = 0
        self.player2_upgrade_m = 0
        self.player1_upgrade_b = 0
        self.player2_upgrade_b = 0

        #multiply
        self.player1_multiply_f = 0
        self.player2_multiply_f = 0
        self.player1_multiply_m = 0
        self.player2_multiply_m = 0
        self.player1_multiply_b = 0
        self.player2_multiply_b = 0

        #Weather
        self.cold = 'F'
        self.rain = 'F'
        self.fog = 'F'
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
        self.all_Heroes = self.cardInstance.getHeroes()
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
                if message == "Hello\n":
                    self.start = 2
                elif message == "GetMyTurn\n":
                    if self.player1_pass and self.player2_pass:
                        self.player1_pass = False
                        self.player2_pass = False
                        self.endRound()
                    if counter == 1 :
                        client_socket.send((str(self.player1_turn) + "\n").encode("utf-8"))
                    if counter == 2 :
                        client_socket.send((str(self.player2_turn) + "\n").encode("utf-8"))
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
                    c = self.all_Cards[card_id]
                    if counter == 1:
                        self.checkAndRealiseEffects(1, card_id, row)
                        self.player1_cards.remove(c)
                        if c.type == "weather":
                            self.realiseWeather(c)
                        elif row == "f":
                            self.player1_frontRow.append(c)
                        elif row == "m":
                            self.player1_middleRow.append(c)
                        elif row == "b":
                            self.player1_backRow.append(c)
                    if counter == 2:
                        self.checkAndRealiseEffects(2, card_id, row)
                        self.player2_cards.remove(c)
                        if c.type == "weather":
                            self.realiseWeather(c)
                        elif row == "f":
                            self.player2_frontRow.append(c)
                        elif row == "m":
                            self.player2_middleRow.append(c)
                        elif row == "b":
                            self.player2_backRow.append(c)
                    if "heal" in c.effects:
                        client_socket.send(("Waiting\n").encode("utf-8"))
                    else:
                        if self.player1_turn == 1 and not self.player2_pass:
                                self.player1_turn = 0
                                self.player2_turn = 1
                        elif self.player2_turn == 1 and not self.player1_pass:
                                self.player1_turn = 1
                                self.player2_turn = 0
                        client_socket.send(("OK\n").encode("utf-8"))
                elif message[0] == "H":
                    c = self.all_Heroes[int(message.split(";")[1])]
                    if counter == 1:
                        self.player1_isHeroActive = 'F'
                        if c.name == "Hagen":
                            self.player1_multiply_f = 1
                        elif c.name == "Lee":
                            max = 0;
                            to_rem = []
                            for i in self.player2_middleRow:
                                if i.power > max:
                                    max = i.power
                            print("max = " + str(max))
                            for i in self.player2_middleRow:
                                if i.power == max:
                                    to_rem.append(i)
                            for i in to_rem:
                                self.player2_middleRow.remove(i)
                                self.player2_stack.append(i)
                        elif c.name == "Angar":
                            self.player1_choosing = True
                    if counter == 2:
                        self.player2_isHeroActive = 'F'
                        if c.name == "Hagen":
                            self.player2_multiply_f = 1
                        elif c.name == "Lee":
                            max = 0;
                            to_rem = []
                            for i in self.player1_middleRow:
                                if i.power > max:
                                    max = i.power
                            for i in self.player1_middleRow:
                                if i.power == max:
                                    to_rem.append(i)
                            for i in to_rem:
                                self.player1_middleRow.remove(i)
                                self.player1_stack.append(i)
                        elif c.name == "Angar":
                            self.player2_choosing = True
                    if self.player1_choosing or self.player2_choosing :
                        client_socket.send(("WaitingForWeather\n").encode("utf-8"))
                    else:
                        if self.player1_turn == 1 and not self.player2_pass:
                            self.player1_turn = 0
                            self.player2_turn = 1
                        elif self.player2_turn == 1 and not self.player1_pass:
                            self.player1_turn = 1
                            self.player2_turn = 0
                        client_socket.send(("OK\n").encode("utf-8"))
                elif message[0] == "E":
                    if counter == 1:
                        self.player1_choosing = False
                    elif counter == 2:
                        self.player2_choosing = False
                    if self.player1_turn == 1 and not self.player2_pass:
                        self.player1_turn = 0
                        self.player2_turn = 1
                    elif self.player2_turn == 1 and not self.player1_pass:
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
                elif message == "GetMyScores\n":
                    if counter == 1:
                        s = self.calculate_power(1,"str")
                        client_socket.send((s+"\n").encode("utf-8"))
                    if counter == 2:
                        s = self.calculate_power(2, "str")
                        client_socket.send((s + "\n").encode("utf-8"))
                elif message == "GetOppScores\n":
                    if counter == 1:
                        s = self.calculate_power(2,"str")
                        client_socket.send((s+"\n").encode("utf-8"))
                    if counter == 2:
                        s = self.calculate_power(1, "str")
                        client_socket.send((s + "\n").encode("utf-8"))
                elif message == "GetWeather\n":
                    s = self.cold + self.fog + self.rain
                    client_socket.send((s+"\n").encode("utf-8"))
                elif message == "GetIsHeroActive\n":
                    if counter == 1:
                        s = self.player1_isHeroActive
                        client_socket.send((s+"\n").encode("utf-8"))
                    if counter == 2:
                        s = self.player2_isHeroActive
                        client_socket.send((s + "\n").encode("utf-8"))
                elif message == "GetIsOppHeroActive\n":
                    if counter == 1:
                        s = self.player2_isHeroActive
                        client_socket.send((s+"\n").encode("utf-8"))
                    if counter == 2:
                        s = self.player1_isHeroActive
                        client_socket.send((s + "\n").encode("utf-8"))
                elif message == "Pass\n":
                    if counter == 1:
                        self.player1_pass = True
                        self.player1_turn = 0
                        self.player2_turn = 1
                        client_socket.send("Got message\n".encode("utf-8"))
                    if counter == 2:
                        self.player2_pass = True
                        self.player1_turn = 1
                        self.player2_turn = 0
                        client_socket.send("Got message\n".encode("utf-8"))
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

        if (self.player1_hero.name == "Gomez" or self.player2_hero.name == "Gomez"):
            self.player1_isHeroActive = "F"
            self.player2_isHeroActive = "F"
        else:
            if self.player2_hero.name == "Rhobar":
                self.player2_cards.append(self.player2_card_Deck.pop())
                self.player2_isHeroActive = "F"
            if self.player1_hero.name == "Rhobar":
                self.player1_cards.append(self.player1_card_Deck.pop())
                self.player1_isHeroActive = "F"

    def stop_server(self):
        for thread in self.client_threads:
            thread.join()
        self.server_socket.close()

    def get_cards_as_string(self, card_list):
        s = ""
        for card in card_list:
            s += str(card.id) + ";"
        return s

    def calculate_power(self,counter,form='int'):
        sum = 0
        line_sum = 0
        s = ''
        if counter == 1:
            for card in self.player1_frontRow:
                sum += card.power
                line_sum += card.power
            s += str(line_sum) + ";"
            line_sum = 0
            for card in self.player1_middleRow:
                sum += card.power
                line_sum += card.power
            s += str(line_sum) + ";"
            line_sum = 0
            for card in self.player1_backRow:
                sum += card.power
                line_sum += card.power
            s += str(line_sum) + ";"
        if counter == 2:
            for card in self.player2_frontRow:
                sum += card.power
                line_sum += card.power
            s += str(line_sum) + ";"
            line_sum = 0
            for card in self.player2_middleRow:
                sum += card.power
                line_sum += card.power
            s += str(line_sum) + ";"
            line_sum = 0
            for card in self.player2_backRow:
                sum += card.power
                line_sum += card.power
            s += str(line_sum) + ";"
        if form == 'str':
            return s
        return sum


    def checkUpgrade(self,counter):
        if counter == 1:
         for card in self.player1_backRow:
             for effect in card.effects:
                if effect == 'upgrade':
                     self.player1_upgrade_b += 1
        if counter == 2:
         for card in self.player2_backRow:
             for effect in card.effects:
                if effect == 'upgrade':
                     self.player2_upgrade_b += 1

    def activateUpgrade(self,counter):

     pass
    def releaseUpgrade(self,counter):
     pass

    def checkAndRealiseEffects(self,counter,card_id,pos):
        card = self.all_Cards[card_id]
        if counter == 1:
            for effect in card.effects:
                if effect == "spy":
                    self.player1_cards.append(self.player1_card_Deck.pop(0))
                if effect == "burn":
                    sum = 0
                    for card in self.player2_frontRow:
                        sum += card.power

                    max_power = 0
                    for card in self.player2_frontRow:
                        if card.power >= max_power:
                            max_power = card.power
                    for card in self.player2_middleRow:
                        if card.power >= max_power:
                            max_power = card.power
                    for card in self.player2_backRow:
                        if card.power >= max_power:
                            max_power = card.power

                    if sum >= 10:
                        card_to_rem_f = []
                        card_to_rem_m = []
                        card_to_rem_b = []

                        for card in self.player2_frontRow:
                            if card.power == max_power:
                                card_to_rem_f.append(card)
                        for card in self.player2_middleRow:
                            if card.power == max_power:
                                card_to_rem_m.append(card)
                        for card in self.player2_backRow:
                            if card.power == max_power:
                                card_to_rem_b.append(card)

                        for card in card_to_rem_f:
                            self.player2_stack.append(card)
                            self.player2_frontRow.remove(card)
                        for card in card_to_rem_m:
                            self.player2_stack.append(card)
                            self.player2_middleRow.remove(card)
                        for card in card_to_rem_b:
                            self.player2_stack.append(card)
                            self.player2_backRow.remove(card)
                if effect == "heal":
                    self.player1_choosing = True
        if counter == 2:
            for effect in card.effects:
                if effect == "spy":
                    self.player2_cards.append(self.player2_card_Deck.pop(0))
                if effect == "burn":
                    sum = 0
                    for card in self.player1_frontRow:
                        sum += card.power

                    max_power = 0
                    for card in self.player1_frontRow:
                        if card.power >= max_power:
                            max_power = card.power
                    for card in self.player1_middleRow:
                        if card.power >= max_power:
                            max_power = card.power
                    for card in self.player1_backRow:
                        if card.power >= max_power:
                            max_power = card.power

                    if sum >= 10:
                        card_to_rem_f = []
                        card_to_rem_m = []
                        card_to_rem_b = []

                        for card in self.player1_frontRow:
                            if card.power == max_power:
                                card_to_rem_f.append(card)
                        for card in self.player1_middleRow:
                            if card.power == max_power:
                                card_to_rem_m.append(card)
                        for card in self.player1_backRow:
                            if card.power == max_power:
                                card_to_rem_b.append(card)

                        for card in card_to_rem_f:
                            self.player1_stack.append(card)
                            self.player1_frontRow.remove(card)
                        for card in card_to_rem_m:
                            self.player1_stack.append(card)
                            self.player1_middleRow.remove(card)
                        for card in card_to_rem_b:
                            self.player1_stack.append(card)
                            self.player1_backRow.remove(card)
                if effect == "heal":
                    self.player2_choosing = True
        pass

    def realiseWeather(self,c):
        if c.name == "Mróz":
            self.cold = 'T'
        elif c.name == "Mgła":
            self.fog = 'T'
        elif c.name == "Deszcz":
            self.rain = 'T'
        elif c.name == "Niebo":
            self.rain = 'F'
            self.fog = 'F'
            self.cold = 'F'


    def endRound(self):
        sum1 = self.calculate_power(1)
        sum2 = self.calculate_power(2)
        if sum1 == sum2:
            self.player1_lifes -= 1
            self.player2_lifes -= 1
            coin = random.randint(0, 1)
            if coin == 1:
                self.player1_turn = 0
                self.player2_turn = 1
            else:
                self.player1_turn = 1
                self.player2_turn = 0
        elif sum1 < sum2:
            self.player1_lifes -= 1
            self.player1_turn = 1
            self.player2_turn = 0
        elif sum1 > sum2:
            self.player2_lifes -= 1
            self.player1_turn = 0
            self.player2_turn = 1

        for card in self.player1_frontRow:
            self.player1_stack.append(card)
        self.player1_frontRow = []

        for card in self.player1_middleRow:
            self.player1_stack.append(card)
        self.player1_middleRow = []

        for card in self.player1_backRow:
            self.player1_stack.append(card)
        self.player1_backRow = []

        for card in self.player2_frontRow:
            self.player2_stack.append(card)
        self.player2_frontRow = []

        for card in self.player2_middleRow:
            self.player2_stack.append(card)
        self.player2_middleRow = []

        for card in self.player2_backRow:
            self.player2_stack.append(card)
        self.player2_backRow = []