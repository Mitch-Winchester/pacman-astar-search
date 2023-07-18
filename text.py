import pygame
import vector
import constants

class Text(object):
    def __init__(self, text, color, x, y, size, time=None, id=None, visible=True):
        self.id = id
        self.text = text
        self.color = color
        self.size = size
        self.visible = visible
        self.position = vector.Vector2(x, y)
        self.timer = 0
        self.lifespan = time
        self.label = None
        self.destroy = False
        self.setupFont("PressStart2P-Regular.ttf")
        self.createLabel()

    def setupFont(self, fontpath):
        self.font = pygame.font.Font(fontpath, self.size)
    
    def createLabel(self):
        self.label = self.font.render(self.text, 1, self.color)
    
    def setText(self, newtext):
        self.text = str(newtext)
        self.createLabel()
    
    def update(self, dt):
        if self.lifespan is not None:
            self.timer += dt
            if self.timer >= self.lifespan:
                self.timer = 0
                self.lifespan = None
                self.destroy = True
    
    def render(self, screen):
        if self.visible:
            x, y = self.position.asTuple()
            screen.blit(self.label, (x, y))

class TextGroup(object):
    def __init__(self):
        self.nextid = 10
        self.alltext = {}
        self.setupText()
        self.showText(constants.READYTXT)
    
    def addText(self, text, color, x, y, size, time=None, id=None):
        self.nextid += 1
        self.alltext[self.nextid] = Text(text, color, x, y, size, time=time, id=id)
        return self.nextid

    def removeText(self, id):
        self.alltext.pop(id)

    def setupText(self):
        size = constants.TILEHEIGHT
        self.alltext[constants.SCORETXT] = Text("0".zfill(8), constants.WHITE, 0, constants.TILEHEIGHT, size)
        self.alltext[constants.LEVELTXT] = Text(str(1).zfill(3), constants.WHITE, 23*constants.TILEWIDTH, constants.TILEHEIGHT, size)
        self.alltext[constants.READYTXT] = Text("READY!", constants.YELLOW, 11.25*constants.TILEWIDTH, 20*constants.TILEHEIGHT, size, visible=False)
        self.alltext[constants.PAUSETXT] = Text("PAUSED!", constants.YELLOW, 10.625*constants.TILEWIDTH, 20*constants.TILEHEIGHT, size, visible=False)
        self.alltext[constants.GAMEOVERTXT] = Text("GAMEOVER!", constants.YELLOW, 10*constants.TILEWIDTH, 20*constants.TILEHEIGHT, size, visible=False)
        self.addText("SCORE", constants.WHITE, 0, 0, size)
        self.addText("LEVEL", constants.WHITE, 23*constants.TILEWIDTH, 0, size)
    
    def update(self, dt):
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].update(dt)
            if self.alltext[tkey].destroy:
                self.removeText(tkey)
    
    def showText(self, id):
        self.hideText()
        self.alltext[id].visible = True
    
    def hideText(self):
        self.alltext[constants.READYTXT].visible = False
        self.alltext[constants.PAUSETXT].visible = False
        self.alltext[constants.GAMEOVERTXT].visible = False
    
    def updateScore(self, score):
        self.updateText(constants.SCORETXT, str(score).zfill(8))
    
    def updateLevel(self, level):
        self.updateText(constants.LEVELTXT, str(level + 1).zfill(3))
    
    def updateText(self, id, value):
        if id in self.alltext.keys():
            self.alltext[id].setText(value)
    
    def render(self, screen):
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].render(screen)