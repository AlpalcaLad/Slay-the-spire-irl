import random
import math
import pygame

class context():
    def __init__(self):
        self.target = None
        self.source = None
        self.asset = "./art/marker.png"
        self.offset = 0

    def draw(self):
        if self.target is not None:
            self.offset = (self.offset+0.02)%(2*math.pi)
            self.g.screen.blit(
                self.img,
                (
                    self.target.x+32,
                    self.target.y - 32 - 5*math.sin(self.offset)
                )
            )
            
class instruction():
    def __init__(self,text,target=None,blocking=False):
        self.text = text
        self.target = target
        self.duration = 0

    def draw():
        pass

class instructionHandler():
    def __init__(self,g):
        self.queue = []
        self.active = []
        self.baseTime = 120 #base duration of an instruction
        self.extraTime = 30 #extra duration per word
        self.g = g

    def draw(self):
        pass

c = context()

def getcard(cardName):
    match cardName:
        case "strike1":
            return strike1()
        case _:
            return card()

class card():
    def __init__(self):
        self.dmg = 0

    def play(self):
        pass

    def damage(self):
        #must have attacker and target
        if c.source is None or c.target is None:
            return
        dmg = self.dmg
        pass #apply buffs
        c.target.damage(dmg)

class strike1(card):
    def __init__(self):
        super().__init__()

    def play(self):
        pass