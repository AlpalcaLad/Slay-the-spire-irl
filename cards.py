import random
import math
import pygame
import numpy as np

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
    def __init__(self,text : list,duration :int=60,target=None,blocking : bool=False):
        self.text = text
        self.target = target
        self.duration = duration
        self.blocking = blocking
        self.g = iHandler.g
        self.border = 30

    def draw(self):
        self.duration -= 1 
        if self.duration < 0:
            iHandler.active.remove(self)
        
        if len(self.text) == 0: return

        if self.target is None: #draw in center of screen
            #draw rectangle
            cntr = (self.g.W/2, self.g.H/2)
            size = (
                np.max([
                    self.g.font.size(t)[0]
                    for t in self.text
                ]) + self.border,
                self.g.font.size(self.text)[1]*len(self.text) + self.border
            )
        

class instructionHandler():
    def __init__(self):
        self.queue = []
        self.active = []
        self.baseTime = 120 #base duration of an instruction
        self.extraTime = 30 #extra duration per word

    def draw(self):
        if len(self.active) < 1 or not self.active[-1].blocking:
            if len(self.queue) > 0:
                #add from queue
                pass

        for instr in self.active:
            instr.draw()

c = context()

iHandler = instructionHandler()

def getcard(cardName):
    match cardName:
        case "strike":
            return strike()
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

class strike(card):
    def __init__(self):
        super().__init__()

    def play(self):
        pass