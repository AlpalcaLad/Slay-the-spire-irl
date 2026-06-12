import random
from main import player

class context():
    def __init__(self):
        self.target = None
        self.source = None

c = context()

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
        if isinstance(c.source,player):
            pass #apply buffs
        c.target.damage(dmg)


class strike(card):
    def __init__(self):
        super().__init__()

    def play(self):
        pass