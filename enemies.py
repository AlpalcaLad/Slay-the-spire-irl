from gameFile import sprite, healthbar, entity

def getenemy(enemyname):
    match enemyname:
        case "enemyrat":
            return enemyrat
        case "enemybird":
            return enemybird
        case _:
            return
        
class intent():
    def __init__(self,action,values):
        self.action = action
        self.values = values

    def damage(self):
        pass

    def act(self):
        match self.action:
            case "attack":
                return
            case "defend":
                return
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