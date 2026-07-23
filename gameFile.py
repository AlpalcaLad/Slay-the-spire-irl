import cv2
import time
from multiprocessing import Process,Pipe
import qr_read
import keyboard
import os
import pygame
import sys
import random
import keyboard
import math
from helperFuncs import *


#region Sprite
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

#region Buff handler
class buffHandler():
    def __init__(self):
        self.vulnerable = 0
        self.weak = 0
        self.frail = 0
        self.strength = 0
        self.tipsy = 0

        self.permaStrength = 0

        #special
        self.store = [] #stored effects

        self.freeSkill = 0
        self.freeAttack = 0
        self.freePower = 0
        self.freeCard = 0

        self.freeCardNames = []

    def reset(self):
        self.strength = self.permaStrength
        self.weak = 0
        self.tipsy = 0
        self.vulnerable = 0
    
    def startturn(self):
        if self.weak>0: self.weak -= 1
        if self.vulnerable>0: self.vulnerable -= 1
        if self.frail>0: self.frail -= 1
        self.freeCard = 0

#region Entity
class entity():
    def __init__(self):
        self.hp = 1
        self.hpMax = self.hp
        self.block = 0
        self.name = "entity"
        self.x = 0
        self.y = 0
        self.friendly = False
        self.energy = -1

        self.acting = False

        #buffs and debuffs
        self.b = buffHandler()

    def damage(self,dmg):
        blockAm = min(dmg,self.block)
        self.block -= blockAm

        dmg -= blockAm
        if dmg > 0:
            hp -= dmg

        if self.hp <= 0:
            self.die()

    def die(self):
        self.hp = 0
        print(self.name + " died")

#region Healthbar
class healthbar():
    def __init__(self,parent : entity,game,x,y,w,h,r=8):
        self.g = game
        self.p = parent
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r

    def draw(self):
        #block
        hpBarCol = (20,255,20)
        if self.p.block > 0:
            self.g.screen.blit(
                self.g.blockAsset,
                (
                    self.x-40,
                    self.y-13
                ),
            )
            drawTextOutlined(self.g,str(self.p.block),(self.x,self.y-3),(20,20,100),(255,255,255))
            hpBarCol = (100,180,255)

        #health
        ratio = self.p.hp / self.p.hpMax
        pygame.draw.rect(self.g.screen,"red",(self.x,self.y,self.w,self.h), border_radius=self.r)
        pygame.draw.rect(self.g.screen,hpBarCol,(self.x,self.y,self.w*ratio,self.h), border_radius=self.r)
        self.g.screen.blit(
            self.g.font.render(
                str(self.p.hp)+"/"+str(self.p.hpMax), True, (255,255,255)
            ),
            (self.x+self.w+14,self.y-3)
        )

        #energy
        if self.p.energy>0:
            self.g.screen.blit(
                self.g.energyAsset,
                (
                    self.x+self.w+8,
                    self.y-43
                ),
            )
            drawTextOutlined(self.g,str(self.p.energy),(self.x+self.w+40,self.y-33),(100,60,20),(255,255,255))
        elif self.p.energy==0: #draw dull sprite
            self.g.screen.blit(
                self.g.noEnergyAsset,
                (
                    self.x+self.w+8,
                    self.y-43
                ),
            )
            drawTextOutlined(self.g,str(self.p.energy),(self.x+self.w+40,self.y-33),(80,50,10),(160,160,160))


from cards import *
from enemies import *

#region Player
class player(entity):
    def __init__(self,className,g):
        super().__init__()
        self.deck = []
        self.relics = []
        self.friendly = True
        self.g : game = g
        self.y = self.g.H-250
        self.energyMax = 3
        self.energy = 0

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
        if not self.g.playerTurn:
            self.g.actionQueue.append((self.play,cardText))
            return
        
        cardToPlay = getcard(cardText)
        cost = cardToPlay.cost

        if self.b.freeCard > 0: #e.g. "next card you play is free"
            cost = 0
            self.b.freeCard -= 1

        if cardText in self.b.freeCardNames: #e.g. "all cards named after a drink are free"
            cost = 0

        if cost > self.energy:
            iHandler.queue.append(instruction([
                "You don't have enough energy!"
            ],120,self,False))
        else:
            self.energy-=cost
            cardToPlay.play()
        

    def draw(self):
        self.s.draw()
        self.h.draw()

    def endturn(self):
        pass

    def startturn(self):
        self.block = 0
        self.energy = self.energyMax
        self.b.startturn()

colours = {
    "black": (0,0,0),
    "white": (255,255,255)
}

#region Game
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
        self.eventFont = pygame.font.SysFont("kreon", 36)

        #UI definition
        self.backdrops = [
            sprite(self,self,"./art/protoBackdrop.png")
            # sprite(self,self,"./art/backdropSky.png"),
            # sprite(self,self,"./art/backdropTree.png"),
            # sprite(self,self,"./art/backdropGrass.png")
        ]
        c.img = pygame.image.load(c.asset).convert_alpha()
        self.blockAsset = pygame.transform.scale(pygame.image.load("./art/icons/blockIcon.png").convert_alpha(),(45,45))
        self.energyAsset = pygame.transform.scale(pygame.image.load("./art/icons/energyIcon.png").convert_alpha(),(45,45))
        self.noEnergyAsset = pygame.transform.scale(pygame.image.load("./art/icons/energylessIcon.png").convert_alpha(),(45,45))
        c.g = self
        iHandler.g = self

        #gameplay definition
        self.players: list[player] = []
        self.enemies: list[enemy] = []
        self.actionQueue = []
        self.playerTurn = True #whether players can play cards
        self.inCombat = False

    def endturn(self):
        for p in self.players:
            if p.acting:
                self.actionQueue.append((self.endturn,))
                return

        for p in self.players:
            p.endturn()
        
        self.playerTurn = False

        for e in self.enemies:
            e.act()

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
        if cardText == "endturn":
            self.endturn()

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
                    tempText = cardText[:-1]
                    if tempText[-1].isupper():
                        p.play(tempText[:-1])
                    else:
                        p.play(tempText)

        elif cardText.startswith("enemy"):
            for p in self.players: 
                p.energy = (p.energy + 1) * 2
                p.block = (p.block + 1) * 2

            if len(self.enemies) == 0:
                self.inCombat = True

            tempText = cardText
            if tempText[-1].isupper():
                tempText=tempText[:-1]

            found = False
            for e in self.enemies:
                if e.enName == tempText:
                    c.target = e
                    found = True
                    break
            if not found:
                en = getenemy(tempText)(self)
                c.target = en
                en.enName = tempText
                self.enemies.append(en)
                #reposition all enemies
                incrX = self.H/(len(self.enemies)+1)
                for i in range(len(self.enemies)):
                    self.enemies[i].x = incrX * (i+1)
                    self.enemies[i].h.x = self.enemies[i].x #update healthbar positions
        
        elif cardText.startswith("event"):
            tempText = cardText
            if tempText[-1].isupper():
                tempText=tempText[:-1]

            iHandler.queue.append(getevent(tempText.replace("event","",1)))

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
        
        #play any waiting actions
        if len(self.actionQueue)>0:
            length = len(self.actionQueue)
            for i in range(length):
                action = self.actionQueue.pop(0)
                action[0](action[1]) #apply action with arguments

        #read in any cards
        if len(self.cardsToBePlayed) > 0:
            newCard = self.cardsToBePlayed.pop(0)
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
        
        #check if enemy turn over
        if not self.playerTurn and len(self.enemies) > 0:
            found = False
            for e in self.enemies:
                if e.acting:
                    found = True
            if not found:
                self.playerTurn = True
                for p in self.players:
                    p.startturn()

        #check if all enemies dead and in combat
        if len(self.enemies)==0 and self.inCombat:
            pass
        
        #render enemies
        for e in self.enemies:
            e.draw()

        #render misc ui
        c.draw()

        #render events
        iHandler.draw()

        #finish up
        pygame.display.flip()

    def waitTick(self,fps):
        self.clock.tick(fps)