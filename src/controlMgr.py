#Yuta Miyake
import utils
import math
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
from vector import MyVector
import random

class ControlMgr:
    def __init__(self, engine):
        self.engine = engine
        
        
    def init(self):
        self.keyboard = self.engine.inputMgr.keyboard
        self.toggle = 0.1
        self.toggle2 = 0.1

        self.rotate = 0.2
        self.timerTick = 0
        self.timerTick2 = 0

        self.chargeTime = 0
        self.chargeToggle = False
        self.chargeVal = .02
        self.maxCharge = 1.5

        self.chargeTime2 = 0
        self.chargeToggle2 = False
        self.chargeVal2 = .02
        self.maxCharge2 = 1.5

        self.spawn = 0

    def stop(self):
        pass
        
    def tick(self, dtime):
        if self.toggle >= 0:
             self.toggle -= dtime

        else:
            self.toggle = 0.1
            self.keyboard.capture()

            player = self.engine.entityMgr.player
            if player == None or not self.engine.gfxMgr.TPVOn:
                return

            # rest speed
            player.speed = 0

            if (not self.engine.gfxMgr.gameOver) or self.engine.gfxMgr.Victory:
            # Speed Up
                
                if self.keyboard.isKeyDown(OIS.KC_W):
                    player.speed = player.runSpeed
                    # print "( " + str(player.pos.x) + ", " + str(player.pos.y) + " , " + str(player.pos.z) + ")"
                    self.timerTick = self.timerTick+1
                    if(self.timerTick%3 == 0):
                        self.engine.sndMgr.playwalk()
                
                # Slow down
                if  self.keyboard.isKeyDown(OIS.KC_S):
                    player.speed = -player.runSpeed

                    self.timerTick = self.timerTick+1

                    if(self.timerTick%6 == 0):
                        self.engine.sndMgr.playwalk()
            
                if  self.keyboard.isKeyDown(OIS.KC_SPACE):
                    self.charge(dtime)

            if self.engine.gfxMgr.game2 == True:
                self.spawn += dtime
                if (self.spawn % 0.3 <= 0.01):
                    posx = random.randint(-2000,2000)
                    posz = random.randint(-2000,2000)
                    self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(5000,0,5000))
                    self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(2000,0,3000))
                    self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(300,0,-4600))
                    self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(300,0,4600))
                    self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(-5000,0,-5000))
                    self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(-2000,0,-3000))
                # print "YAY

        if self.toggle2 >= 0:
             self.toggle2 -= dtime
        else:
            self.toggle2 = 0.1
            self.keyboard.capture()

            if not self.engine.gfxMgr.gameOver:
                player2 = self.engine.entityMgr.player2
                if player2 == None:
                    return

                player2.speed = 0

                if self.engine.gfxMgr.game3:
                    if self.keyboard.isKeyDown(OIS.KC_UP):
                        player2.speed = player2.runSpeed

                        self.timerTick2 = self.timerTick2+1
                        if(self.timerTick2%3 == 0):
                            self.engine.sndMgr.playwalk()

                    if  self.keyboard.isKeyDown(OIS.KC_DOWN):
                        player2.speed = -player2.runSpeed

                        self.timerTick2 = self.timerTick2+1
                        if(self.timerTick2%6 == 0):
                            self.engine.sndMgr.playwalk()

                    if self.keyboard.isKeyDown(OIS.KC_RETURN):
                       self.charge2(dtime)


    def charge(self, dtime):
        if self.chargeVal < self.maxCharge:
            self.chargeVal += dtime*10
        self.chargeToggle = True

    def release(self):
        if self.chargeVal <.5:
            self.chargeVal = .04

        # produce bullet with scale relative to charge time
        self.shoot()
        self.chargeToggle = False
        self.chargeVal = 0.02

    def shoot(self):
        player = self.engine.entityMgr.player
        if player != None:
            if player.speed >= player.maxSpeed:
                deltaSpeed = 200
            elif player.speed > 0:
                deltaSpeed = 100
            else:
                deltaSpeed = 20
            direction = MyVector(-deltaSpeed*math.sin(player.heading),0, -deltaSpeed*math.cos(player.heading))
            pos = MyVector(player.pos.x + direction.x,player.pos.y+60,player.pos.z + direction.z)
            self.engine.entityMgr.playerNum = 1
            bullet = self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[3], pos = pos, heading = player.heading)
            bullet.pitch = player.pitch
            self.engine.sndMgr.playBullet()

    def charge2(self, dtime):
        if self.chargeVal2 < self.maxCharge2:
            self.chargeVal2 += dtime*10
        self.chargeToggle2 = True

    def release2(self):
        if self.chargeVal2 <.5:
            self.chargeVal2 = .04

        # produce bullet with scale relative to charge time
        self.shoot2()
        self.chargeToggle2 = False
        self.chargeVal2 = 0.02

    def shoot2(self):
        player = self.engine.entityMgr.player2
        if player != None:
            if player.speed >= player.maxSpeed:
                deltaSpeed = 200
            elif player.speed > 0:
                deltaSpeed = 100
            else:
                deltaSpeed = 20
            direction = MyVector(-deltaSpeed*math.sin(player.heading),0, -deltaSpeed*math.cos(player.heading))
            pos = MyVector(player.pos.x + direction.x,player.pos.y+60,player.pos.z + direction.z)
            self.engine.entityMgr.playerNum = 2
            bullet = self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[3], pos = pos, heading = player.heading)
            bullet.pitch = player.pitch
            self.engine.sndMgr.playBullet()