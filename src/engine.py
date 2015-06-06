# 381 main engine

class Engine(object):
    '''
    The root of the global manager tree
    '''

    def __init__(self):
        pass

    def init(self):
        import gfxMgr
        self.gfxMgr = gfxMgr.GfxMgr(self)
        self.gfxMgr.init()

        import entityMgr
        self.entityMgr = entityMgr.EntityMgr(self)
        self.entityMgr.init()

        import gameMgr
        self.gameMgr = gameMgr.GameMgr(self)
        self.gameMgr.init()

        import inputMgr
        self.inputMgr = inputMgr.InputMgr(self)
        self.inputMgr.init()

        import controlMgr
        self.controlMgr = controlMgr.ControlMgr(self)
        self.controlMgr.init()

        import sndMgr
        self.sndMgr = sndMgr.SndMgr(self)
        self.sndMgr.init()

        import collisionMgr
        self.collisionMgr = collisionMgr.CollisionMgr(self)
        self.collisionMgr.init()

        self.keepRunning = True


    def stop(self):
        self.gfxMgr.stop()
        self.inputMgr.stop()
        self.controlMgr.stop()
        self.sndMgr.stop()
        self.gameMgr.stop()
        self.entityMgr.stop()
        self.collisionMgr.stop()
        self.keepRunning = False

    def run(self):
        import time
        import ogre.renderer.OGRE as ogre
        weu = ogre.WindowEventUtilities() # Needed for linux/mac
        weu.messagePump()                 # Needed for linux/mac

        self.oldTime = time.time()        
        self.runTime = 0
        self.gfxMgr.menu.show()

        while (self.keepRunning):
            now = time.time() # Change to time.clock() for windows
            dtime = now - self.oldTime
            self.oldTime = now

            self.inputMgr.tick(dtime)
            self.controlMgr.tick(dtime)
            self.sndMgr.tick(dtime)
            self.collisionMgr.tick(dtime)
            self.gfxMgr.tick(dtime)
            self.entityMgr.tick(dtime)
            self.gameMgr.tick(dtime)
            
            
            self.runTime += dtime
        
            weu.messagePump()             # Needed for linux/mac
            time.sleep(0.001)
    
