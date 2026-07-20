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
            
def textMulti(g,textArray,cntr,backbox=True,adjustCenterHeight=False):
    fnts = []
    stats = []
    height = 0
    width = 0
    padding = 8

    #first pass build all the lines and measure them
    for t in textArray:
        fnt = g.eventFont.render(
            t, True, (255,255,255)
        )
        stat = fnt.get_rect()
        stats.append(stat)
        fnts.append(fnt)
        width = max(width,stat.width)
        height += stat.height+4

    if adjustCenterHeight:
        cntr[1]-=height//2

    #draw backbox
    if backbox:
        pygame.draw.rect(g.screen,(40,40,40),(
                cntr[0]-width//2-padding,
                cntr[1]-height//2-padding,
                width+padding,
                height+padding
            ), 
        border_radius=8)

    #second pass draw all the lines in correct positions
    curY = cntr[1]-height/2
    for f,s in zip(fnts,stats):
        g.screen.blit(
            f,
            (cntr[0]-s.width//2,curY)
        )
        curY += s.height+4

class instruction():
    def __init__(self,text : list,duration :int=60,target=None,blocking : bool=False):
        self.text = text
        self.target = target
        self.duration = duration
        self.blocking = blocking
        self.g = iHandler.g
        self.border = 30
        self.r = 8

    def draw(self):
        #can set duration to -1 to make it permenant until proceeding
        if self.duration > 0: self.duration -= 1 
        if self.duration == 0:
            iHandler.active.remove(self)
        
        if len(self.text) == 0: return

        if self.target is None: #draw in center of screen
            #draw rectangle
            cntr = (self.g.W/2, self.g.H/2)
            textMulti(self.g,self.text,cntr,True)
        else:
            cntr = (self.target.x,self.target.y-24)
            textMulti(self.g,self.text,cntr,True,True)
            

class instructionHandler():
    def __init__(self):
        self.queue = []
        self.active = []
        self.baseTime = 120 #base duration of an instruction
        self.extraTime = 30 #extra duration per word

    def draw(self):
        if len(self.active) < 1 or not self.active[-1].blocking:
            if len(self.queue) > 0:
                for instr in self.queue:
                    if instr.blocking:
                        if len(self.active)<1:
                            self.active.append(instr)
                            self.queue.remove(instr)
                        break
                    else:
                        busy = False
                        for instr2 in self.active:
                            if instr.target==instr2.target:
                                busy = True
                                break
                        if not busy:
                            self.active.append(instr)
                            self.queue.remove(instr)
                        else:
                            break

        for instr in self.active:
            instr.draw()

        #print("-----------\n",self.queue,self.active)

c = context()

iHandler = instructionHandler()

def getevent(eventName):
    match eventName:
        case "bus":
            return busEvent()
        case _:
            raise Exception("Event not found!")

def busEvent():
    return instruction(
        [
            "You come across a lone party bus in the road",
            "inside the minifridge are a selection of drinks",
            "everyone gets 1 potion"
        ],
        duration=900,
        blocking=True
    )

def getcard(cardName):
    match cardName:
        case "strike":
            return strike()
        case _:
            return card()

class card():
    def __init__(self):
        self.dmg = 0
        self.block = 0
        self.cost = 0
        self.sips = 0

    def play(self):
        pass

    def damage(self, times=1):
        #must have attacker and target
        if c.source is None or c.target is None:
            return
        dmg = self.dmg

        strength = c.source.b.strength
        weak = c.source.b.weak
        vulnerable = c.target.b.vulnerable
        
        dmg += strength
        if vulnerable > 0:
            dmg *= 2
            c.target.b.vulnerable -= 1
        if weak > 0:
            dmg = math.floor(dmg / 2)
            c.source.b.weak -= 1

        for t in times:
            c.target.damage(dmg)
    
    def protect(self):
        blk = self.block

        if self.frail > 0:
            blk = math.floor(blk / 2)

        c.target.block += blk
    
    def sip(self):
        iHandler.queue.append(instruction([
            "take "+str(self.sips)+" sips!"
        ],60,c.source,False))

    def exhaust(self):
        iHandler.queue.append(instruction([
            "Card exhausted!"
        ],60,c.source,False))

class strike(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.dmg = 1

    def play(self):
        self.damage()