#Yuta Miyake
from vector import MyVector
import ent

class EntityMgr:
    def __init__(self, engine):
        self.engine = engine
  
    def init(self):
        self.ents = []
        self.nEnts = 0

        self.shields = []
        self.nShields = 0

        self.bullets = []
        self.nBullets = 0

        self.bullets2 = []
        self.nBullets2 = 0

        self.enems = []
        self.nEnems = 0

        self.pickups = []
        self.nPickups = 0

        self.entTypes = [ent.robot, ent.player, ent.cubeWall, ent.orb, ent.lobster, ent.shieldWall, ent.ship, ent.pickupItem]
        
        self.player = None
        self.player2 = None
        self.nplayers = 0
        self.playerNum = 0
        
    def createEnt(self, entType, pos = MyVector(0,0,0), yaw = 0, heading = 0, scale = (1,1,1)):
        
        # player
        if entType == self.entTypes[1]:
            
            if self.nplayers == 0:
                self.player = entType(self.engine, self.nplayers, pos = pos, yaw = yaw, heading = heading)
                self.player.init()
            else:
                self.player2 = entType(self.engine, self.nplayers, pos = pos, yaw = yaw, heading = heading)
                self.player2.init()

            self.nplayers = self.nplayers + 1

        # bullet
        elif entType == self.entTypes[3]:
            if scale == (1,1,1):
                scale = (.02,.02,.02)

            if self.playerNum == 1:
                bullet = entType(self.engine, self.nBullets, pos = pos, yaw = yaw, heading = heading, scale = scale)
                bullet.init()
                self.bullets.append(bullet)
            elif self.playerNum == 2:
                bullet = entType(self.engine, self.nBullets, pos = pos, yaw = yaw, heading = heading, scale = scale)
                bullet.init()
                self.bullets2.append(bullet)
            
            self.nBullets = self.nBullets + 1
            return bullet

        # cube wall
        elif entType == self.entTypes[2]:
            ent = entType(self.engine, self.nEnts, pos = pos, yaw = yaw, heading = heading, scale = scale)
            ent.init()
            self.ents.append(ent);
            self.nEnts = self.nEnts + 1
            return ent

        # lobster
        elif entType == self.entTypes[4]:
            ent = entType(self.engine, self.nEnts, pos = pos, yaw = yaw, heading = heading, scale = scale)
            ent.init()
            self.ents.append(ent);
            self.nEnts = self.nEnts + 1
            return ent

        # robots
        elif entType == self.entTypes[0]:
            enem = entType(self.engine, self.nEnems, pos = pos, yaw = yaw, heading = heading)
            enem.init()
            self.enems.append(enem);
            self.nEnems = self.nEnems + 1
            return enem

        # shields
        elif entType == self.entTypes[5]:
            shield = entType(self.engine, self.nShields, pos = pos, yaw = yaw, heading = heading, scale = scale)
            shield.init()
            self.shields.append(shield);
            self.nShields = self.nShields + 1
            return shield

        # ship
        elif entType == self.entTypes[6]:
            ent = entType(self.engine, self.nEnts, pos = pos, yaw = yaw, heading = heading, scale = scale)
            ent.init()
            self.ents.append(ent);
            self.nEnts = self.nEnts + 1
            return ent
        #pick up
        elif entType == self.entTypes[7]:
            ent = entType(self.engine, self.nEnts, pos = pos, yaw = yaw, heading = heading, scale = scale)
            ent.init()
            self.pickups.append(ent);
            self.nPickups = self.nPickups + 1
            return ent

    def tick(self, dt):

        if self.player!= None:
            self.player.tick(dt)

        if self.player2!=None:
            self.player2.tick(dt)

            for bullet in self.bullets2:
                bullet.tick(dt)
        
        for enem in self.enems:
            enem.tick(dt)

        for ent in self.ents:
            ent.tick(dt)

        for shield in self.shields:
            if self.player.score >= 2000:
                 shield.shieldsOn = False
                 print "shield off"
            shield.tick(dt)

        for bullet in self.bullets:
            bullet.tick(dt)

        for items in self.pickups:
            items.tick(dt)

        # pop out hit bullets from bullets
        temp = []
        for bullet in self.bullets:
            if bullet.isGone == False:
                temp.append(bullet)
        self.bullets = temp

        # pop out hit bullets from bullets2
        if self.player2!=None:
            temp = []
            for bullet in self.bullets2:
                if bullet.isGone == False:
                    temp.append(bullet)
            self.bullets2 = temp

        # pop out dead enemies from enems
        temp = []
        for enem in self.enems:
            if enem.death == False:
                temp.append(enem)
        self.enems = temp

        # pop out shields
        temp = []
        for shield in self.shields:
            if shield.shieldsOn == True:
                temp.append(shield)
        self.shields = temp

        temp = []
        for items in self.pickups:
            if items.death == False:
                temp.append(items)
        self.pickups = temp
         
        
    def stop(self):
        self.ents = []
        self.nEnts = -1
        self.entTypes = []
        

