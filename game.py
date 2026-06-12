import cv2
import time
from multiprocessing import Process,Queue,freeze_support
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

colours = {
    "black": (0,0,0),
    "white": (255,255,255)
}

class game():
    def __init__(self):
        #general setup
        self.run = True
        #basic pygame setup
        pygame.init()
        self.W, self.H = 600, 600
        self.screen = pygame.display.set_mode((self.W,self.H))
        pygame.display.set_caption("Slay the Spire IRL")
        self.clock = pygame.time.Clock()
        font = pygame.font.SysFont(None, 36)
        #UI definition

    def readCard(self,cardText: str):
        if cardText.startswith("player"):
            pass #create player
        if cardText[-1] in ["1","2","3","4"]:
            pass #play card for given player
        return
    
    def mainloop(self,conn):
        while self.run:
            self.screen.fill(colours["black"])

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    self.run=False
            
            #render UI

            #render players

            #render events