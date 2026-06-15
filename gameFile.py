import cv2
import time
from multiprocessing import Process,Pipe
import qr_read
import keyboard
import os
from cards import *
import pygame
import sys
import random

class sprite():
    def __init__(self,parent,game,asset):
        self.p = parent
        self.g = game
        self.img = pygame.image.load(asset).convert_alpha()

    def draw(self):
        self.g.screen.blit(
            self.img,
            (
                self.parent.x,
                self.parent.y
            ),
        )

class entity():
    def __init__(self):
        self.hp = 1
        self.block = 0
        self.effects = []
        self.name = "entity"
        self.x = 0
        self.y = 0
        self.friendly = False

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
        self.friendly = True

        match className: #setup player class
            case "cocktailmixer":
                self.hp=100
                self.deck = []
            case "beermaster":
                pass
            case "winecon":
                pass
            case "designateddriver":
                pass
            case _:
                pass

        self.className = className

    def play(cardText):
        pass

colours = {
    "black": (0,0,0),
    "white": (255,255,255)
}

class game():
    def __init__(self):
        #general setup
        self.run = True
        self.cardsToBePlayed = []
        #basic pygame setup
        pygame.init()
        self.W, self.H = 600, 600
        self.screen = pygame.display.set_mode((self.W,self.H))
        pygame.display.set_caption("Slay the Spire IRL")
        self.clock = pygame.time.Clock()
        font = pygame.font.SysFont(None, 36)
        #UI definition

        #gameplay definition
        self.players = []
        self.enemies = []

    def readCard(self,cardText: str):
        if cardText in ["cocktailmixer","beermaster","winecon","designateddriver"]:
            found = False
            for p in self.players:
                if p.className == cardText:
                    c.target = p
                    found = True
            if not found:
                self.players.append(player(cardText))

        elif cardText[-1] in ["1","2","3","4"]:
            pass #play card for given player
        print("Read card ",cardText)
        return

    def setup(self):
        sharedArray = []
        self.cardsToBePlayed = sharedArray
        return sharedArray

    def mainloop(self,):
        self.screen.fill(colours["black"])
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                self.run=False
        
        #read in any cards
        if len(self.cardsToBePlayed) > 0:
            newCard = self.cardsToBePlayed.pop()
            self.readCard(newCard)

        #render UI

        #render players

        #render events

    def waitTick(self,fps):
        self.clock.tick(fps)