from dis import Instruction
import random
import math
import pygame
import numpy as np
from gameFile import entity
from helperFuncs import *

#region context
class context():
    """Keeps track of who a card comes from and affects"""
    def __init__(self):
        self.target : entity = None
        self.source : entity = None
        self.asset = "./art/marker.png"
        self.offset = 0

    def draw(self):
        #draw the target marker
        if self.target is not None:
            self.offset = (self.offset+0.02)%(2*math.pi)
            self.g.screen.blit(
                self.img,
                (
                    self.target.x+32,
                    self.target.y - 32 - 5*math.sin(self.offset)
                )
            )

#region instruction
class instruction():
    """An instruction box (optionally affecting a specific player)"""
    def __init__(self,text : list,duration :int=60,target=None,blocking : bool=False, options=[]):
        self.text = text
        self.target = target
        self.duration = duration
        self.blocking = blocking
        self.g = iHandler.g
        self.border = 30
        self.r = 8
        self.options = options

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
            cntr = (self.target.x+32,self.target.y-24)
            textMulti(self.g,self.text,cntr,True,True)
            
#region instruction handler
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

def getevent(eventName : str):
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

#region cards

def getcard(cardName):
    match cardName:
        case "strike":
            return strike()
        case "defend":
            return defend()
        case _:
            return card()

class card():
    def __init__(self):
        self.dmg = 0
        self.block = 0
        self.cost = 0
        self.sips = 0
        self.harmful = False
        self.selfTarget = False

    def play(self):
        pass

    def damage(self, times=1,target = c.target):
        #must have attacker and target
        if c.source is None or target is None:
            return
        dmg = self.dmg

        strength = c.source.b.strength
        weak = c.source.b.weak
        vulnerable = target.b.vulnerable
        wasted = target.b.wasted
        
        dmg += strength
        if vulnerable > 0:
            dmg *= 2
            c.target.b.vulnerable -= 1
        if weak > 0:
            dmg = dmg // 2
            c.source.b.weak -= 1
        if wasted>0:
            dmg*=2

        for t in range(times):
            target.damage(dmg)
    
    def protect(self,target=c.source):
        blk = self.block

        frail = target.b.frail
        if frail > 0:
            blk = blk // 2
            target.b.frail -= 1

        target.block += blk
    
    def sip(self,target=c.source):
        if self.sips > 0:
            target.b.drinkSafe -= self.sips
            if target.b.drinkSafe < 0:
                target.b.drinkSafe = 0
                iHandler.queue.append(instruction([
                    "take "+str(self.sips)+f" sip{"s" if self.sips>1 else ""}!"
                ],90,target,False))

    def exhaust(self):
        iHandler.queue.append(instruction([
            "Card exhausted!"
        ],90,c.source,False))

    def tipsy(self,am,target=c.target):
        target.b.tipsy += am
        if target.b.tipsy >= 5:
            target.b.tipsy.wasted += 1
            target.b.tipsy -= 5

    def draw(self,am,target=c.source):
        iHandler.queue.append(instruction([
            "Draw "+str(am)+f" card{"s" if self.am>1 else ""}"
        ],120,target,False))

    def heal(self,am,target=c.source):
        target.hp = min(target.hp+am,target.hpMax)

    def brew(self,message,addition):
        if c.source.b.alchemist>0:
            self.block = c.source.b.alchemist
            self.protect()
        iHandler.queue.append(instruction(
            message
        ,90,c.source,False))
        c.source.b.store.append(addition)

#region GENERIC





#region strike

class strike(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.dmg = 1
        self.harmful = True

    def play(self):
        self.damage()

#region defend

class defend(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.block = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        self.protect()



#region BEERMASTER

class alcoholic_rage(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = True
        self.selfTarget = False

    def play(self):
        c.target.b.vulnerable += 1
        c.target.b.weak += 1

class corona_and_lime(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.dmg=1
        self.harmful = True
        self.selfTarget = False

    def play(self):
        self.damage()
        iHandler.queue.append(instruction([
            "Draw a card",
            "and take a sip"
        ],180,c.source,False))

class brewdog(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.dmg=1
        self.sips = 1
        self.harmful = True
        self.selfTarget = False

    def play(self):
        c.target.b.vulnerable += 1
        self.damage()

class inchs(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.dmg=1
        self.harmful = True
        self.selfTarget = False

    def play(self):
        c.target.b.vulnerable += 1
        self.damage()
        self.sip()

class peroni(card):
    def __init__(self):
        super().__init__()
        self.cost = 2
        self.block = 2
        self.sips = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        for p in c.g.players:
            self.protect(p)
        self.sip()

class relaxing_pint(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.sips = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        self.heal(2)
        iHandler.queue.append(instruction([
            "Take a sip",
            "and exhaust this card"
        ],180,c.source,False))

class on_tap(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "Draw 1 card, if named",
            "after a drink, 2 more"
        ],180,c.source,False))

class catch_up(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.sips =1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        c.source.energy += 2
        self.sip()

class chug(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.dmg = 4
        self.sips = 4
        self.harmful = False
        self.selfTarget = True

    def play(self):
        self.sip()

class snakebite(card):
    def __init__(self):
        super().__init__()
        self.cost = 3
        self.dmg = 5
        self.harmful = False
        self.selfTarget = True

    def play(self):
        self.damage()

class wingman(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = True
        self.selfTarget = False

    def play(self):
        c.target.b.vulnerable += 3

class beer_jacket(card):
    def __init__(self):
        super().__init__()
        self.cost = 2
        self.block = 2
        self.sips = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        self.protect()
        self.sip()

class ring_of_fire(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.sips = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        for p in c.g.players:
            p.energy += 1
            self.sip(p)

class split_the_g(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        for p in c.g.players:
            p.energy += 1
            self.sip(p)

class hellsraiser(card):
    def __init__(self):
        super().__init__()
        self.cost = 2
        self.harmful = False
        self.selfTarget = True

    def play(self):
        c.source.b.freeCardNames = [
            "corona",
            "brewdog",
            "inchs",
            "peroni",
            "snakebite",
        ]

class tacky_chunder(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.block = 2
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "Exhaust a card",
            "in your hand"
        ],150,c.source,False))
        self.protect()

class finisher(card):
    def __init__(self):
        super().__init__()
        self.cost = 2
        self.dmg = 1
        self.harmful = True
        self.selfTarget = False

    def play(self):
        self.dmg = c.target.b.vulnerable
        self.damage()

class break_the_seal(card):
    def __init__(self):
        super().__init__()
        self.cost = 2
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "Draw until 10",
            "in your hand"
        ],150,c.source,False))
        self.protect()


#region COCKTAIL MIXER

class lemon_up(card):
    def __init__(self):
        super().__init__()
        self.cost = 0
        self.harmful = False
        self.selfTarget = True

    def play(self):
        self.brew(["Added lemonade!"], "lemonade")

class clearly_strong(card):
    def __init__(self):
        super().__init__()
        self.cost = 0
        self.harmful = False
        self.selfTarget = True

    def play(self):
        self.brew(["Added vodka!"], "vodka")

class bump_the_flavour(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        self.brew(["Added squash!"], "squash")

class see_sunrise(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        self.brew(["Added orange juice!"], "orange")

class red_moon(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        self.brew(["Added cranberry juice!"], "cranberry")

class schnapp_to_it(card):
    def __init__(self):
        super().__init__()
        self.cost = 2
        self.harmful = False
        self.selfTarget = True

    def play(self):
        self.brew(["Added peach schnapps!"], "peach")

class blue_moon(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        self.brew(["Added blue curacao!","Exhausted"], "blue")

class gin_to_win(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        self.brew(["Added gin!"], "gin")

class rumaway(card):
    def __init__(self):
        super().__init__()
        self.cost = 2
        self.harmful = False
        self.selfTarget = True

    def play(self):
        self.brew(["Added rum!", "Exhausted"], "rum")

class drunken_wallop(card):
    def __init__(self):
        super().__init__()
        self.cost = 2
        self.harmful = True
        self.selfTarget = False
        self.dmg = 1

    def play(self):
        self.dmg = c.target.b.tipsy
        self.damage()
        self.dmg = 1

class spin_the_bottle(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "Draw 4 cards",
            "Discard 4 cards"
        ],150,c.source,False))

class roulette(card):
    def __init__(self):
        super().__init__()
        self.cost = 0
        self.harmful = False
        self.selfTarget = True

    def play(self):
        if random.randint(0,1)==0:
            iHandler.queue.append(instruction([
                "Gained block!"
            ],150,c.source,False))
            self.block = 2
            self.protect()
        else:
            iHandler.queue.append(instruction([
                "Gained tipsy!"
            ],150,c.source,False))
            self.tipsy(2,c.source)

class ride_the_bus(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = True
        self.selfTarget = False

    def play(self):
        if c.target.b.tipsy > 0:
            self.tipsy(3)
        else:
            self.tipsy(1)

class taste_test(card):
    def __init__(self):
        super().__init__()
        self.cost = 0
        self.sips = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        self.sip()
        c.source.energy += 2

class key_ingredients(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "Take 2 cards",
            "from draw pile"
        ],150,c.source,False))

class seal_of_approval(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "Share drink",
            "both draw 3"
        ],150,c.source,False))

class keep_it_flowing(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.block = 1
        self.harmful = True
        self.selfTarget = False

    def play(self):
        self.tipsy(1)
        self.protect()
        iHandler.queue.append(instruction([
            "draw 1 card",
        ],150,c.source,False))

class get_it_started(card):
    def __init__(self):
        super().__init__()
        self.cost = 2
        self.block = 1
        self.harmful = True
        self.selfTarget = False

    def play(self):
        self.tipsy(1)
        self.protect()
        iHandler.queue.append(instruction([
            "draw 1 card",
        ],150,c.source,False))

class down_the_hatch(card):
    def __init__(self):
        super().__init__()
        self.cost = 2
        self.dmg = 1
        self.harmful = True
        self.selfTarget = False
        self.printEffects = []

    def printAppend(self,text1,val,text2):
        for i in range(len(self.printEffects)):
            if text1 in self.printEffects[i]:
                newVal = int(self.printEffects[i].replace(text1,"").replace(text2,""))+val
                self.printEffects[i]=text1+str(newVal)+text2
                return
        self.printEffects.append(text1+str(val)+text2)
                

    def play(self):
        for effect in c.source.b.store:
            match effect:
                case "vodka":
                    e = random.choice(c.g.enemies)
                    self.dmg = 2
                    self.damage(1,e)
                case "lemonade":
                    self.block = 2
                    self.protect()
                case "squash":
                    c.source.energy += 2
                case "orange":
                    self.heal(1)
                case "cranberry":
                    self.printAppend("Exhaust up to ",2," cards")
                case "peach":
                    self.tipsy(4)
                case "blue":
                    self.tipsy(4,c.source)
                    c.source.b.strength += 1
                case "gin":
                    c.source.b.gin += 1
                case "rum":
                    c.dmg = 2
                    self.damage(1)
                    self.printAppend("Brew ",2," rum")
                    c.source.b.store.append("rum")
                    c.source.b.store.append("rum")
                case _:
                    return
        if len(self.printEffects)>0:
            iHandler.queue.append(instruction(
                self.printEffects
            ,180 * len(self.printEffects) ,c.source,False))


#region WINE CONNOISEUR   

#region DESIGNATED DRIVER