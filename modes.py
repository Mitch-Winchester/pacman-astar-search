from pygame import mixer
import constants



class MainMode(object):
    endFright = False
    def __init__(self):
        self.timer = 0
        self.scatter()
        
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.time:
            if self.mode is constants.SCATTER:
                self.chase()
            elif self.mode is constants.CHASE:
                self.scatter()
    
    def scatter(self):
        self.mode = constants.SCATTER
        self.time = 7
        self.timer = 0

    def chase(self):
        self.mode = constants.CHASE
        self.time = 20
        self.timer = 0

class ModeController(object):
    def __init__(self, entity):
        self.timer = 0
        self.time = None
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.entity = entity
    
    #If Ghosts are in Scatter/Chase Mode -> Activates Fright Mode
    #If already in Fright Mode -> Resets timer
    def setFrightMode(self):
        if self.current in [constants.SCATTER, constants.CHASE]:
            self.timer = 0
            self.time = 7
            mixer.music.load('soundEffects/power_pellet.wav')
            mixer.music.play(-1)
            self.current = constants.FRIGHT
        elif self.current is constants.FRIGHT:
            self.timer = 0

    def update(self, dt):
        self.mainmode.update(dt)
        if self.current is constants.FRIGHT:
            self.timer += dt
            if self.timer >= self.time:
                self.time = None
                mixer.music.stop()
                self.entity.normalMode()
                self.current = self.mainmode.mode
        elif self.current in [constants.SCATTER, constants.CHASE]:
            self.current = self.mainmode.mode
        
        if self.current is constants.SPAWN:
            if self.entity.node == self.entity.spawnNode:
                self.entity.normalMode()
                self.current = self.mainmode.mode
    
    def setSpawnMode(self):
        if self.current is constants.FRIGHT:
            self.current = constants.SPAWN