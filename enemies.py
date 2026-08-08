from gameFile import sprite, healthbar, entity
import math

def getenemy(enemyname):
    match enemyname:
        case "enemyrat":
            return enemyrat
        case "enemybird":
            return enemybird
        case _:
            return
        
class intent():
    def __init__(self,p,action: str, values: list[int]):
        self.action = action
        self.values = values
        self.p = p
        self.g = p.g

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

            for t in times:
                player.damage(dmg)

    def defend(self, am: int):
        blk = am
        
        if self.p.b.frail > 0:
            blk = blk // 2
            self.p.b.frail -= 1

        self.p.block += blk

    def act(self):
        match self.action:
            case "attack":
                self.damage(self.values[0],self.values[1])
            case "defend":
                self.defend(self.values[0])
            case "attack_defend":
                self.damage(self.values[0],self.values[1])
                self.defend(self.values[2])
            case _:
                return

class enemy(entity):
    def __init__(self,g):
        super().__init__()
        self.g = g
        self.intentions: list[intent] = []
    
    def draw(self):
        pass

    def act(self):
        self.b.startturn()
        if len(self.intentions) > 0:
            cur = self.intentions.pop(0)
            cur.act()
            self.intentions.append(cur)

class enemyrat(enemy):
    def __init__(self,g):
        super().__init__(g)
        self.hp = 10
        self.hpMax = self.hp
        self.y = self.g.H-600
        self.h = healthbar(self,self.g,self.x,self.y+200,125,20)
        self.s = sprite(self,g,"./art/enemyRatArt.png")
    
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
        self.s = sprite(self,g,"./art/enemyBirdArt.png")
    
    def draw(self):
        self.s.draw()
        self.h.draw()