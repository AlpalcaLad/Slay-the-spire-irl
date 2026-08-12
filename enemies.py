from gameFile import sprite, healthbar, entity
import math
from helperFuncs import *
from cards import *

def getenemy(enemyname):
    match enemyname:
        case "enemyrat":
            return enemyrat
        case "enemybird":
            return enemybird
        case "byrdonis":
            return byrdonis
        case "cultist":
            return cultist
        case "fossilstlk":
            return fossil_stalker
        case "frogknight":
            return frog_knight
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
            case "buff" | "debuff" | "sleep" | "mystery" | "stun" | "defend":
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
                p.b.drinkSafe -= self.sips
                if p.b.drinkSafe < 0:
                    p.b.drinkSafe = 0
                    iHandler.queue.append(instruction([
                        "take "+str(sips)+" sips!"
                    ],90,c.source,False))

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
                    case _:
                        pass
            case _:
                return
#region enemy
class enemy(entity):
    def __init__(self,g):
        super().__init__()
        self.g = g
        self.intentions: list[intent] = []
    
    def draw(self):
        if len(self.intentions)>0:
            self.intentions[0].draw()

    def act(self):
        self.b.startturn()
        if len(self.intentions) > 0:
            cur = self.intentions.pop(0)
            cur.act()
            if cur.repeat:
                self.intentions.append(cur)

class enemyrat(enemy):
    def __init__(self,g):
        super().__init__(g)
        self.hp = 10
        self.hpMax = self.hp
        self.y = self.g.H-600
        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)
        self.s = sprite(self,g,"./art/enemyRatArt.png",25)
    
    def draw(self):
        self.s.draw()
        self.h.draw()

class enemybird(enemy):
    def __init__(self,g):
        super().__init__(g)
        self.hp = 10
        self.hpMax = self.hp
        self.y = self.g.H-600
        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)
        self.s = sprite(self,g,"./art/enemyBirdArt.png",50)
    
    def draw(self):
        self.s.draw()
        self.h.draw()
#region byrdonis
class byrdonis(enemy):
    def __init__(self,g):
        super().__init__(g)
        self.hp = 12 * len(self.g.players)
        self.hpMax = self.hp
        self.y = self.g.H-600
        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)
        self.s = sprite(self,g,"./art/enemies/byrdonis.png",300)
        self.s.x=-30
        self.s.y=-40
        self.intentions = [
            intent(self,"attack",[2,1]),
            intent(self,"attack",[1,3]),
            intent(self,"buff",["strength",1])
        ]
    
    def draw(self):
        super().draw()
        self.s.draw()
        self.h.draw()

class cultist(enemy):
    def __init__(self,g):
        super().__init__(g)
        self.hp = 8  * len(self.g.players)
        self.hpMax = self.hp
        self.y = self.g.H-600
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
        self.hp = 9 * len(self.g.players)
        self.hpMax = self.hp
        self.y = self.g.H-600
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
        self.y = self.g.H-600
        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)
        self.s = sprite(self,g,"./art/enemies/frog_knight.png",200)
        self.b.plating = 5 * len(self.g.players)
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