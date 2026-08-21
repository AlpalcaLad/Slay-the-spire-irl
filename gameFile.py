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
import json
import requests

#region Sprite
class sprite():
    def __init__(self,parent,game,asset,scale=100,scaleBy=1,surface=None):
        self.p = parent
        self.g = game
        if surface is None:
            self.img = pygame.image.load(asset).convert_alpha()
            if scale != 100:
                self.img = pygame.transform.scale(self.img,(scale,scale))
            if scaleBy != 1:
                self.img = pygame.transform.scale_by(self.img,scaleBy)
        else:
            self.img = surface
        self.x = 0
        self.y = 0
        self.a = 1

    def draw(self):
        if self.a != 1:
            self.img.set_alpha(self.a)
        self.g.screen.blit(
            self.img,
            (
                self.p.x + self.x,
                self.p.y + self.y
            ),
        )

#region TODO: Animation

class animation():
    def __init__(self,game,folder,animSpeed=0.1,repeat=False,scaleBy=1):
        self.g = game
        self.f = folder
        self.anim = animSpeed
        self.scale = scaleBy


#region Asset Holder

class assetHolder():
    def __init__(self):
        #self.blockAsset = self.load("./art/icons/blockIcon.png")
        self.energyAsset = self.load("./art/icons/energyIcon.png")
        self.noEnergyAsset = self.load("./art/icons/energylessIcon.png")

        self.vulnerableAsset = self.load("./art/icons/vulnerableIcon.png",25)
        self.weakAsset = self.load("./art/icons/weakIcon.png",25)
        self.frailAsset = self.load("./art/icons/frailIcon.png",25)
        self.strengthAsset = self.load("./art/icons/strengthIcon.png",25)

        self.attackAsset = self.load("./art/icons/attackingIcon.png",35)
        self.beerAsset = self.load("./art/icons/beerIcon.png")
        self.asleepAsset = self.load("./art/icons/asleepIcon.png")
        self.blockAsset = self.load("./art/icons/defendIcon.png")
        self.buffAsset = self.load("./art/icons/buffIcon.png")
        self.debuffAsset = self.load("./art/icons/debuffIcon.png")
        self.mysteryAsset = self.load("./art/icons/mysteryIcon.png")
        self.stunAsset = self.load("./art/icons/stunnedIcon.png")
        self.attackDefendAsset = self.load("./art/icons/attackDefendIcon.png",35)
        self.escapeAsset = self.load("./art/icons/escapeIcon.png",35)

        self.ritualAsset = self.load("./art/icons/ritualIcon.png",35)
        self.thornsAsset = self.load("./art/icons/thornsIcon.png",35)
        self.platingAsset = self.load("./art/icons/platingIcon.png",25)
        self.shellAsset = self.load("./art/icons/hardenedShell.png",25)
        self.shriekAsset = self.load("./art/icons/shriekIcon.png",25)

        self.ginAsset = self.load("./art/icons/ginIcon.png",25)
        self.bufferAsset = self.load("./art/icons/bufferIcon.png",25)

        #hellsraiser, grapeVine, herbAroma, minAroma, sommelier, alchemist, grapeshot
        self.hellsraiserAsset = self.load("./art/icons/hellIcon.png",25)
        self.vineAsset = self.load("./art/icons/vineIcon.png",25)
        self.herbAsset = self.load("./art/icons/herbIcon.png",25)
        self.minAsset = self.load("./art/icons/minIcon.png",25)
        self.sommelierAsset = self.load("./art/icons/grapeDamageIcon.png",35)
        self.alchemistAsset = self.load("./art/icons/alchemistIcon.png",25)
        self.grapeshotAsset = self.load("./art/icons/grapeshotIcon.png",25)

    def load(self,path,scale = 45):
        return pygame.transform.scale(pygame.image.load(path).convert_alpha(),(scale,scale))


#region Buff handler
class buffHandler():
    def __init__(self,p):
        self.p = p

        self.vulnerable = 0
        self.weak = 0
        self.frail = 0
        self.strength = 0
        self.tipsy = 0
        self.wasted = 0

        self.gin = 0

        self.permaStrength = 0
        self.permaPlating = 0

        #special
        self.store: list[tuple] = [] #stored effects
        self.drinkSafe = 0
        self.drinksThisCombat = 0

        #powers
        self.hellsraiser = 0
        self.grapeVine = 0
        self.herbAroma = 0
        self.minAroma = 0
        self.sommelier = 0
        self.alchemist = 0
        self.grapeshot = 0
        self.buffer = 0

        self.ritual = 0
        self.plating = 0
        self.hardenedShell = 0
        self.damageTaken = 0
        self.shriek = 0

        self.grapesPlayed = 0

        self.freeCard = 0

        self.freeCardNames = []

    def reset(self):
        self.strength = self.permaStrength
        self.weak = 0
        self.tipsy = 0
        self.vulnerable = 0

        self.store: list[tuple] = [] #stored effects
        self.drinkSafe = 0
        self.drinksThisCombat = 0

        self.hellsraiser = 0
        self.grapeVine = 0
        self.herbAroma = 0
        self.minAroma = 0
        self.sommelier = 0
        self.alchemist = 0
        self.grapeShot = 0
        self.buffer = 0
    
        self.ritual = 0
        self.plating = self.permaPlating
        self.hardenedShell = 0
        self.damageTaken = 0
        self.shriek = 0

        self.grapesPlayed = 0

        self.freeCardNames = []
    
    def startturn(self):
        # if self.weak>0: self.weak -= 1
        # if self.vulnerable>0: self.vulnerable -= 1
        # if self.frail>0: self.frail -= 1
        # if self.wasted>0: self.wasted -= 1
        if self.ritual>0: self.strength += self.ritual
        self.freeCard = 0

    def endturn(self):
        if self.plating>0:
            self.p.block += self.plating
            self.plating-=1
        if self.weak>0: self.weak -= 1
        if self.vulnerable>0: self.vulnerable -= 1
        if self.frail>0: self.frail -= 1
        if self.wasted>0: self.wasted -= 1

    def itemise(self, assets: assetHolder) -> list[tuple[int,pygame.Surface]]:
        effects = []
        if self.vulnerable>0:
            effects.append((str(self.vulnerable),assets.vulnerableAsset))
        if self.weak>0:
            effects.append((str(self.weak),assets.weakAsset))
        if self.frail>0:
            effects.append((str(self.frail),assets.frailAsset))
        if self.strength>0:
            effects.append((str(self.strength),assets.strengthAsset))
        if self.ritual>0:
            effects.append((str(self.ritual),assets.ritualAsset))
        if self.plating>0:
            effects.append((str(self.plating),assets.platingAsset))
        if self.hardenedShell>0:
            effects.append((str(self.hardenedShell-self.damageTaken),assets.shellAsset))
        if self.shriek>0:
            effects.append((str(self.shriek),assets.shriekAsset))
        if self.gin>0:
            effects.append((str(self.gin),assets.ginAsset))
        if self.buffer>0:
            effects.append((str(self.buffer),assets.bufferAsset))
        if self.hellsraiser>0:
            effects.append((-1,assets.hellsraiserAsset))
        if self.alchemist>0:
            effects.append((-1,assets.alchemistAsset))
        if self.grapeshot>0:
            effects.append((-1,assets.grapeshotAsset))
        if self.herbAroma>0:
            effects.append((-1,assets.herbAsset))
        if self.minAroma>0:
            effects.append((-1,assets.minAsset))
        if self.sommelier>0:
            effects.append((str(self.sommelier),assets.sommelierAsset))
        if self.grapeVine>0:
            effects.append((-1,assets.vineAsset))

        return effects

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
        self.dead = False
        self.dying = False

        #buffs and debuffs
        self.b = buffHandler(self)

    def damage(self,dmg):
        if self.dead:
            return
        blockAm = min(dmg,self.block)
        self.block -= blockAm

        dmg -= blockAm
        if dmg > 0:
            if self.b.buffer > 0:
                self.b.buffer -= 1
                return
            self.hp -= dmg

        if self.hp <= 0:
            self.dying = True

    def die(self):
        self.dead = True
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
                self.g.a.blockAsset,
                (
                    self.x-40,
                    self.y-13
                ),
            )
            drawTextOutlined(self.g,str(self.p.block),(self.x-10,self.y-3),(20,20,100),(255,255,255))
            hpBarCol = (100,180,255)

        #health
        ratio = self.p.hp / max(1,self.p.hpMax)
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
                self.g.a.energyAsset,
                (
                    self.x+self.w+8,
                    self.y-43
                ),
            )
            drawTextOutlined(self.g,str(self.p.energy),(self.x+self.w+42,self.y-38),(100,60,20),(255,255,255))
        elif self.p.energy==0: #draw dull sprite
            self.g.screen.blit(
                self.g.a.noEnergyAsset,
                (
                    self.x+self.w+8,
                    self.y-43
                ),
            )
            drawTextOutlined(self.g,str(self.p.energy),(self.x+self.w+42,self.y-38),(80,50,10),(160,160,160))

        #buffs and debuffs
        toDraw = self.p.b.itemise(self.g.a)
        curX = self.x
        for e in toDraw:
            #draw effect
            if e[0] != -1:
                drawTextOutlined(self.g,e[0],(curX,self.y+23),(255,255,255),(0,0,0))
            else:
                curX -= 15
            #blit icon to screen
            self.g.screen.blit(
                e[1],
                (
                    curX,
                    self.y+23
                ),
            )
            curX += 50


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

        self.baseY = self.y
        self.vsp = 0
        self.grv = 0.2

        self.energyMax = 3
        self.energy = self.energyMax
        self.friendly = True

        self.dead = False

        self.shakeTime = 0

        self.awaitingCard = None

        self.startTurnText = [
            "Draw 4 cards"
        ]

        match className: #setup player class
            case "cocktail":
                self.hp=10
                self.deck = []
                self.s = sprite(self,g,"./art/characters/cocktail.png",scaleBy=0.2)
                self.x = 2*self.g.W//5-55
                self.hatchEffects = []
            case "beermaster":
                self.hp=10
                self.s = sprite(self,g,"./art/characters/beer.png",scaleBy=0.2)
                self.x = 1*self.g.W//5-45
            case "winecon":
                self.hp=10
                self.s = sprite(self,g,"./art/characters/wine.png",scaleBy=0.2)
                self.x = 3*self.g.W//5-35
                self.wine = 0
            case "driver":
                self.hp=10
                self.s = sprite(self,g,"./art/characters/driver.png",scaleBy=0.2)
                self.x = 4*self.g.W//5-25
            case _:
                self.s = sprite(self,g,"./art/player1Art.png")

        self.hpMax = self.hp
        self.className = className

        self.sd = sprite(self,g,surface=greyscale(self.s.img),asset="")

        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)

    def play(self,cardText):
        if not self.g.playerTurn:
            self.g.actionQueue.append((self.play,cardText))
            return
        
        cardToPlay = getcard(cardText)

        #playing harmful card targetted at player
        if cardToPlay.harmful and c.target.friendly:
            iHandler.queue.append(instruction([
                "Cannot harm another player!"
            ],120,c.source,False))

        #playing helping card targetted at enemy
        if not cardToPlay.harmful and not cardToPlay.selfTarget and not c.target.friendly:
            iHandler.queue.append(instruction([
                "Cannot help an enemy!"
            ],120,c.source,False))

        if not cardToPlay.harmful and cardToPlay.selfTarget and c.target==c.source:
            iHandler.queue.append(instruction([
                "Must target someone else",
            ],120,c.source,False))

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
            if cardToPlay.dmg > 0:
                self.vsp = -6
                self.awaitingCard = cardToPlay
            else:
                cardToPlay.play()
        

    def draw(self):
        if self.dead and self.hp > 0:
            self.dead = False

        if self.vsp != 0:
            if self.y + self.vsp >= self.baseY:
                self.y = self.baseY
                self.vsp = 0
                if self.awaitingCard is not None:
                    c.source = self
                    self.awaitingCard.play()
            else:
                self.y += self.vsp
                self.vsp += self.grv

        if not self.dying and not self.dead:
            if self.y > self.baseY:
                self.y = lerp(self.y,self.baseY,0.1)
                if abs(self.y-self.baseY)<0.01:
                    self.y = self.baseY
            self.s.draw()
        else:
            if self.y < self.baseY+40:
                self.y = lerp(self.y,self.baseY+40,0.1)
                if abs(self.y-self.baseY+40)<0.01:
                    self.y = self.baseY+40
                    self.dead=True
                    self.dying = False
            self.sd.draw()
        self.h.draw()

    def endturn(self):
        if not self.dead:
            self.b.endturn()

    def startturn(self):
        if not self.dead:
            self.block = 0
            self.energy = self.energyMax
            self.b.startturn()
            iHandler.queue.append(instruction(
                self.startTurnText,
                150,self,False
            ))
        else:
            pass
            #self.b.reset()

    def reset(self):
        self.dead = False
        self.hp = self.hpMax
        self.b.reset()
        self.energy = self.energyMax
        self.block = 0
        self.startTurnText = [
            "Draw 4 cards"
        ]

    def combatEnd(self):
        self.dead=False
        self.hp = max(1,self.hp)
        self.b.reset()
        self.energy = self.energyMax
        self.block = 0
        self.startTurnText = [
            "Draw 4 cards"
        ]

colours = {
    "black": (0,0,0),
    "white": (255,255,255)
}


#region Game
import pygame._sdl2 as sdl2
class game():
    def __init__(self):
        #general setup
        self.run = True
        self.cardsToBePlayed = []

        self.API_URL = "https://opentdb.com/api.php?amount=50&category=22"
        self.response = requests.get(self.API_URL)
        self.data = json.loads(self.response.text)["results"]

        #basic pygame setup
        pygame.init()
        self.W, self.H = 960, 540
        self.x,self.y = 0,0
        flags = pygame.SCALED
        flags |= pygame.RESIZABLE

        self.screen = pygame.display.set_mode((self.W,self.H), flags | pygame.HIDDEN)
        scale_fact = 2
        window = sdl2.Window.from_display_module()
        window.size = (self.W * scale_fact, self.H * scale_fact)
        window.position = sdl2.WINDOWPOS_CENTERED
        window.show()

        pygame.display.set_caption("Slay the Spire IRL")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("kreon", 22)
        self.eventFont = pygame.font.SysFont("kreon", 36)

        #UI definition
        self.backdrops = [
            sprite(self,self,"./art/spireBackground.jpg",scaleBy=1.5)
            # sprite(self,self,"./art/backdropSky.png"),
            # sprite(self,self,"./art/backdropTree.png"),
            # sprite(self,self,"./art/backdropGrass.png")
        ]
        c.img = pygame.image.load(c.asset).convert_alpha()
        self.a : assetHolder = assetHolder()
        c.g = self
        self.c = c
        iHandler.g = self
        self.iHandler = iHandler

        #gameplay definition
        self.players: list[player] = []
        self.enemies: list[enemy] = []
        self.actionQueue = []
        self.playerTurn = True #whether players can play cards
        self.inCombat = False
        self.eliteCombat = False

        self.startTime = time.time()
        self.score = 0
        self.scoreSources = []

    def addScore(self,am,reason="special"):
        self.scoreSources.append((am,reason))
        self.score += am

    def question(self):
        qVal = None
        while qVal is None or len(qVal["incorrect_answers"])<3 or qVal["difficulty"] not in ["easy","medium"] or len(qVal["question"])>50:
            if len(self.data)<=0:
                self.response = requests.get(self.API_URL)
                self.data = json.loads(self.response.text)["results"]
            qVal = self.data.pop(0)
        return qVal

    def reset(self):
        self.startTime = time.time()
        raise NotImplementedError("Reset is currently handled at main.py level...")

    def endturn(self):
        for p in self.players:
            if p.acting:
                self.actionQueue.append((self.endturn,))
                return

        for p in self.players:
            p.endturn()
        
        self.playerTurn = False

        for e in self.enemies:
            e.startturn()
        for e in self.enemies:
            e.act()

    def mapToChar(self,string):
        if string=="1":
            return "beermaster"
        elif string=="2":
            return "cocktail"
        elif string=="3":
            return "winecon"
        else:
            return "driver"

    #region Game - readCard
    def readCard(self,cardText: str):
        if cardText == "endturn":
            self.endturn()

        if cardText in ["cocktail","beermaster","winecon","driver"]:
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

        elif len(cardText)>2 and cardText[-1] in ["1","2","3","4"]:
            charName = self.mapToChar(cardText[-1])
            for p in self.players:
                if p.className == charName:
                    tempText = cardText[:-1]
                    if tempText[-1].isupper():
                        p.play(tempText[:-1])
                    else:
                        p.play(tempText)
        
        elif getenemy(cardText) is not None:# or getenemy(cardText[:-1]) is not None:
            # for p in self.players: 
            #     p.energy = (p.energy + 1) * 2
            #     p.block = (p.block + 1) * 2
            #     iHandler.queue.append(instruction(
            #         ["draw 2 cards"],
            #         60,
            #         p,
            #         False
            #     ))

            if len(self.enemies) == 0:
                self.inCombat = True

            tempText = cardText
            # if tempText[-1].isupper():
            #     tempText=tempText[:-1]

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
                incrX = self.W/(len(self.enemies)+1)
                for i in range(len(self.enemies)):
                    self.enemies[i].x = incrX * (i+1) - 75
                    self.enemies[i].h.x = self.enemies[i].x #update healthbar positions
        
        elif cardText.startswith("event"):
            tempText = cardText
            if tempText[-1].isupper():
                tempText=tempText[:-1]

            iHandler.queue.append(getevent(tempText.replace("event","",1)))

        elif cardText == "rest":
            if not self.inCombat:
                for p in self.players:
                    p.hp = max(p.hp,p.hpMax//2)
                    p.dead = False
                    p.dying = False

        elif cardText == "shopShot":
            self.addScore(2,"shop")
            iHandler.queue.append(instruction(
                ["Take a shot!"],-1,None,True,rewards
            ))

        elif cardText=="pubquiz":
            #load up pub quiz question
            quizQ = self.question()
            quizT = [quizQ["question"]]
            correctAns = random.randint(0,3)

            #before correct
            for i in range(correctAns):
                quizT.append(quizQ["incorrect_answers"][i]+f" ({i+1})")
            #correct
            quizT.append(quizQ["correct_answer"]+f" ({correctAns+1})")
            #after correct
            for i in range(correctAns+1,4):
                quizT.append(quizQ["incorrect_answers"][i-1]+f" ({i+1})")

            rewards = [
                instruction(
                    ["Incorrect! The answer was "+quizQ["correct_answer"],"You move on a failiure..."],
                    360,None,True
                )for i in range(4)
            ]

            rewards[correctAns]=instruction(
                ["Correct! You recieve 2 gold each as a reward."],
                300, None, True
            )
            iHandler.queue.append(instruction(
                quizT,-1,None,True,rewards
            ))

        elif cardText.startswith("pot"):
            #potions
            match cardText:
                case "potWeak":
                    if self.inCombat: c.target.b.weak += 1
                case "potStrength":
                    if self.inCombat: c.target.b.strength += 1
                case "potDraw":
                    if self.inCombat: iHandler.queue.append(instruction([
                        "draw 2 cards"
                    ],90,c.target))
                case "potVuln":
                    if self.inCombat: c.target.b.vulnerable += 1
                case "potTipsy":
                    if self.inCombat: c.target.b.tipsy += 3
                case "potEnergy":
                    if self.inCombat and c.target.friendly:
                        c.target.energy += 2
                case "potExhaust":
                    if self.inCombat: iHandler.queue.append(instruction([
                        "exhaust 2 cards"
                    ],90,c.target))
                case "potDamage":
                    if self.inCombat: c.target.damage(2)
                case "potHeal":
                    c.target.hp = min(c.target.hp + 1, c.target.hpMax)
                case "potFree":
                    c.target.b.freeCard += 1
                case "potRMaxHP":
                    if c.target.friendly:
                        c.target.hpMax += 1
                        c.target.hp += 1
                case "potRStrength":
                    if c.target.friendly:
                        c.target.b.permaStrength += 1
                        if self.inCombat:
                            c.target.b.strength += 1
                case "potRDamage":
                    if self.inCombat: c.target.damage(6)
                case "potRScore":
                    self.addScore(5,"potion")
                case "potRStun":
                    if self.inCombat and not c.target.friendly:
                        e:enemy = c.target
                        e.intentions.insert(0,intent(e,"stun",[],False))
                case "potRRemove":
                    iHandler.queue.append(instruction([
                        "permenantly remove a card"
                    ],90,c.target))
                case "potRPlating":
                    c.target.b.permaPlating+=1
                case "potRRitual":
                    c.target.b.ritual += 1
                case "potRFullHeal":
                    c.target.hp = c.target.hpMax
                case "potRReward":
                    iHandler.queue.append(instruction([
                        "Gain a 5-option card reward"
                    ],120,c.target))
                case _:
                    pass

        elif len(cardText)==2: #pub quiz answer
            if len(iHandler.active)>0 and len(iHandler.active[0].options)>=int(cardText[1]):
                #answer question
                #print(cardText[1],iHandler.active[0].options[int(cardText[1])].text)
                iHandler.queue.append(iHandler.active[0].options[int(cardText[1])-1])
                iHandler.active[0].duration=0

        print("Read card ",cardText)
        return

    def setup(self):
        sharedArray = []
        self.cardsToBePlayed = sharedArray
        return sharedArray

    #region Game - mainloop
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
                for e in self.enemies:
                    e.b.endturn()
                self.playerTurn = True
                for p in self.players:
                    p.startturn()

        #check if all enemies dead and in combat
        if len(self.enemies)==0 and self.inCombat:
            self.playerTurn = False
            for p in self.players:
                p.combatEnd()

            #reward instructions
            if self.eliteCombat:
                self.eliteCombat = False
                iHandler.queue.append(instruction(
                    ["Everyone gets 1 rare potion","Everyone gets 1 card reward","1 gold each"],
                    300,blocking=True
                ))
                self.addScore(5,"elite")
            else:
                iHandler.queue.append(instruction(
                    ["Everyone gets 1 simple potion","Everyone gets 1 card reward","1 gold each"],
                    300,blocking=True
                ))
                self.addScore(2,"enemy")

        #check if all players dead
        if len(self.players)>0:
            found = False
            for p in self.players:
                if not p.dead:
                    found = True
                    break
            if not found:
                #All players died, show endscreen
                iHandler.queue.append(instruction([
                    "You died...",
                    "You achieved a final score and time of",
                    f"{self.score} points, {secondsToTime(int(time.time()-self.startTime))}"
                ],-1,None,True))
        
        #render enemies
        for e in self.enemies:
            if self.inCombat and e.elite:
                self.eliteCombat = True
            e.draw()

        #render misc ui
        c.draw()

        #render events
        iHandler.draw()

        #finish up
        pygame.display.flip()

    def waitTick(self,fps):
        self.clock.tick(fps)