#Yuta Miyake
import ogre.renderer.OGRE as ogre
import math
from vector import MyVector 

class Renderable:
    def __init__(self, ent):
        self.ent = ent
        self.timer = 0
        self.animationStates = []
        self.animationSpeeds = []

        if self.ent.mesh == "ninja.mesh":
            self.ogreEnt =  self.ent.engine.gfxMgr.sceneManager.createEntity('Player'+str(self.ent.eid), self.ent.mesh)
            self.node =  self.ent.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode('Player_node'+str(self.ent.eid), self.ent.pos)
            self.node.attachObject(self.ogreEnt)
            self.node.yaw(ogre.Degree(ent.yaw))
            self.node.setScale(.5,.5,.5)
            if self.ent.uiname == 'Player1':
                self.ogreEnt.setMaterialName("blueninja")

            if not self.ent.engine.gfxMgr.game3:
                self.ogreEnt.setVisible(False)
            else:
                self.animationStates.append(self.ogreEnt.getAnimationState('Walk'))
                self.animationStates[-1].Enabled = True

            self.damageTimer = 0

        elif self.ent.mesh == 'shield.mesh':
            self.ogreEnt = self.ent.engine.gfxMgr.sceneManager.createEntity(self.ent.uiname+ '_ent', self.ent.mesh)
            self.node =  self.ent.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(self.ent.uiname+ '_node', self.ent.pos)
            self.node.attachObject(self.ogreEnt)
            self.node.yaw(self.ent.heading)
            x,y,z = self.ent.scale
            self.node.setScale(x,y,z) 
            #self.ogreEnt.setMaterialName("lobster")

        elif self.ent.uiname == "shield":
            self.ogreEnt =  self.ent.engine.gfxMgr.sceneManager.createEntity(self.ent.uiname+ '_ent', self.ent.mesh)
            self.node =  self.ent.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(self.ent.uiname+ '_node', self.ent.pos)
            self.node.attachObject(self.ogreEnt)
            self.node.yaw(self.ent.heading)
            x,y,z = self.ent.scale
            self.node.setScale(x,y,z) 
            self.ogreEnt.setMaterialName("shieldwall")

        elif self.ent.mesh == "cube.mesh":
            self.ogreEnt =  self.ent.engine.gfxMgr.sceneManager.createEntity(self.ent.uiname+ '_ent', self.ent.mesh)
            self.node =  self.ent.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(self.ent.uiname+ '_node', self.ent.pos)
            self.node.attachObject(self.ogreEnt)
            self.node.yaw(self.ent.heading)
            x,y,z = self.ent.scale
            self.node.setScale(x,y,z) 
            self.ogreEnt.setMaterialName("honeycomb")


        elif self.ent.mesh == "robot.mesh":
            self.ogreEnt =  self.ent.engine.gfxMgr.sceneManager.createEntity(self.ent.uiname+ '_enemEnt', self.ent.mesh)
            self.node =  self.ent.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(self.ent.uiname+ '_enemNode', self.ent.pos)
            self.node.attachObject(self.ogreEnt)
            self.node.yaw(ogre.Degree(ent.yaw))
            self.node.scale(1.3,1.3,1.3)
            self.ogreEnt.setQueryFlags(0)

            self.animationStates.append(self.ogreEnt.getAnimationState('Walk'))
            self.animationStates2 = []
            self.animationStates2.append(self.ogreEnt.getAnimationState('Idle'))
            self.animationStates[-1].Enabled = True
            self.animationStates2[-1].Enabled = True

        elif self.ent.mesh == "sphere.mesh":
            self.ogreEnt =  self.ent.engine.gfxMgr.sceneManager.createEntity(self.ent.uiname+'_ent', self.ent.mesh)
            self.node =  self.ent.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(self.ent.uiname+'_node', self.ent.pos)
            self.node.attachObject(self.ogreEnt)
            x,y,z = self.ent.scale
            self.node.setScale(x,y,z)
            self.ogreEnt.setVisible(True)
            self.ogreEnt.setQueryFlags(0)

        elif self.ent.mesh == "astatusMesh.mesh":
            self.ogreEnt =  self.ent.engine.gfxMgr.sceneManager.createEntity(self.ent.uiname+'_ent', self.ent.mesh)
            self.node =  self.ent.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(self.ent.uiname+'_node', self.ent.pos)
            self.node.attachObject(self.ogreEnt)
            self.node.setScale(2000,2000,2000)
            self.ogreEnt.setMaterialName("lobster")
            #self.ogreEnt.setVisible(False)
            
        elif self.ent.mesh == "alienship.mesh":
            self.ogreEnt =  self.ent.engine.gfxMgr.sceneManager.createEntity(self.ent.uiname+'_ent', self.ent.mesh)
            self.node =  self.ent.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(self.ent.uiname+'_node', self.ent.pos)
            self.node.attachObject(self.ogreEnt)
            self.node.setScale(75,75,75)
            self.ogreEnt.setMaterialName("alienship")
            #self.ogreEnt.setVisible(False)

        else:
            self.ogreEnt =  self.ent.engine.gfxMgr.sceneManager.createEntity(self.ent.uiname+'_ent', self.ent.mesh)
            self.node =  self.ent.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(self.ent.uiname+'_node', self.ent.pos)
            self.node.attachObject(self.ogreEnt)
            self.node.yaw(ogre.Degree(ent.yaw))

        # bounding box
        self.bBox = self.ogreEnt.getWorldBoundingBox(True) # needs True
        self.node.showBoundingBox(False)

    def updateBBox(self):
        self.bBox = self.ogreEnt.getWorldBoundingBox(True)

    def tick(self, dtime):
        """update the position of the entity"""
        self.node.resetOrientation()
        self.node.position = self.ent.pos
        self.node.yaw(ogre.Radian(self.ent.heading))

        # shield
        if self.ent.uiname == "shield":
            if self.ent.shieldsOn == False:
                self.ogreEnt.setVisible(False)

        # player
        elif self.ent.mesh == "ninja.mesh":

            if self.ent.damage:
                if self.ent.timer > 0:
                    self.ent.timer -= dtime
                    self.damageTimer+= dtime
                    if self.damageTimer % 0.20 <= 0.1:
                        if self.ogreEnt.isVisible():
                            self.ogreEnt.setVisible(False)
                        else:
                            self.ogreEnt.setVisible(True)
                else:
                    self.damageTimer = 0
                    self.ent.damage = False
                    self.ent.timer = 0
                    self.ogreEnt.setVisible(True)

            if self.ent.move:
                self.timer = self.timer+dtime
                for index in xrange(0,len(self.animationStates)):
                    if self.ent.speed == self.ent.maxSpeed:
                        self.animationStates[index].addTime((self.timer/15)%3)
                    else:
                        self.animationStates[index].addTime((self.timer/30)%3)
                    if self.timer > 3:
                        self.timer = 3

        # bullet
        elif self.ent.mesh == "sphere.mesh" and self.ent.isGone:
            #self.node.setVisible(False)
            self.node.detachAllObjects()


        # robot
        elif self.ent.mesh == "robot.mesh":
            if self.ent.death:
                self.node.detachAllObjects()

            if self.ent.hit:
                if self.ent.timer > 0:
                    self.ent.timer -= dtime
                else:
                    self.ogreEnt.setMaterialName("Examples/Robot")
                    self.ent.hit = False
                    self.ent.timer = 0

            # animation
            if self.ent.move:
                self.timer = self.timer+dtime
                #print "TIMER = " + str(self.timer)
                for index in xrange(0,len(self.animationStates)):
                    self.animationStates[index].addTime((self.timer/100)%3)
                    if self.timer > 3:
                        self.timer = 3
            else:
                self.timer = self.timer+dtime
                for index in xrange(0,len(self.animationStates2)):
                    self.animationStates2[index].addTime((self.timer/200)%3)
                    if self.timer > 3:
                        self.timer = 3

        #pick up
        elif self.ent.mesh == 'shield.mesh':
            #stuff
            if self.ent.death:
                self.ogreEnt.setVisible(False)
                self.node.detachAllObjects()


