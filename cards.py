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
        #check target is valid
        if self.target is not None and self.target.dead:
            if self.target.name=="enemy":
                for e in self.g.enemies:
                    if not e.dead:
                        self.target = e
                if self.target.dead:
                    self.target = None
            else:
                for p in self.g.players:
                    if not p.dead:
                        self.target = p
                if self.target.dead:
                    self.target = None


        #draw the target marker
        if self.target is not None:
            self.offset = (self.offset+0.02)%(2*math.pi)
            tempY = self.target.y - 32 - 5*math.sin(self.offset)
            tempX = self.target.x+32
            if self.target.name!="enemy":
                tempY += 90
                tempX += 50
            self.g.screen.blit(
                self.img,
                (
                    tempX,
                    tempY
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
            cntr = (self.target.x+self.target.s.x+32,self.target.y+self.target.s.y-24)
            if self.target.name!="enemy":
                cntr = (cntr[0]+150,cntr[1]+150)
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
        #region cocktail mixer
        case "clearstrng":
            return clearly_strong()
        case "lemonup":
            return lemon_up()
        case "downhat":
            return down_the_hatch()
        case "bumpflv":
            return bump_the_flavour()
        case "seesun":
            return see_sunrise()
        case "redmoon":
            return red_moon()
        case "schnapp":
            return schnapp_to_it()
        case "bluemoon":
            return blue_moon()
        case "rumaway":
            return rumaway()
        case "wallop":
            return drunken_wallop()
        case "spinbot":
            return spin_the_bottle()
        case "roulette":
            return roulette()
        case "ridebus":
            return ride_the_bus()
        case "tastetest":
            return taste_test()
        case "keyingred":
            return key_ingredients()
        case "sealappr":
            return seal_of_approval()
        case "keepitfl":
            return keep_it_flowing()
        case "getstart":
            return get_it_started()
        case "gintowin":
            return gin_to_win()
        #region designated driver
        case "supplybag":
            return supply_bag()
        case "notforme":
            return not_for_me()
        case "carry":
            return carry()
        case "hitnrun":
            return hit_and_run()
        case "goodstuff":
            return the_good_stuff()
        case "raidtrunk":
            return raid_trunk()
        case "responsible":
            return be_responsible()
        case "offerlift":
            return offer_lift()
        case "cherrypck":
            return cherry_pick()
        case "soberfoc":
            return sober_focus()
        case "wakeup":
            return wake_up_call()
        case "linestom":
            return line_the_stomach()
        # case "checkin":
        #     return check_in()
        case "maybeone":
            return maybe_just_one()
        case "rulesbroke":
            return rules_broken()
        case "believe":
            return believe_in_you()
        case "freshenup":
            return freshen_up()
        case "checkin":
            return sealant()
        #region beermaster
        case "alcrage":
            return alcoholic_rage()
        case "corona":
            return corona_and_lime()
        case "brewdog":
            return brewdog()
        case "inchs":
            return inchs()
        case "peroni":
            return peroni()
        case "relaxing":
            return relaxing_pint()
        case "ontap":
            return on_tap() 
        case "catchup":
            return catch_up()
        case "chug":
            return chug()
        case "snakebite":
            return snakebite()
        case "wingman":
            return wingman()
        case "beerjack":
            return beer_jacket()
        case "ringfire":
            return ring_of_fire()
        case "splitg":
            return split_the_g()
        case "hellsraise":
            return hellsraiser()
        case "tackychun":
            return tacky_chunder()
        case "finisher":
            return finisher()
        case "breakseal":
            return break_the_seal()
        #region wine connoiseur
        case "grapetime":
            return grape_time()
        case "fruitarom":
            return fruity_aroma()
        case "grape":
            return grape()
        case "royalgam":
            return royal_gamble()
        case "snobbery":
            return snobbery()
        case "vinyard":
            return vinyard()
        case "grapevin":
            return grape_vine()
        case "bottleup":
            return bottle_it_up()
        case "grapedan":
            return grape_dance()
        case "cheesebrd":
            return cheese_board()
        case "floralarom":
            return floral_aroma()
        case "herbalarom":
            return herbal_aroma()
        case "minerarom":
            return mineral_aroma()
        case "pourheart":
            return pour_out_heart()
        case "onemoreg":
            return one_more_glass()
        case "sommelier":
            return sommelier()
        case "grapetrap":
            return grape_trap()
        case "grapeshot":
            return grapeshot()
        case "bottlesmk":
            return bottle_smack()
        case "vacseal":
            return vacuum_seal()
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

    def damage(self, times=1,target = None):
        if target is None: target = c.target
        if target.dead:
            return
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
    
    def protect(self,target=None):
        if target is None: target = c.source

        if target.dead:
            return
        blk = self.block

        frail = target.b.frail
        if frail > 0:
            blk = blk // 2
            target.b.frail -= 1

        target.block += blk
    
    def sip(self,target=  None):
        if target is None: target = c.source
        if target.dead:
            return
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

    def tipsy(self,am,target=None):
        if target is None: target = c.target
        if target.dead:
            return
        target.b.tipsy += am
        if target.b.tipsy >= 5:
            target.b.tipsy.wasted += 1
            target.b.tipsy -= 5

    def draw(self,am,target=None):
        if target is None: target = c.source
        if target.dead:
            return
        iHandler.queue.append(instruction([
            "Draw "+str(am)+f" card{"s" if self.am>1 else ""}"
        ],120,target,False))

    def heal(self,am,target=None):
        if target is None: target = c.source
        if target.dead:
            return
        target.hp = min(target.hp+am,target.hpMax)

    def brew(self,message,addition):
        if c.source.b.alchemist>0:
            self.block = c.source.b.alchemist
            self.protect()
        iHandler.queue.append(instruction(
            message
        ,90,c.source,False))
        c.source.b.store.append(addition)

    def status(self):
        if c.source.b.minAroma > 0:
            e = random.choice(c.g.enemies)
            self.dmg = 1
            self.damage(1,e)

#region GENERIC





#region strike

class strike(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.dmg = 1
        self.harmful = True
        self.selfTarget = False

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
        self.damage()

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
        if c.target.b.tipsy == 0:
            self.tipsy(4)
        else:
            iHandler.queue.append(instruction([
                "target had no tipsy!",
            ],150,c.source,False))

class alchemist(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.block = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        c.source.b.alchemist += 1

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
                    self.printAppend("Draw ",2," cards")
                case "cranberry":
                    self.printAppend("Exhaust up to ",2," cards")
                case "peach":
                    self.tipsy(4)
                case "blue":
                    self.tipsy(3,c.source)
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

class grape(card):
    def __init__(self):
        super().__init__()
        self.cost = 0
        self.dmg = 1
        self.sips = 1
        self.harmful = True
        self.selfTarget = False

    def play(self):
        self.dmg = 1 + c.source.b.sommelier
        if not c.source.b.grapeShot:
            self.damage(1)
        else:
            for e in c.g.enemies:
                self.damage(1,e)
        self.sip()

class grape_time(card):
    def __init__(self):
        super().__init__()
        self.cost = 0
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "Add a grape!"
        ],90,c.source,False))

class fruity_aroma(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "Draw 3 cards",
            "Discard 1 card"
        ],120,c.source,False))

class royal_gamble(card):
    def __init__(self):
        super().__init__()
        self.cost = 0
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "Shuffle 2 dazed",
            "into draw pile"
        ],120,c.source,False))
        self.status()
        c.source.energy += 2

class snobbery(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.block = 2
        self.harmful = True
        self.selfTarget = False

    def play(self):
        iHandler.queue.append(instruction([
            "Add 2 snobbish",
            "to your hand"
        ],120,c.source,False))
        self.status()
        self.protect()
        c.target.b.weak += 1

class vinyard(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "Add 2 grapes",
            "to your hand"
        ],120,c.source,False))

class grape_vine(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "Each turn add",
            "a grape to hand"
        ],120,c.source,False))
        c.source.startTurnText.append("Add a grape")

class bottle_it_up(card):
    def __init__(self):
        super().__init__()
        self.cost = 2
        self.block = 3
        self.harmful = False
        self.selfTarget = True

    def play(self):
        self.protect()

class grape_dance(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "Add 3 grapes",
            "exhaust"
        ],120,c.source,False))

class cheese_board(card):
    def __init__(self):
        super().__init__()
        self.cost = 2
        self.block = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "All players draw 1"
        ],120,None,False))
        for p in c.g.players:
            self.protect(p)

class floral_aroma(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "Exhaust all statuses",
            "in your hand"
        ],120,c.source,False))

class herbal_aroma(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "Whenever you draw",
            "a status, draw 1"
        ],150,c.source,False))

class mineral_aroma(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        c.source.b.minAroma += 1

class pour_out_heart(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "Add an emotional",
            "to your discard pile"
        ],180,c.source,False))
        self.status()
        c.source.energy += 2

class one_more_glass(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "Add a dazed",
            "to your discard pile",
            "draw 2"
        ],180,c.source,False))
        self.status()
        c.source.energy += 2

class sommelier(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        c.source.b.sommelier += 1

class grape_trap(card):
    def __init__(self):
        super().__init__()
        self.cost = 2
        self.harmful = True
        self.selfTarget = False

    def play(self):
        for g in range(c.source.b.grapesPlayed):
            grapeToPlay = grape()
            grapeToPlay.sips = 0
            grape().play(random.choice(c.g.enemies))
        iHandler.queue.append(instruction([
            f"take {c.source.b.grapesPlayed} sips",
        ],210,c.source,False))

class grapeshot(card):
    def __init__(self):
        super().__init__()
        self.cost = 2
        self.harmful = False
        self.selfTarget = True

    def play(self):
        c.source.b.grapeshot += 1
        iHandler.queue.append(instruction([
            "Add 3 grapes",
            "to your hand"
        ],180,c.source,False))

class bottle_smack(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.dmg = 3
        self.harmful = True
        self.selfTarget = False

    def play(self):
        iHandler.queue.append(instruction([
            "Exhausted",
        ],120,c.source,False))
        self.damage()

class vacuum_seal(card):
    def __init__(self):
        super().__init__()
        self.cost = 2
        self.harmful = False
        self.selfTarget = True

    def play(self):
        c.source.b.buffer += 2
        iHandler.queue.append(instruction([
            "Exhausted",
        ],120,c.source,False))

#region DESIGNATED DRIVER

class supply_bag(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = False

    def play(self):
        iHandler.queue.append(instruction([
            "Give a player",
            "a simple potion"
        ],120,c.source,False))

class not_for_me(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        c.source.b.drinkSafe += 1

class carry(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.block = 2
        self.harmful = False
        self.selfTarget = False

    def play(self):
        self.protect(c.target)

class hit_and_run(card):
    def __init__(self):
        super().__init__()
        self.cost = 2
        self.block = 2
        self.dmg = 2
        self.harmful = True
        self.selfTarget = False

    def play(self):
        self.protect()
        self.damage()

class the_good_stuff(card):
    def __init__(self):
        super().__init__()
        self.cost = 2
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "Give a player",
            "a rare potion",
            "exhausted"
        ],120,c.source,False))

class raid_trunk(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "draw 3 cards",
            "exhausted"
        ],120,c.source,False))

class be_responsible(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "Exhaust a card",
            "in someones hand"
        ],120,c.source,False))

class offer_lift(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "Another player draws",
            "a card of their choice"
        ],120,c.source,False))

class cherry_pick(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "Discard any number",
            "from draw pile"
        ],120,c.source,False))

class sober_focus(card):
    def __init__(self):
        super().__init__()
        self.cost = 0
        self.harmful = False
        self.selfTarget = True

    def play(self):
        if c.source.b.drinksThisCombat > 0:
            iHandler.queue.append(instruction([
                "Drank this combat!"
            ],120,c.source,False))
        else:
            c.source.energy += 3

class wake_up_call(card):
    def __init__(self):
        super().__init__()
        self.cost = 0
        self.harmful = False
        self.selfTarget = True

    def play(self):
        if c.source.energy > 0:
            iHandler.queue.append(instruction([
                f"All players draw {c.source.energy}"
            ],120,None,False))
        c.source.energy = 0

class line_the_stomach(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.block = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        for p in c.g.players:
            self.protect(p)

class check_in(card):
    def __init__(self):
        super().__init__()
        self.cost = 0
        self.harmful = False
        self.selfTarget = False

    def play(self):
        self.heal(c.source.energy,c.target)
        c.source.energy = 0

class maybe_just_one(card):
    def __init__(self):
        super().__init__()
        self.cost = 0
        self.sips = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        self.sip()
        c.source.energy += 2

class rules_broken(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        if c.source.b.drinksThisCombat > 0:
            self.draw(c.source.b.drinksThisCombat)
        else:
            iHandler.queue.append(instruction([
                "No drinks taken"
            ],120,None,False))

class believe_in_you(card):
    def __init__(self):
        super().__init__()
        self.cost = 0
        self.harmful = False
        self.selfTarget = False

    def play(self):
        c.target.energy += 2

class freshen_up(card):
    def __init__(self):
        super().__init__()
        self.cost = 1
        self.harmful = False
        self.selfTarget = True

    def play(self):
        iHandler.queue.append(instruction([
            "Exhaust any number",
            "exhausted"
        ],120,None,False))

class sealant(card):
    def __init__(self):
        super().__init__()
        self.cost = 3
        self.harmful = False
        self.selfTarget = True

    def play(self):
        for p in c.g.players:
            if not p.dead and not p.dying:
                p.hp = p.maxHp

        iHandler.queue.append(instruction([
            "exhausted"
        ],90,None,False))