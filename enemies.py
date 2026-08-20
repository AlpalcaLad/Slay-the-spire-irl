from gameFile import sprite, healthbar, entity
import math
from helperFuncs import *
from cards import *

def getenemy(enemyname):
    match enemyname:
        case "byrdonis":
            return byrdonis
        case "cultist":
            return cultist
        case "fossilstlk":
            return fossil_stalker
        case "frogknight":
            return frog_knight
        case "gianthead":
            return giant_head
        case "lagavulin":
            return lagavulin
        case "leafslime":
            return leaf_slime
        case "mawler":
            return mawler
        case "nibbit":
            return nibbit
        case "orbwalker":
            return orb_walker
        case "skulkcol":
            return skulking_colony
        case "slaverA":
            return slaverA
        case "slaverB":
            return slaverB
        case "slaverC":
            return slaverB
        case "terroreel":
            return terror_eel
        case "thiefA" | "thiefB":
            return thief
        case "vineshamb":
            return vine_shambler
        case _:
            return None
#region intent
class intent():
    def __init__(self,p,action: str, values: list[int], repeat:bool=True):
        self.action = action
        self.values = values
        self.p = p
        self.g = p.g
        self.repeat = repeat

        self.asset = None
        match self.action:
            case "attack":
                self.asset = self.p.g.a.attackAsset
            case "defend":
                self.asset = self.p.g.a.blockAsset
            case "attack_defend":
                self.asset = self.p.g.a.attackDefendAsset
            case "drink":
                self.asset = self.p.g.a.beerAsset
            case "buff":
                self.asset = self.p.g.a.buffAsset
            case "debuff":
                self.asset = self.p.g.a.debuffAsset
            case "sleep":
                self.asset = self.p.g.a.asleepAsset
            case "mystery":
                self.asset = self.p.g.a.mysteryAsset
            case "stun":
                self.asset = self.p.g.a.stunAsset
            case "escape":
                self.asset = self.p.g.a.escapeAsset
            case _:
                return

    def draw(self):
        match self.action:
            case "attack" | "attack_defend":
                self.g.screen.blit(
                    self.asset,
                    (
                        self.p.x+90,
                        self.p.y-40
                    ),
                )

                if self.values[1] > 1:
                    self.printVal = str(self.values[0])+"x"+str(self.values[1])
                else:
                    self.printVal = str(self.values[0])

                drawTextOutlined(self.g,self.printVal,(self.p.x+90,self.p.y-40),(100,60,20),(255,255,255))

            case "drink":
                self.g.screen.blit(
                    self.asset,
                    (
                        self.p.x+90,
                        self.p.y-40
                    ),
                )
                drawTextOutlined(self.g,str(self.values[0]),(self.p.x+90,self.p.y-40),(100,60,20),(255,255,255))
            case "buff" | "debuff" | "sleep" | "mystery" | "stun" | "defend" | "escape":
                self.g.screen.blit(
                    self.asset,
                    (
                        self.p.x+90,
                        self.p.y-40
                    ),
                )
            case _:
                return


    def damage(self, am: int, times: int):
        for player in self.g.players:
            if p.dead: continue
            dmg = am

            strength = self.p.b.strength
            weak = self.p.b.weak
            vulnerable = player.b.vulnerable
            wasted = player.b.wasted
            
            dmg += strength
            if vulnerable > 0:
                dmg *= 2
                player.b.vulnerable -= 1
            if weak > 0:
                dmg = dmg // 2
                self.p.b.weak -= 1
            if wasted>0:
                dmg*=2

            for t in range(times):
                player.damage(dmg)

    def defend(self, am: int):
        blk = am
        
        if self.p.b.frail > 0:
            blk = blk // 2
            self.p.b.frail -= 1

        self.p.block += blk

    def sip(self, sips: int):
        if sips > 0:
            for p in self.g.players:
                if p.dead: continue
                p.b.drinkSafe -= self.sips
                if p.b.drinkSafe < 0:
                    p.b.drinkSafe = 0
                    iHandler.queue.append(instruction([
                        "take "+str(sips)+" sips!"
                    ],90,c.source,False))
                    p.b.drinksThisCombat += 1

    def act(self):
        match self.action:
            case "attack":
                self.damage(self.values[0],self.values[1])
            case "defend":
                self.defend(self.values[0])
            case "attack_defend":
                self.damage(self.values[0],self.values[1])
                self.defend(self.values[2])
            case "drink":
                self.sip(self.values[0])
            case "buff":
                match self.values[0]:
                    case "strength":
                        self.p.b.strength += self.values[1]
                    case "ritual":
                        self.p.b.ritual += self.values[1]
                    case _:
                        pass
            case "debuff":
                match self.values[0]:
                    case "frail":
                        for p in self.g.players:
                            p.b.frail += self.values[1]
                    case "vulnerable":
                        for p in self.g.players:
                            p.b.vulnerable += self.values[1]
                    case "weak":
                        for p in self.g.players:
                            p.b.weak += self.values[1]
                    case "strength":
                        for p in self.g.players:
                            p.b.strength -= self.values[1]
                    case _:
                        pass
            case "mystery":
                if self.values[0]=="instruction":
                    iHandler.queue.append(self.values[1])
                if self.values[0]=="allInstruction":
                    for p in self.g.players:
                        iHandler.queue.append(instruction(self.values[1],self.values[2],p))
            case "escape":
                if self.p in self.g.enemies:
                    if len(self.g.enemies)==1:
                        self.g.inCombat = False
                        self.g.eliteCombat = False
                    self.g.enemies.remove(self.p)
                #region TODO escape fog
            case _:
                return

#region enemy
class enemy(entity):
    def __init__(self,g):
        super().__init__()
        self.g = g
        self.y = self.g.H - 460
        self.intentions: list[intent] = []
        self.elite = False

        self.baseY = self.y
        self.vsp = 0
        self.grv = 0.2
        self.intentionWaiting : intent = None
    
    def draw(self):
        if len(self.intentions)>0:
            self.intentions[0].draw()

        if self.vsp != 0:
            self.vsp += self.grv
            self.y += self.vsp
            if self.y + self.vsp > self.baseY:
                self.y = self.baseY
                self.vsp = 0
                self.intentionWaiting.act()
                if self.intentionWaiting.repeat:
                    self.intentions.append(self.intentionWaiting)

    def act(self):
        self.b.startturn()

        if len(self.intentions) > 0:
            cur = self.intentions.pop(0)
            if cur.action in ["attack","attack_defend"]:
                self.vsp = -6
            else:
                cur.act()
                if cur.repeat:
                    self.intentions.append(cur)

    def startturn(self):
        self.block = 0

    def die(self):
        self.dead = True
        if self in self.g.enemies:
            self.g.enemies.remove(self)
            #todo mini explosion animation

#region boss

class scorebar():
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

        #score
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
            drawTextOutlined(self.g,e[0],(curX,self.y+23),(255,255,255),(0,0,0))
            #blit icon to screen
            self.g.screen.blit(
                e[1],
                (
                    curX,
                    self.y+23
                ),
            )
            curX += 50

class boss(enemy):
    def __init__(self,g):
        super().__init__(g)
        self.hp = -1
        self.hpMax = self.hp
        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)
        self.s = sprite(self,g,"./art/enemies/byrdonis.png",300)
        self.s.x=-30
        self.s.y=-40
        self.intentions = [
            intent(self,"attack",[2,1]),
            intent(self,"attack",[1,3]),
            intent(self,"buff",["strength",1])
        ]
        self.elite = True
        self.boss = True
        
    def draw(self):
        super().draw()
        self.s.draw()
        self.h.draw()

#region byrdonis
class byrdonis(enemy):
    def __init__(self,g):
        super().__init__(g)
        self.hp = 13 * len(self.g.players)
        self.hpMax = self.hp
        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)
        self.s = sprite(self,g,"./art/enemies/byrdonis.png",300)
        self.s.x=-30
        self.s.y=-40
        self.intentions = [
            intent(self,"attack",[2,1]),
            intent(self,"attack",[1,3]),
            intent(self,"buff",["strength",1])
        ]
        self.elite = True
    
    def draw(self):
        super().draw()
        self.s.draw()
        self.h.draw()
#region cultist
class cultist(enemy):
    def __init__(self,g):
        super().__init__(g)
        self.hp = 7  * len(self.g.players)
        self.hpMax = self.hp
        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)
        self.s = sprite(self,g,"./art/enemies/cultist.png",200)
        self.intentions = [
            intent(self,"buff",["ritual",1],False),
            intent(self,"attack",[1,1])
        ]
    
    def draw(self):
        super().draw()
        self.s.draw()
        self.h.draw()
#region fossil stalker
class fossil_stalker(enemy):
    def __init__(self,g):
        super().__init__(g)
        self.hp = 10 * len(self.g.players)
        self.hpMax = self.hp
        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)
        self.s = sprite(self,g,"./art/enemies/fossil_stalker.png",200)
        self.intentions = [
            intent(self,"attack",[1,2]),
            intent(self,"buff",["strength",1])
        ]
    
    def draw(self):
        super().draw()
        self.s.draw()
        self.h.draw()

#region frog knight
class frog_knight(enemy):
    def __init__(self,g):
        super().__init__(g)
        self.hp = 6 * len(self.g.players)
        self.hpMax = self.hp
        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)
        self.s = sprite(self,g,"./art/enemies/frog_knight.png",200)
        self.b.plating = 2 * len(self.g.players)
        self.block = self.b.plating
        self.intentions = [
            intent(self,"debuff",["frail",3]),
            intent(self,"attack",[2,1]),
            intent(self,"buff",["strength",1]),
            intent(self,"drink",[2])
        ]
    
    def draw(self):
        super().draw()
        self.s.draw()
        self.h.draw()

#region Giant Head
class giant_head(enemy):
    def __init__(self,g):
        super().__init__(g)
        self.hp = 18 * len(self.g.players)
        self.hpMax = self.hp
        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)
        self.s = sprite(self,g,"./art/enemies/giant_head.png",300)
        self.s.x-=30
        self.s.y-=40
        self.intentions = [
            intent(self,"mystery",["instruction",
                instruction(["3..."],120,self)
            ],False),
            intent(self,"mystery",["instruction",
                instruction(["2..."],120,self)
            ],False),
            intent(self,"mystery",["instruction",
                instruction(["1..."],120,self)
            ],False),
            intent(self,"attack",[6,1]),
        ]
        self.elite = True
    
    def draw(self):
        super().draw()
        self.s.draw()
        self.h.draw()

#region Lagavulin
class lagavulin(enemy):
    def __init__(self,g):
        super().__init__(g)
        self.hp = 14 * len(self.g.players)
        self.hpMax = self.hp
        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)
        self.s = sprite(self,g,"./art/enemies/lagavulin_sleep.png",300)
        self.s2 = sprite(self,g,"./art/enemies/lagavulin.png",300)
        self.x-=30
        self.y-=40
        self.b.plating = 2 * len(self.g.players)
        self.block = self.b.plating
        self.intentions = [
            intent(self,"mystery",["instruction",
                instruction(["..."],120,self)
            ],False),
            intent(self,"mystery",["instruction",
                instruction(["..?"],120,self)
            ],False),
            intent(self,"mystery",["instruction",
                instruction(["..!"],120,self)
            ],False),
            intent(self,"attack",[3,1]),
            intent(self,"attack",[3,1]),
            intent(self,"drink",[2]),
            intent(self,"debuff",["strength",1]),
        ]
        self.elite = True

    def damage(self,dmg):
        super().damage(dmg)
        if self.b.plating > 0 and self.hp < self.hpMax:
            self.plating = 0
        if self.hp < self.hpMax and self.intentions[0].action=="mystery":
            self.intentions = [
                intent(self,"stun",[],False),
                intent(self,"attack",[3,1]),
                intent(self,"attack",[3,1]),
                intent(self,"defend",[2 * len(self.g.players)]),
                intent(self,"debuff",["strength",1]),
            ]

    
    def draw(self):
        super().draw()
        if self.intentions[0].action=="mystery":
            self.s.draw()
        else:
            self.s2.draw()
        self.h.draw()

#region leaf slime
class leaf_slime(enemy):
    def __init__(self,g):
        super().__init__(g)
        self.hp = 5 * len(self.g.players)
        self.hpMax = self.hp
        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)
        self.s = sprite(self,g,"./art/enemies/leaf_slime.png",200)
        self.intentions = [
            intent(self,"attack",[1,1]),
            intent(self,"debuff",["weak",2]),
            intent(self,"attack",[1,1]),
            intent(self,"debuff",["frail",2]),
        ]
    
    def draw(self):
        super().draw()
        self.s.draw()
        self.h.draw()

#region mawler
class mawler(enemy):
    def __init__(self,g):
        super().__init__(g)
        self.hp = 8 * len(self.g.players)
        self.hpMax = self.hp
        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)
        self.s = sprite(self,g,"./art/enemies/mawler.png",200)
        self.intentions = [
            intent(self,"attack",[1,1]),
            intent(self,"attack",[2,1]),
            intent(self,"defend",[3]),
            intent(self,"attack",[3,1]),
        ]
    
    def draw(self):
        super().draw()
        self.s.draw()
        self.h.draw()

#region nibbit
class nibbit(enemy):
    def __init__(self,g):
        super().__init__(g)
        self.hp = 8 * len(self.g.players)
        self.hpMax = self.hp
        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)
        self.s = sprite(self,g,"./art/enemies/nibbit.png",200)
        self.intentions = [
            intent(self,"attack",[1,2]),
            intent(self,"defend",[3]),
            intent(self,"buff",["strength",1]),
        ]
    
    def draw(self):
        super().draw()
        self.s.draw()
        self.h.draw()

#region orb walker
class orb_walker(enemy):
    def __init__(self,g):
        super().__init__(g)
        self.hp = 10 * len(self.g.players)
        self.hpMax = self.hp
        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)
        self.s = sprite(self,g,"./art/enemies/nibbit.png",200)
        self.intentions = [
            intent(self,"attack",[1,3]),
            intent(self,"drink",[1]),
            intent(self,"buff",["strength",1]),
        ]
    
    def draw(self):
        super().draw()
        self.s.draw()
        self.h.draw()

#region skulking colony
class skulking_colony(enemy):
    def __init__(self,g):
        super().__init__(g)
        self.hp = 12 * len(self.g.players)
        self.hpMax = self.hp
        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)
        self.s = sprite(self,g,"./art/enemies/skulking_colony.png",300)
        self.x-=30
        self.y-=40
        self.b.hardenedShell = 4 * len(self.g.players)
        self.intentions = [
            intent(self,"attack",[2,1]),
            intent(self,"debuff",["vulnerable",2]),
            intent(self,"attack",[3,1]),
        ]
        self.elite = True
    
    def draw(self):
        super().draw()
        self.s.draw()
        self.h.draw()

    def damage(self,dmg):
        blockAm = min(dmg,self.block)
        self.block -= blockAm

        dmg -= blockAm
        if dmg > 0:
            if self.b.damageTaken>=self.b.hardenedShell:
                return
            self.b.damageTaken += dmg
            if self.b.damageTaken>=self.b.hardenedShell:
                dmg -= max(0,self.b.damageTaken-self.b.hardenedShell)
        else:
            return
        
        self.hp -= dmg

        if self.hp <= 0:
            self.die()

#region slaver
class slaverA(enemy):
    def __init__(self,g):
        super().__init__(g)
        self.hp = 8 * len(self.g.players)
        self.hpMax = self.hp
        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)

        self.s = sprite(self,g,"./art/enemies/slaverA.png",200)
        self.intentions = [
            intent(self,"attack",[2,1]),
            intent(self,"debuff",["vulnerable",2]),
        ]
    
    def draw(self):
        super().draw()
        self.s.draw()
        self.h.draw()

class slaverB(enemy):
    def __init__(self,g):
        super().__init__(g)
        self.hp = 8 * len(self.g.players)
        self.hpMax = self.hp
        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)

        self.s = sprite(self,g,"./art/enemies/slaverB.png",200)
        self.intentions = [
            intent(self,"debuff",["frail",2]),
            intent(self,"attack",[2,1]),
        ]
    
    def draw(self):
        super().draw()
        self.s.draw()
        self.h.draw()

#region terror_eel
class terror_eel(enemy):
    def __init__(self,g):
        super().__init__(g)
        self.hp = 12 * len(self.g.players)
        self.hpMax = self.hp
        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)
        self.s = sprite(self,g,"./art/enemies/terror_eel.png",300)
        self.x-=30
        self.y-=40
        self.intentions = [
            intent(self,"attack",[1,3]),
            intent(self,"attack",[2,1]),
            intent(self,"debuff",["weak",3]),
            intent(self,"buff",["strength",1]),
        ]
        self.elite = True
        self.b.shriek = self.hpMax//2
    
    def draw(self):
        super().draw()
        self.s.draw()
        self.h.draw()

    def damage(self):
        super().damage()
        if self.hp > 0 and self.hp < self.b.shriek:
            self.intentions.insert(0,intent(
                self,"stun",[],False
            ))
            self.intentions.insert(0,intent(
                self,"debuff",["vulnerable",99],False
            ))

#region Thief
class thief(enemy):
    def __init__(self,g):
        super().__init__(g)
        self.hp = 8 * len(self.g.players)
        self.hpMax = self.hp
        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)

        self.s = sprite(self,g,"./art/enemies/thief.png",200)
        self.intentions = [
            intent(self,"attack",[2,1],False),
            intent(self,"attack",[2,1],False),
            intent(self,"attack",[2,1],False),
            intent(self,"defend",[3],False),
            intent(self,"escape",[],False),
            intent(self,"defend",[9999],False) #Just to flag somethings gone wrong - should never happen
        ]

    def act(self):
        if self.intentions[0].action=="attack":
            iHandler.queue.append(instruction(
                ["Thief steals 1 gold!"],120,self
            ))
        super().act()
    
    def draw(self):
        super().draw()
        self.s.draw()
        self.h.draw()

#region vine shambler
class vine_shambler(enemy):
    def __init__(self,g):
        super().__init__(g)
        self.hp = 9 * len(self.g.players)
        self.hpMax = self.hp
        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)

        self.s = sprite(self,g,"./art/enemies/vine_shambler.png",200)
        self.intentions = [
            intent(self,"drink",[2]),
            intent(self,"attack",[3,1]),
        ]
    
    def draw(self):
        super().draw()
        self.s.draw()
        self.h.draw()