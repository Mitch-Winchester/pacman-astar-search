import pygame
from pygame.locals import *
from random import randint
import constants
from vector import Vector2
import aStar

class Entity(object):
    def __init__(self, node):
        self.name = None
        self.directions = {constants.UP:Vector2(0,-1),
                           constants.DOWN:Vector2(0,1),
                           constants.LEFT:Vector2(-1,0),
                           constants.RIGHT:Vector2(1,0),
                           constants.STOP:Vector2()}
        self.direction = constants.STOP
        self.setSpeed(100)
        self.radius = 10
        self.collideRadius = 5
        self.color = constants.WHITE
        self.visible = True
        self.disablePortal = False
        self.goal = None
        self.directionMethod = self.randomDirection
        self.setStartNode(node)
        self.image = None
    
    def setStartNode(self, node):
        self.node = node
        self.startNode = node
        self.target = node
        self.setPosition()

    def setPosition(self):
        self.position = self.node.position.copy()
    
    def validDirection(self, direction):
        if direction is not constants.STOP:
            if self.name in self.node.access[direction]:
                if self.node.neighbors[direction] is not None:
                    return True
        return False

    def getNewTarget(self, direction):
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node
    
    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1. magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False
    
    def reverseDirection(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    def oppositeDirection(self, direction):
        if direction is not constants.STOP:
            if direction == self.direction * -1:
                return True
        return True
    
    def setSpeed(self, speed):
        self.speed = speed * constants.TILEWIDTH/22

    def setBetweenNodes(self, direction):
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) / 2.0
    
    def reset(self):
        self.setStartNode(self.startNode)
        self.direction = constants.STOP
        self.speed = 100
        self.visible = True

    def render(self, screen):
        if self.visible:
            if self.image is not None:
                adjust = Vector2(constants.TILEWIDTH, constants.TILEHEIGHT) / 2
                p = self.position - adjust
                screen.blit(self.image, p.asTuple())
            else:
                p = self.position.asInt()
                pygame.draw.circle(screen, self.color, p, self.radius)

    #SHOULD REWRITE THIS
    #CAN LIKELY MAKE THIS MORE EFFICIENT
    def update(self, dt):
        self.position += self.directions[self.direction]*self.speed*dt

        if self.overshotTarget():
            self.node = self.target
            directions = self.validDirections()
            direction = self.directionMethod(directions)
            if not self.disablePortal:
                if self.node.neighbors[constants.PORTAL] is not None:
                    self.node = self.node.neighbors[constants.PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)
            
            self.setPosition()

    def randomDirection(self, directions):
            return directions[randint(0, len(directions)-1)]

    #NON AI METHOD TO CALCULATE MOVEMENT OF GHOSTS
    #The following methods check the 4 possible nodes for valid options
    def validDirections(self):
        directions = []
        for key in [constants.UP, constants.DOWN, 
                    constants.LEFT, constants.RIGHT]:
            if self.validDirection(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions
    
    #LOOPS THROUGH POSSIBLE DIRECTIONS AND ADDS THAT TO ITS CURRENT
    #POSITION ALL 4 VALUES ARE ADDED TO AN ARRAY AND THE MIN IS PASSED ON
    def goalDirection(self, directions):
        distances = []
        for direction in directions:
            vec = self.node.position + self.directions[direction]*constants.TILEWIDTH - self.goal
            distances.append(vec.magnitudeSquared())
        index = distances.index(min(distances))
        return directions[index]
    
    #method to call aStar
    def aStarGoal(self, directions):
        path: list[aStar.Location] = []
        start = self.position.asTuple()
        goal = self.pacman.position.asTuple()
        came_from = aStar.a_star_search(aStar.board, start, goal)
        path = aStar.reconstruct_path(came_from, start=start, goal=goal)
        if path:
            if len(path) > 1:
                index = 1
            else:
                index = 0
            return path[index]
        else:
            self.goalDirection
        