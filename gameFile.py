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
import keyboard
import math

class sprite():
    def __init__(self,parent,game,asset):
        self.p = parent
        self.g = game
        self.img = pygame.image.load(asset).convert_alpha()
        self.x = 0
        self.y = 0

    def draw(self):
        self.g.screen.blit(
            self.img,
            (
                self.p.x + self.x,
                self.p.y + self.y
            ),
        )

class healthbar():
    def __init__(self,parent,game,x,y,w,h,r=8):
        self.g = game
        self.p = parent
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r

    def draw(self):
        ratio = self.p.hp / self.p.hpMax
        pygame.draw.rect(self.g.screen,"red",(self.x,self.y,self.w,self.h), border_radius=self.r)
        pygame.draw.rect(self.g.screen,"green",(self.x,self.y,self.w*ratio,self.h), border_radius=self.r)
        self.g.screen.blit(
            self.g.font.render(
                str(self.p.hp)+"/"+str(self.p.hpMax), True, (255,255,255)
            ),
            (self.x+self.w+14,self.y-3)
        )
        

class entity():
    def __init__(self):
        self.hp = 1
        self.hpMax = self.hp
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

from enemies import *

class player(entity):
    def __init__(self,className,g):
        super().__init__()
        self.deck = []
        self.relics = []
        self.friendly = True
        self.g = g
        self.y = self.g.H-250

        match className: #setup player class
            case "cocktailmaker":
                self.hp=100
                self.deck = []
                self.s = sprite(self,g,"./art/player1Art.png")
                self.x = 2*self.g.W//5-55
                self.hatchEffects = []
            case "beermaster":
                self.s = sprite(self,g,"./art/player1Art.png")
                self.x = 1*self.g.W//5-45
            case "winecon":
                self.s = sprite(self,g,"./art/player1Art.png")
                self.x = 3*self.g.W//5-35
                self.wine = 0
            case "designateddriver":
                self.s = sprite(self,g,"./art/player1Art.png")
                self.x = 4*self.g.W//5-25
            case _:
                self.s = sprite(self,g,"./art/player1Art.png")

        self.hpMax = self.hp
        self.className = className

        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)

    def play(self,cardText):
        print(cardText)

    def draw(self):
        self.s.draw()
        self.h.draw()

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
        self.W, self.H = 1200, 900
        self.x,self.y = 0,0
        self.screen = pygame.display.set_mode((self.W,self.H))#, pygame.FULLSCREEN)
        pygame.display.set_caption("Slay the Spire IRL")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("kreon", 22)
        #UI definition
        self.backdrops = [
            sprite(self,self,"./art/protoBackdrop.png")
            # sprite(self,self,"./art/backdropSky.png"),
            # sprite(self,self,"./art/backdropTree.png"),
            # sprite(self,self,"./art/backdropGrass.png")
        ]
        c.img = pygame.image.load(c.asset).convert_alpha()
        c.g = self
        iHandler.g = self

        #gameplay definition
        self.players = []
        self.enemies = []
        self.actionQueue = []
        self.playerTurn = False #whether players can play cards


    def mapToChar(self,string):
        if string=="1":
            return "beermaster"
        elif string=="2":
            return "cocktailmaker"
        elif string=="3":
            return "winecon"
        else:
            return "designateddriver"

    def readCard(self,cardText: str):
        if cardText in ["cocktailmaker","beermaster","winecon","designateddriver"]:
            found = False
            for p in self.players:
                if p.className == cardText:
                    c.target = p
                    found = True
                    break
            if not found:
                p = player(cardText,self)
                self.players.append(p)
                c.target = p

        elif cardText[-1] in ["1","2","3","4"]:
            charName = self.mapToChar(cardText[-1])
            for p in self.players:
                if p.className == charName:
                    p.play(cardText[:-1])

        elif cardText.startswith("enemy"):
            found = False
            for e in self.enemies:
                if e.enName == cardText:
                    c.target = e
                    found = True
                    break
            if not found:
                en = getenemy(cardText)(self)
                c.target = en
                en.enName = cardText
                self.enemies.append(en)
                #reposition all enemies
                incrX = self.H/(len(self.enemies)+1)
                for i in range(len(self.enemies)):
                    self.enemies[i].x = incrX * (i+1)
                    self.enemies[i].h.x = self.enemies[i].x #update healthbar positions

        #print("Read card ",cardText)
        return

    def setup(self):
        sharedArray = []
        self.cardsToBePlayed = sharedArray
        return sharedArray

    def mainloop(self):
        if keyboard.is_pressed("q"):
            exit()

        self.screen.fill(colours["black"])

        e = pygame.event.poll()
        if e.type == pygame.QUIT:
            pygame.quit()
            self.run=False
        
        #read in any cards
        if len(self.cardsToBePlayed) > 0:
            newCard = self.cardsToBePlayed.pop()
            self.readCard(newCard)

        #render UI
        for i in range(len(self.backdrops)):
            b = self.backdrops[i]
            # t = pygame.time.get_ticks()
            # if i!=0: 
            #     b.x = sum(list(math.sin(x*t/9000 + x*10)*i for x in range(10)))-100
            #     b.y = sum(list(math.sin(x*t/11000 - x*10)*i for x in range(10)))-100
            
            b.draw()

        #render players
        for p in self.players:
            p.draw()

        #render enemies
        for e in self.enemies:
            e.draw()

        #render misc ui
        c.draw()

        #render events

        #finish up
        pygame.display.flip()

    def waitTick(self,fps):
        self.clock.tick(fps)