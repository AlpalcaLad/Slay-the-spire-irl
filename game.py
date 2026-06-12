import cv2
import time
from multiprocessing import Process,Queue,freeze_support
import qr_read
import keyboard
import os
from cards import *

class entity():
    def __init__(self):
        self.hp = 1
        self.block = 0
        self.effects = []
        self.name = "entity"

    def damage(self,dmg):
        #naive formula
        self.hp -= dmg
        if self.hp <= 0:
            self.die()

    def die(self):
        self.hp = 0
        print(self.name + " died")

class player(entity):
    def __init__(self,className):
        super().__init__()
        self.deck = []
        self.relics = []

        match className: #setup player class
            case "cocktail":
                self.hp=100
                self.deck = []
            case "beermaster":
                pass
            case "winecon":
                pass
            case "driver":
                pass
            case _:
                pass

    def play(cardText):
        pass

class game():
    def __init__(self):
        pass

    def readCard(self,cardText: str):
        if cardText.startswith("player"):
            pass #create player
        if cardText[-1] in ["1","2","3","4"]:
            pass #play card for given player
        return
    
