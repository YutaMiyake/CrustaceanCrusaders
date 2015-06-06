import math
import utils
import ogre.renderer.OGRE as ogre
from vector import MyVector
 
class Physics:
     
    '''Initilize physics ent'''
    def __init__(self, ent):
        self.ent = ent
        self.raySceneQuery = self.ent.engine.gfxMgr.sceneManager.createRayQuery(ogre.Ray())
        self.raySceneQuery.setSortByDistance(True, 1)
         
         
    '''dtime is the change in time since the las call '''   
    def tick(self, dtime):

	if (self.ent.mesh == "sphere.mesh"):
            self.ent.vel.z = -math.cos(self.ent.heading)*self.ent.speed
            self.ent.vel.x = -math.sin(self.ent.heading)*self.ent.speed
            if self.ent.pitch != 0:
                self.ent.vel.y = self.ent.speed*math.tan(-self.ent.pitch)
            else:
                self.ent.vel.y = 0
             
            self.ent.pos = self.ent.pos + (self.ent.vel * dtime)
            squaredDistance = (self.ent.pos - self.ent.initialPos).squaredLength()
            if  squaredDistance > self.ent.distance**2:
                self.ent.isGone = True

            if self.ent.pos.y <= 0:
                self.ent.isGone = True
 
        elif self.ent.mesh == "ninja.mesh":
            #------------position--------------------------------
            self.ent.vel.z = -math.cos(self.ent.heading) * self.ent.speed
            self.ent.vel.x = -math.sin(self.ent.heading) * self.ent.speed
            self.ent.vel.y = 0
            self.ent.pos = self.ent.pos + (self.ent.vel * dtime)
            self.ent.heading = utils.fixAngle(self.ent.heading)

            if self.ent.speed != 0:
                self.ent.move = True
            else:
                self.ent.move = False
                self.ent.speed = 0

        elif (self.ent.mesh == "robot.mesh"):
 
            self.ent.move = False
            self.ent.speed = 0
            self.ent.lockOn = False

            if not self.ent.engine.gfxMgr.game3:
                self.game1(dtime)
            else:
                self.game1(dtime)
                self.game3(dtime)

            if self.ent.lockOn:
                self.ent.pos = self.ent.pos + self.ent.vel*dtime

            # update heading 
            if abs(self.ent.desiredHeading - self.ent.heading) >= 0.01:
                self.ent.heading = utils.fixAngle(self.ent.heading)
                timeScaledRotation = self.ent.turningRate * dtime
                angleDiff = utils.diffAngle(self.ent.desiredHeading, self.ent.heading)
                dheading = utils.clamp(angleDiff, -timeScaledRotation, timeScaledRotation)
                self.ent.heading += dheading
            else:
                self.ent.causion = False	


        elif self.ent.mesh == "shield.mesh":
            #-------------------------Bobbing-------------#
            if self.ent.pos.y < self.ent.bobMax and self.ent.bobReset == False:
                self.ent.pos.y += dtime*12
            elif self.ent.bobReset == True:
                self.ent.pos.y -= dtime*12

            if self.ent.pos.y >= self.ent.bobMax:
                self.ent.bobReset = True
            elif self.ent.pos.y <= self.ent.bobMin:
                self.ent.bobReset = False

            self.ent.heading += dtime

 

    def game1(self, dtime):
        diff = self.ent.engine.entityMgr.player.pos -self.ent.pos
        squaredDistance = diff.squaredLength()

        # player detection 
        if (squaredDistance <= self.ent.sightDistance**2 or self.ent.causion == True):
            if(squaredDistance >= self.ent.proximity**2):
                if self.ent.engine.gfxMgr.game2 == True:
                    self.ent.move = True
                    self.ent.speed = self.ent.maxSpeed
                    self.ent.desiredHeading = math.atan2(-diff.z,(diff.x+0.000001))
                    self.ent.lockOn = True

                else:
                    # enemy's line of sight
                    deg = -math.pi/4-math.pi/8
                    end = False
                    while(not self.ent.lockOn and not end):
                        newHeading = self.ent.heading + deg
                        direction = MyVector(math.cos(newHeading),0, -math.sin(newHeading))
                        self.raySceneQuery.setRay(ogre.Ray(self.ent.pos+direction,direction))
                        result = self.raySceneQuery.execute()
                    
                        if len(result) > 0:
                            # print result[len(result)-1].movable.getName()
                            if result[len(result)-1].movable.getName()[:7] == "Player0":
                                self.ent.move = True
                                end = True
                                self.ent.speed = self.ent.maxSpeed

                                self.ent.desiredHeading = math.atan2(-diff.z,(diff.x+0.000001))
                                self.ent.lockOn = True

                        deg += math.pi/8
                        if deg > math.pi/4+math.pi/8:
                            end = True

                self.ent.vel.z = -math.sin(self.ent.desiredHeading)*self.ent.speed
                self.ent.vel.x = math.cos(self.ent.desiredHeading)*self.ent.speed
        
            # damage
            elif(squaredDistance < self.ent.proximity**2):
                self.ent.engine.entityMgr.player.damage = True
                self.ent.pos -= self.ent.vel*dtime
        
        else:
            self.ent.move = False
            self.ent.speed = 0

    def game3(self, dtime):
        diff2 = self.ent.engine.entityMgr.player2.pos - self.ent.pos
        squaredDistance2 = diff2.squaredLength()

        # player detection 
        if (squaredDistance2 <= self.ent.sightDistance**2 or self.ent.causion == True):
            if(squaredDistance2 >= self.ent.proximity**2):
                
                if self.ent.engine.gfxMgr.game2 == True:
                    diff1 = self.ent.engine.entityMgr.player.pos -self.ent.pos
                    squaredDistance1 = diff1.squaredLength()
                    if squaredDistance2 < squaredDistance1: 
                        self.ent.desiredHeading = math.atan2(-diff2.z,(diff2.x+0.000001))

                else:
                    deg = -math.pi/4-math.pi/8
                    end = False

                    if self.ent.lockOn: # if it already finds the player1
                        lockOn2 = False
                        while(not lockOn2 and not end):
                            newHeading = self.ent.heading + deg
                            direction = MyVector(math.cos(newHeading),0, -math.sin(newHeading))
                            self.raySceneQuery.setRay(ogre.Ray(self.ent.pos+direction,direction))
                            result = self.raySceneQuery.execute()
                        
                            if len(result) > 0:
                                # print result[len(result)-1].movable.getName()
                                if result[len(result)-1].movable.getName()[:7] == "Player1":
                                    end = True

                                    diff1 = self.ent.engine.entityMgr.player.pos -self.ent.pos
                                    squaredDistance1 = diff1.squaredLength()

                                    if squaredDistance2 < squaredDistance1: 
                                        self.ent.desiredHeading = math.atan2(-diff2.z,(diff2.x+0.000001))

                            deg += math.pi/8
                            if deg > math.pi/4+math.pi/8:
                                end = True

                    else:
                        while(not self.ent.lockOn and not end):
                            newHeading = self.ent.heading + deg
                            direction = MyVector(math.cos(newHeading),0, -math.sin(newHeading))
                            self.raySceneQuery.setRay(ogre.Ray(self.ent.pos+direction,direction))
                            result = self.raySceneQuery.execute()
                        
                            if len(result) > 0:
                                # print result[len(result)-1].movable.getName()
                                if result[len(result)-1].movable.getName()[:7] == "Player1":
                                    self.ent.move = True
                                    end = True
                                    self.ent.lockOn = True
                                    self.ent.speed = self.ent.maxSpeed

                                    self.ent.desiredHeading = math.atan2(-diff2.z,(diff2.x+0.000001))

                            deg += math.pi/8
                            if deg > math.pi/4+math.pi/8:
                                end = True

                self.ent.vel.z = -math.sin(self.ent.desiredHeading)*self.ent.speed
                self.ent.vel.x = math.cos(self.ent.desiredHeading)*self.ent.speed
        
            # damage
            elif(squaredDistance2 < self.ent.proximity**2):
                self.ent.engine.entityMgr.player2.damage = True
                self.ent.pos -= self.ent.vel*dtime
        
        else:
            self.ent.move = False
            self.ent.speed = 0
