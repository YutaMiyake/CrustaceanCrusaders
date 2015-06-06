import ogre.renderer.OGRE as ogre
from vector import MyVector

class Wake:
    def __init__(self, ent):
        self.ent = ent
        self.ent.pSystem = self.ent.engine.gfxMgr.sceneManager.createParticleSystem(self.ent.uiname + '_P', "myParticle/FireBall1")
        self.ent.aspects[1].node.attachObject(self.ent.pSystem)

    def tick(self, dtime):
        pass
        #self.emitter.setDirection(self.ent.vel.UNIT_SCALE)
        


