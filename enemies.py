from gameFile import sprite, healthbar, entity

class enemy(entity):
    def __init__(self,g):
        super().__init__()
        self.g = g
    
    def draw(self):
        pass

    def act(self):
        pass