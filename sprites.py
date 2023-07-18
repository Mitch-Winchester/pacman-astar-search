import pygame
import constants
import numpy as np
from animation import Animator
from modes import MainMode

BASETILEWIDTH = 16
BASETILEHEIGHT = 16
DEATH = 5

class Spritesheet(object):
    def __init__(self):
        self.sheet = pygame.image.load("spritesheet.png").convert()
        transcolor = self.sheet.get_at((0,0))
        self.sheet.set_colorkey(transcolor)
        width = int(self.sheet.get_width() / BASETILEWIDTH * constants.TILEWIDTH)
        height = int(self.sheet.get_height() / BASETILEHEIGHT * constants.TILEHEIGHT)
        self.sheet = pygame.transform.scale(self.sheet, (width, height))

    def getImage(self, x, y, width, height):
        x *= constants.TILEWIDTH
        y *= constants.TILEHEIGHT
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())
        
#'''Uncomment for sharks
class SharkSpritesheet(object):
    def __init__(self):
        self.sheet = pygame.image.load("sharks.png").convert()
        transcolor = self.sheet.get_at((0,0))
        self.sheet.set_colorkey(transcolor)
        width = int(self.sheet.get_width() / BASETILEWIDTH * constants.TILEWIDTH)
        height = int(self.sheet.get_height() / BASETILEHEIGHT * constants.TILEHEIGHT)
        self.sheet = pygame.transform.scale(self.sheet, (width, height))

    def getImage(self, x, y, width, height):
        x *= constants.TILEWIDTH
        y *= constants.TILEHEIGHT
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())
#'''    
class PacmanSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.entity = entity
        self.entity.image = self.getStartImage()
        self.animations = {}
        self.defineAnimations()
        self.stopimage = (8, 0)
    
    def defineAnimations(self):
        self.animations[constants.LEFT] = Animator(((8,0), (0, 0), (0, 2), (0, 0)))
        self.animations[constants.RIGHT] = Animator(((10,0), (2, 0), (2, 2), (2, 0)))
        self.animations[constants.UP] = Animator(((10,2), (6, 0), (6, 2), (6, 0)))
        self.animations[constants.DOWN] = Animator(((8,2), (4, 0), (4, 2), (4, 0)))
        self.animations[DEATH] = Animator(((0, 12), (2, 12), (4, 12), (6, 12), (8, 12), (10, 12), (12, 12), (14, 12), (16, 12), (18, 12), (20, 12)), speed=6, loop=False)

    def update(self, dt):
        if self.entity.alive == True:
            if self.entity.direction == constants.LEFT:
                self.entity.image = self.getImage(*self.animations[constants.LEFT].update(dt))
                self.stopimage = (8, 0)
            elif self.entity.direction == constants.RIGHT:
                self.entity.image = self.getImage(*self.animations[constants.RIGHT].update(dt))
                self.stopimage = (10, 0)
            elif self.entity.direction == constants.DOWN:
                self.entity.image = self.getImage(*self.animations[constants.DOWN].update(dt))
                self.stopimage = (8, 2)
            elif self.entity.direction == constants.UP:
                self.entity.image = self.getImage(*self.animations[constants.UP].update(dt))
                self.stopimage = (10, 2)
            elif self.entity.direction == constants.STOP:
                self.entity.image = self.getImage(*self.stopimage)
        else:
            self.entity.image = self.getImage(*self.animations[DEATH].update(dt))

    def reset(self):
        for key in list(self.animations.keys()):
            self.animations[key].reset()

    def getStartImage(self):
        return self.getImage(8, 0)
    
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*constants.TILEWIDTH, 2*constants.TILEHEIGHT)

class GhostSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.x = {constants.BLINKY:0, constants.PINKY:2, constants.INKY:4, constants.CLYDE:6}
        self.entity = entity
        self.entity.image = self.getStartImage()
        self.animations = {}
        self.defineAnimations()

    def defineAnimations(self):
        self.animations[constants.FRIGHT] = Animator((10, 4), (10, 6))

    def update(self, dt):
        x = self.x[self.entity.name]
        if self.entity.mode.current in [constants.SCATTER, constants.CHASE]:
            if self.entity.direction == constants.LEFT:
                self.entity.image = self.getImage(x, 8)
            elif self.entity.direction == constants.RIGHT:
                self.entity.image = self.getImage(x, 10)
            elif self.entity.direction == constants.DOWN:
                self.entity.image = self.getImage(x, 6)
            elif self.entity.direction == constants.UP:
                self.entity.image = self.getImage(x, 4)
        elif self.entity.mode.current == constants.FRIGHT:
           self.entity.image = self.getImage(10, 4)
        elif self.entity.mode.current == constants.SPAWN:
            if self.entity.direction == constants.LEFT:
                self.entity.image = self.getImage(8, 8)
            elif self.entity.direction == constants.RIGHT:
                self.entity.image = self.getImage(8, 10)
            elif self.entity.direction == constants.DOWN:
                self.entity.image = self.getImage(8, 6)
            elif self.entity.direction == constants.UP:
                self.entity.image = self.getImage(8, 4)
               
    def getStartImage(self):
        return self.getImage(self.x[self.entity.name], 4)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*constants.TILEWIDTH, 2*constants.TILEHEIGHT)

'''Class to replace Ghosts with sharks
class SharkSprites(SharkSpritesheet):
    def __init__(self, entity):
        SharkSpritesheet.__init__(self)
        self.x = {constants.BLINKY:0, constants.PINKY:2, constants.INKY:4, constants.CLYDE:6}
        self.entity = entity
        self.entity.image = self.getStartImage()
        self.animations = {}
        self.defineAnimations()
    
    def defineAnimations(self):
        self.animations[constants.LEFT] = animation.Animator(((0,2), (2, 2), (4, 2), (6, 2)))
        self.animations[constants.RIGHT] = animation.Animator(((0,4), (2, 4), (4, 4), (6, 4)))
        self.animations[constants.DOWN] = animation.Animator(((0,0), (2, 0), (4, 0), (6, 0)))
        self.animations[constants.UP] = animation.Animator(((0,6), (2, 6), (4, 6), (6, 6)))

    def update(self, dt):
        if self.entity.direction == constants.LEFT:
            self.entity.image = self.getImage(*self.animations[constants.LEFT].update(dt))
            #self.stopimage = (8, 0)
        elif self.entity.direction == constants.RIGHT:
            self.entity.image = self.getImage(*self.animations[constants.RIGHT].update(dt))
            #self.stopimage = (10, 0)
        elif self.entity.direction == constants.DOWN:
            self.entity.image = self.getImage(*self.animations[constants.DOWN].update(dt))
            #self.stopimage = (8, 2)
        elif self.entity.direction == constants.UP:
            self.entity.image = self.getImage(*self.animations[constants.UP].update(dt))
            #self.stopimage = (10, 2)

    def getStartImage(self):
        return self.getImage(self.x[self.entity.name], 4)
    
    def getImage(self, x, y):
        return SharkSpritesheet.getImage(self, x, y, 2*constants.TILEWIDTH, 2*constants.TILEHEIGHT)
'''

class FruitSprites(Spritesheet):
    def __init__(self, entity, level):
        Spritesheet.__init__(self)
        self.entity = entity
        self.fruits = {0:(16,8), 1:(18,8), 2:(20,8), 3:(16,10), 4:(18,10), 5:(20,10)}
        self.entity.image = self.getStartImage(level % len(self.fruits))

    def getStartImage(self, key):
        return self.getImage(*self.fruits[key])

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*constants.TILEWIDTH, 2*constants.TILEHEIGHT)

class LifeSprites(Spritesheet):
    def __init__(self, numlives):
        Spritesheet.__init__(self)
        self.resetLives(numlives)

    def removeImage(self):
        if len(self.images) > 0:
            self.images.pop(0)

    def resetLives(self, numlives):
        self.images = []
        for i in range(numlives):
            self.images.append(self.getImage(0,0))
    
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*constants.TILEWIDTH, 2*constants.TILEHEIGHT)

class MazeSprites(Spritesheet):
    def __init__(self, mazefile, rotfile):
        Spritesheet.__init__(self)
        self.data = self.readMazeFile(mazefile)
        self.rotdata = self.readMazeFile(rotfile)
    
    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, constants.TILEWIDTH, constants.TILEHEIGHT)
    
    def readMazeFile(self, mazefile):
        return np.loadtxt(mazefile, dtype='<U1')
    
    def constructBackground(self, background, y):
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                if self.data[row][col].isdigit():
                    x = int(self.data[row][col]) + 12
                    sprite = self.getImage(x, y)
                    rotval = int(self.rotdata[row][col])
                    sprite = self.rotate(sprite, rotval)
                    transcolor = self.sheet.get_at((0,0))
                    sprite.set_colorkey(transcolor)
                    background.blit(sprite, (col*constants.TILEWIDTH, row*constants.TILEHEIGHT))
                elif self.data[row][col] == '=':
                    sprite = self.getImage(10, 8)
                    background.blit(sprite, (col*constants.TILEWIDTH, row*constants.TILEHEIGHT))
        return background
    
    def rotate(self, sprite, value):
        return pygame.transform.rotate(sprite, value*90)
