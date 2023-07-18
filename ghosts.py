from pygame.locals import *
import vector
import constants
import entity
import modes
from sprites import GhostSprites
import simpleaudio as sa

retreatSound = sa.WaveObject.from_wave_file('soundEffects/retreating.wav')

class Ghost(entity.Entity):
    def __init__(self, node, pacman=None, blinky=None):
        entity.Entity.__init__(self, node)
        self.name = constants.GHOST
        self.points = 200
        self.goal = vector.Vector2(360,480)
        self.directionMethod = self.goalDirection
        self.pacman = pacman
        self.mode = modes.ModeController(self)
        self.blinky = blinky
        self.homeNode = node
        
    
    def update(self, dt):
        self.sprites.update(dt)
        self.mode.update(dt)
        if self.mode.current is constants.SCATTER:
            self.scatter()
        elif self.mode.current is constants.CHASE:
            self.chase()
        entity.Entity.update(self, dt)
    
    #Functions for the various modes
    def scatter(self):
        self.goal = vector.Vector2()
    def chase(self):
        self.goal = self.pacman.position
    def startFright(self):
        self.mode.setFrightMode()
        if self.mode.current == constants.FRIGHT:
            self.setSpeed(50)
            self.directionMethod = self.randomDirection
    def normalMode(self):
        self.setSpeed(100)
        self.directionMethod = self.goalDirection
        self.homeNode.denyAccess(constants.DOWN, self)

    #Functions to control spawning
    def spawn(self):
        self.goal = self.spawnNode.position
    def setSpawnNode(self, node):
        self.spawnNode = node
    def startSpawn(self):
        self.mode.setSpawnMode()
        if self.mode.current == constants.SPAWN:
            play = retreatSound.play()
            self.setSpeed(550)
            self.directionMethod = self.goalDirection
            self.spawn()
    
    def reset(self):
        entity.Entity.reset(self)
        self.points = 200
        self.directionMethod = self.goalDirection

#Classes to create the 4 Ghosts
class Blinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = constants.BLINKY
        self.color = constants.RED
        self.sprites = GhostSprites(self)
    #call aStarSearch
    def chaseMode(self):
        self.directionMethod = self.aStarGoal
    
class Pinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = constants.PINKY
        self.color = constants.PINK
        self.sprites = GhostSprites(self)
    def scatter(self):
        self.goal = vector.Vector2(constants.TILEWIDTH*constants.NCOLS, 0)
    def chase(self):
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * constants.TILEWIDTH * 4

class Inky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = constants.INKY
        self.color = constants.TEAL
        self.sprites = GhostSprites(self)
    def scatter(self):
        self.goal = vector.Vector2(constants.TILEWIDTH*constants.NCOLS, constants.TILEHEIGHT*constants.NROWS)
    def chase(self):
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction]*constants.TILEWIDTH*2
        vec2 = (vec1 - self.blinky.position)*2
        self.goal = self.blinky.position+vec2

class Clyde(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = constants.CLYDE
        self.color = constants.ORANGE
        self.sprites = GhostSprites(self)
    def __iter__(self):
        return iter(self.ghosts)
    def scatter(self):
        self.goal = vector.Vector2(0, constants.TILEWIDTH*constants.NROWS)
    def chase(self):
        d = self.pacman.position - self.position
        ds = d.magnitudeSquared()
        if ds <= (constants.TILEWIDTH*8)**2:
            self.scatter()
        else:
            self.goal = self.pacman.position+self.pacman.directions[self.pacman.direction]*constants.TILEWIDTH*4

#Group class to simplify working with each Ghost
class GhostGroup(object):
    def __init__(self, node, pacman):
        self.blinky = Blinky(node, pacman)
        self.pinky = Pinky(node, pacman)
        self.inky = Inky(node, pacman, self.blinky)
        self.clyde = Clyde(node, pacman)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]
    def __iter__(self):
        return iter(self.ghosts)
    def update(self, dt):
        for ghost in self.ghosts:
            ghost.update(dt)
    def startFright(self):
        for ghost in self.ghosts:
            ghost.startFright()
        self.resetPoints()
    def setSpawnNode(self, node):
        for ghost in self.ghosts:
            ghost.setSpawnNode(node)
    def updatePoints(self):
        for ghost in self.ghosts:
            ghost.points *= 2
    def resetPoints(self):
        for ghost in self.ghosts:
            ghost.points = 200
    def reset(self):
        for ghost in self.ghosts:
            ghost.reset()
    def hide(self):
        for ghost in self.ghosts:
            ghost.visible = False
    def show(self):
        for ghost in self.ghosts:
            ghost.visible = True
    def render(self, screen):
        for ghost in self.ghosts:
            ghost.render(screen)
