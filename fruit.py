import entity
import constants
from sprites import FruitSprites

class Fruit(entity.Entity):
    def __init__(self, node, level=0):
        entity.Entity.__init__(self, node)
        self.name = constants.FRUIT
        self.color = constants.GREEN
        self.lifespan = 10
        self.timer = 0
        self.destroy = False
        self.points = 100 + level*20
        self.setBetweenNodes(constants.RIGHT)
        self.sprites = FruitSprites(self, level)

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True