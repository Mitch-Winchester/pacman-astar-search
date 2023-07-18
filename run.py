import pygame
from pygame import mixer
from pygame.locals import *
import constants
import pacman
import nodes
import pellets
import ghosts
from fruit import Fruit
import pause
import text
import sprites
from aStar import MazeWalls
from mazedata import MazeData
import simpleaudio as sa

eatPelletSound1 = sa.WaveObject.from_wave_file('soundEffects/munch_1.wav')
eatPelletSound2 = sa.WaveObject.from_wave_file('soundEffects/munch_2.wav')
eatFruitSound = sa.WaveObject.from_wave_file('soundEffects/eat_fruit.wav')
eatGhostSound = sa.WaveObject.from_wave_file('soundEffects/eat_ghost.wav')
deathSound1 = sa.WaveObject.from_wave_file('soundEffects/death_1.wav')

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(constants.SCREENSIZE, 0, 32)
        self.background = None
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.pause = pause.Pause(True)
        self.level = 0
        self.score = 0
        self.lives = 5
        self.textgroup = text.TextGroup()
        self.lifesprites = sprites.LifeSprites(self.lives)
        self.fruitCaptured = []
        self.mazedata = MazeData()
        
    
    def setBackground(self):
        self.background = pygame.surface.Surface(constants.SCREENSIZE).convert()
        self.background.fill(constants.BLACK)

    def startGame(self):
        self.mazedata.loadMaze(self.level)
        self.mazesprites = sprites.MazeSprites(self.mazedata.obj.name+".txt", self.mazedata.obj.name+"_rotation.txt")
        self.setBackground()
        #Creates boardWalls for aStarSearch from maze text file
        MazeWalls(self.mazedata.obj.name+".txt")
        self.background = self.mazesprites.constructBackground(self.background, self.level%5)
        self.nodes = nodes.NodeGroup(self.mazedata.obj.name+'.txt')
        self.mazedata.obj.setPortalPairs(self.nodes)
        self.mazedata.obj.connectHomeNodes(self.nodes)
        self.pacman = pacman.Pacman(self.nodes.getNodeFromTiles(*self.mazedata.obj.pacmanStart))
        self.pellets = pellets.PelletGroup(self.mazedata.obj.name+'.txt')
        self.ghosts = ghosts.GhostGroup(self.nodes.getStartTempNode(), self.pacman)
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 0)))
        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(0, 3)))
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(4, 3)))
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.ghosts)
        #prevent ghosts from moving left and right when in the middle of the home
        #helps prevent them from getting stuck in the home
        self.ghosts.inky.startNode.denyAccess(constants.RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(constants.LEFT, self.ghosts.clyde)
        self.mazedata.obj.denyGhostsAccess(self.ghosts, self.nodes)

    #Functions to control restart and level changes
    def restartGame(self):
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.startGame()
        self.score = 0
        self.textgroup.updateScore(self.score)
        self.textgroup.updateLevel(self.level)
        self.textgroup.showText(constants.READYTXT)
        self.lifesprites.resetLives(self.lives)
        
    def nextLevel(self):
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.startGame()
        self.textgroup.updateLevel(self.level)
    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None
        self.textgroup.showText(constants.READYTXT)

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.textgroup.update(dt)
        self.pellets.update(dt)
        if not self.pause.paused:
            self.ghosts.update(dt)
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkGhostEvents()
            self.checkFruitEvents()

        if self.pacman.alive:
            if not self.pause.paused:
                self.pacman.update(dt)
        else:
            self.pacman.update(dt)

        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()

    def updateScore(self, points):
        self.score += points
        self.textgroup.updateScore(self.score)

    #Functions for specific events
    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is constants.FRIGHT:
                    play = eatGhostSound.play()
                    self.pacman.visible = False
                    ghost.visible = False
                    self.updateScore(ghost.points)
                    self.textgroup.addText(str(ghost.points), constants.WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.ghosts.updatePoints()
                    self.pause.setPause(pauseTime=1, func=self.showEntities)
                    ghost.startSpawn()
                    self.nodes.allowHomeAccess(ghost)
                elif ghost.mode.current is not constants.SPAWN:
                    if self.pacman.alive:
                        mixer.music.stop()
                        deathSound1.play()
                        self.lives -= 1
                        self.lifesprites.removeImage()
                        self.pacman.die()
                        self.ghosts.hide()
                        if self.lives <= 0:
                            self.textgroup.showText(constants.GAMEOVERTXT)
                            self.pause.setPause(pauseTime=3, func=self.restartGame)
                        else:
                            self.pause.setPause(pauseTime=3, func=self.resetLevel)
    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.alive:
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            self.textgroup.hideText()
                            self.showEntities()
                        else:
                            self.textgroup.showText(constants.PAUSETXT)
                            self.hideEntities()
    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            play1 = eatPelletSound1.play()
            self.pellets.numEaten += 1
            self.updateScore(pellet.points)
            #play2 = eatPelletSound2.play()
            if self.pellets.numEaten == 30:
                self.ghosts.inky.startNode.allowAccess(constants.RIGHT, self.ghosts.inky)
            if self.pellets.numEaten == 70:
                self.ghosts.clyde.startNode.allowAccess(constants.LEFT, self.ghosts.clyde)
            self.pellets.pelletList.remove(pellet)
            if pellet.name == constants.POWERPELLET:
                self.ghosts.startFright()
            if self.pellets.isEmpty():
                mixer.music.stop()
                self.hideEntities()
                self.pause.setPause(pauseTime=3, func=self.nextLevel)
            
    def checkFruitEvents(self):
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20), self.level)
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                play = eatFruitSound.play()
                self.updateScore(self.fruit.points)
                self.textgroup.addText(str(self.fruit.points), constants.WHITE, self.fruit.position.x, self.fruit.position.y, 8, time=1)
                fruitCaptured = False
                for fruit in self.fruitCaptured:
                    if fruit.get_offset() == self.fruit.image.get_offset():
                        fruitCaptured = True
                        break
                if not fruitCaptured:
                    self.fruitCaptured.append(self.fruit.image)
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    #Functions to hide/show entities when pausing
    def showEntities(self):
        self.pacman.visible = True
        self.ghosts.show()
    def hideEntities(self):
        self.pacman.visible = False
        self.ghosts.hide()

    #Function to render images on screen
    def render(self):
        self.screen.blit(self.background, (0,0))
        #this line shows the nodes
        #self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.textgroup.render(self.screen)
        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = constants.SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))
        for i in range(len(self.fruitCaptured)):
            x = constants.SCREENWIDTH - self.fruitCaptured[i].get_width() * (i+1)
            y = constants.SCREENHEIGHT - self.fruitCaptured[i].get_height()
            self.screen.blit(self.fruitCaptured[i], (x, y))
        
        pygame.display.update()

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()