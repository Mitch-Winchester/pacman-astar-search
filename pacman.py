import pygame
from pygame.locals import *
import constants
import entity
from sprites import PacmanSprites

class Pacman(entity.Entity):
    def __init__(self, node):
        entity.Entity.__init__(self, node)
        self.name = constants.PACMAN
        self.color = constants.YELLOW
        self.direction = constants.LEFT
        self.setBetweenNodes(constants.LEFT)
        self.alive = True
        self.sprites = PacmanSprites(self)
        self.setSpeed(105)

    def reset(self):
        entity.Entity.reset(self)
        self.direction = constants.LEFT
        self.setBetweenNodes(constants.LEFT)
        self.alive = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()
    
    def die(self):
        self.alive = False
        self.direction = constants.STOP

    def update(self, dt):
        self.sprites.update(dt)
        self.position += self.directions[self.direction]*self.speed*dt
        direction = self.getValidKey()
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[constants.PORTAL] is not None:
                self.node = self.node.neighbors[constants.PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = constants.STOP
            self.setPosition()
        else:
            if self.oppositeDirection(direction):
                self.reverseDirection()

    def validDirection(self, direction):
        if direction is not constants.STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False
    
    def getNewTarget(self, direction):
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node

    #read keys input by user
    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP] or key_pressed[K_w]:
            return constants.UP
        if key_pressed[K_DOWN] or key_pressed[K_s]:
            return constants.DOWN
        if key_pressed[K_LEFT] or key_pressed[K_a]:
            return constants.LEFT
        if key_pressed[K_RIGHT] or key_pressed[K_d]:
            return constants.RIGHT
        return constants.STOP
    
    #Checks to make sure Pacman hasn't overshot the target during movement
    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False
    
    #Allows the player to reverse Pacman's direction while moving
    def reverseDirection(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp
    def oppositeDirection(self, direction):
        if direction is not constants.STOP:
            if direction == self.direction * -1:
                return True
        return False
    
    #Functions to control eating of Ghosts and Pellets
    def eatPellets(self, pelletList):
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None
    def collideGhost(self, ghost):
        return self.collideCheck(ghost)
    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius)**2
        if dSquared <= rSquared:
            return True
        return False
    