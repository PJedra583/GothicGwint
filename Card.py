import pygame
import os
import random
class Card:
    cards = []
    heroses = []
    id_counter = 0
    def __init__(self,name,power,type,effects) :
        if name!=None:
         self.image = pygame.image.load("data/textures/"+name+".jpg")
         self.name = name
         self.effects = effects
         for effect in effects :
             self.effects.append(effect)
         self.type = type
         self.power = power
         self.id = self.id_counter
         self.id_counter += 1


    def load_cards(self):
        f = "front"
        mid = "middle"
        b = "back"
        m = "mixed"
        h = "hero"
        w = "weather"
        u = "upgrade"
        heal = "heal"
        spy = "spy"
        a = "to_attack"
        pos_to_attack = "pos_to_attack"
        s = "switch"
        t = "trap"
        brotherhood = "brotherhood"
        summon = "summon"
        burn = "burn"
        pos_to_burn = "pos_to_burn"
        self.cards.append(Card("Abuyin",2,b,(u,)))
        self.cards.append(Card("Andre", 6, f, ()))
        self.heroses.append(Card("Angar", None, h, ("Zagraj karte pogody",)))
        self.cards.append(Card("Baal Netbek", 2, b, ()))
        self.cards.append(Card("Bezi", 15, f, (h,)))
        self.cards.append(Card("Bloodwyn", 4, f, ()))
        self.cards.append(Card("Brutus", 2, f, ()))
        self.cards.append(Card("Bullit", 4, f, ()))
        self.cards.append(Card("Cavalorn", 7, m, (s,)))
        self.cards.append(Card("Cord", 6, f, ()))
        self.cards.append(Card("Corristo", 6, mid, ()))
        self.cards.append(Card("Dar", 1, b, ()))
        self.cards.append(Card("Deszcz", None, w, ("Zmniejsz siłe z tyłu",)))
        self.cards.append(Card("Diego", 10, mid, (h,)))
        self.cards.append(Card("Finkregh", 10, b, (h,)))
        self.cards.append(Card("Gestath", 8, m, (s,)))
        self.heroses.append(Card("Gomez", None, h, ("Blokuje umiejetnosc przeciwnika",)))
        self.cards.append(Card("Gor Boba", 4, f, ()))
        self.cards.append(Card("Gor Na Toth", 8, f, ()))
        self.cards.append(Card("Gorn", 10, f, (h,)))
        self.cards.append(Card("Greg", 7, f, (burn,)))
        self.heroses.append(Card("Hagen", None, h, ("Podwaja sile jednostek w zwarciu ",)))
        self.cards.append(Card("Herold", 2, f, (a,)))
        self.cards.append(Card("In Extremo", None, pos_to_attack, (a,)))
        self.cards.append(Card("Jergan", 2, f, (spy,)))
        self.cards.append(Card("Kalom", 7, mid, (burn,)))
        self.cards.append(Card("Kharim", 3, f, ()))
        self.cards.append(Card("Kruk", 7, f, (h,)))
        self.cards.append(Card("Lares", 4, mid, (spy,)))
        self.heroses.append(Card("Lee", None, h, ("Niszczy najsilniejsze łucznictwo wroga",)))
        self.cards.append(Card("Lester", 8, b, (h,heal)))
        self.cards.append(Card("Manekin", None, t, (t,)))
        self.cards.append(Card("Mgła", None, w, ("Zmniejsz siłe po środku",)))
        self.cards.append(Card("Milten", 10, mid, (h,)))
        self.cards.append(Card("Mróz", None, w, ("Zmniejsz siłe z przodu",)))
        self.cards.append(Card("Najemnik1", 4, f, (brotherhood,)))
        self.cards.append(Card("Najemnik2", 4, f, (brotherhood,)))
        self.cards.append(Card("Niebo", None, w, ("Usun efekty pogodowe",)))
        self.cards.append(Card("Onar", 2, mid, (summon,)))
        self.cards.append(Card("Opętany", 2, f, (summon,)))
        self.cards.append(Card("Pożoga", None, pos_to_burn, (burn,)))
        self.cards.append(Card("Pyrokar", 8, mid, (h,)))
        self.cards.append(Card("Rączka", 3, mid, (spy,)))
        self.heroses.append(Card("Rhobar", None, h, ("Weź o jedną karte więcej")))
        self.cards.append(Card("Sagitta", 2, b, (u,)))
        self.cards.append(Card("Saturas", 8, mid, (h,)))
        self.cards.append(Card("Sentenza", 6, f, ()))
        self.cards.append(Card("Snaf", 1, b, (u,)))
        self.cards.append(Card("Sylvio", 5, f, ()))
        self.cards.append(Card("Thorus", 6, f, ()))
        self.cards.append(Card("Torlof", 6, f, ()))
        self.cards.append(Card("Udar", 8, mid, ()))
        self.cards.append(Card("Ur-Shak", 5, b, (heal,)))
        self.cards.append(Card("Vatras", 5, b, (heal,)))
        self.cards.append(Card("Wilk", 5, mid, ()))
        self.cards.append(Card("Wrzód1", 0, b, ()))
        self.cards.append(Card("Wrzód2", 8, f, ()))
        self.cards.append(Card("Xardas", 15, f, (h,)))
        self.cards.append(Card("Y'Berion", 5, b, (u,)))
        random.shuffle(self.cards)


    def getCard(self):
        c = self.cards.pop(0)
        return c
    def getHeroCard(self):
        c = self.heroses.pop(0)
        return c

    def getDeck(self):
        return self.cards




















































