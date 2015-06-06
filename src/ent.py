#Yuta Miyake
from vector import MyVector
from physics import Physics
from render  import Renderable
from myWake import Wake

import math

class Entity:
    def __init__(self, engine, id, pos = MyVector(0,0,0), mesh = 'robot.mesh', 
                    vel = MyVector(0, 0, 0), yaw = 0, heading = 0, scale = (1,1,1)):
        self.engine = engine
        aspectTypes = []
        
        self.uiname = "Robot" + str(id)
        self.eid = id
        self.pos = pos
        self.vel = vel
        self.mesh = mesh

        self.speed = 0.0
        self.heading = 0.0
        self.desiredHeading = 0.0

        self.aspects = []

    def init(self):
        self.initAspects()

    def initAspects(self):
        for aspType in self.aspectTypes:
            self.aspects.append(aspType(self))
        
    def tick(self, dtime):
        for aspect in self.aspects:
            aspect.tick(dtime)

    def __str__(self):
        x = "Entity: %s %s \nPos: %s Vel: %s \nSpeed: %f, Heading: %f" % (str(self.uiname), self.eid, str(self.pos), str(self.vel), self.speed, self.heading)
        return x


class robot(Entity):
    def __init__(self, engine, id, pos = MyVector(0,0,0), vel = MyVector(0, 0, 0), yaw = 0, heading = 0, scale = (1,1,1)):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw, heading = heading, scale = scale)
        self.mesh = 'robot.mesh'
        self.uiname = 'robot' + str(id)
        self.eid = id
        self.aspectTypes = [Physics, Renderable]

        self.scale = scale

        self.timer = 0
        self.hit = False
        self.power = 100
        self.health = 100
        self.death = False

        self.speed = 0
        self.minSpeed = 50
        self.maxSpeed = 200
        self.move = False

        self.turningRate  = 2
        self.desiredHeading = heading
        self.heading = heading

        self.proximity = 100
        self.sightDistance = 800
        
        if self.engine.gfxMgr.game2 == True:
            self.sightDistance = 10000
            self.maxSpeed = 400
        self.point = 300
        self.lockOn = False
        self.causion = False
        self.yaw = yaw

class player(Entity):
    def __init__(self, engine,id, pos = MyVector(0,0,0),vel = MyVector(0, 0, 0),yaw = 0, heading = 0):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw, heading = heading)
        self.mesh = 'ninja.mesh'
        self.uiname = 'ninja' + str(id)
        self.eid = id
        self.aspectTypes=[Physics, Renderable]

        self.timer = 0
        self.damage = False
        self.health = 600
        self.death = False
        self.proximity = 50
        self.pitch = 0

        if self.death == True:
            counter = 0
            counter = counter + 1
            if counter == 1:
                self.engine.sndMgr.playwaa()

        if self.engine.gfxMgr.game2 == True:
            self.runSpeed = 1000
        else:
            self.runSpeed = 500

        self.move = False
        self.vel = MyVector(0,0,0)
        self.acceleration = 2
        self.maxSpeed = 1000
        self.desiredSpeed = 0
        self.speed = 0
        self.turningRate  = 1
        self.desiredHeading = math.pi/2
        self.heading = math.pi/2
        self.yaw  = yaw

        self.score = 0

class pickupItem(Entity):
    def __init__(self, engine,id, pos=MyVector(0,0,0),vel = MyVector(0, 0, 0),yaw = 0, heading = 0, scale = (1,1,1), pickupType = 'Armor'):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw, heading = heading)
        '''
        to be added later
        '''
        self.mesh = 'shield.mesh'
        self.uiname = 'pickup'+ str(id)
        self.scale = scale
        self.yaw = yaw
        self.bobMax = 75
        self.bobMin = 25
        self.bobReset = False
        self.proximity = 50
        self.healthAmount = 2
        self.death = False
        self.pickupType = pickupType
        self.aspectTypes = [Physics, Renderable]


class cubeWall(Entity):
    def __init__(self, engine,id, pos=MyVector(0,0,0),vel = MyVector(0, 0, 0),yaw = 0, heading = 0, scale = (1,1,1)):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw, heading = heading)
        self.mesh = 'cube.mesh'
        self.uiname = 'wall' + str(id)

        self.scale = scale
        self.heading = heading
        self.yaw = yaw
        self.proximity = 50
        self.aspectTypes = [Physics, Renderable]

class shieldWall(Entity):
    def __init__(self, engine,id, pos=MyVector(0,0,0),vel = MyVector(0, 0, 0),yaw = 0, heading = 0, scale = (1,1,1)):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw, heading = heading)
        self.mesh = 'cube.mesh'
        self.uiname = 'shield'
        self.shieldsOn = True

        self.scale = scale
        self.heading = heading
        self.yaw = yaw
        self.proximity = 50
        self.aspectTypes = [Physics, Renderable]

class orb(Entity):
    def __init__(self, engine,id, pos=MyVector(0,0,0),vel = MyVector(0, 0, 0),yaw = 0, heading = 0, scale = (.02,.02,.02)):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw, heading = heading, scale = scale)
        self.mesh = 'sphere.mesh'
        self.uiname = 'bullet' + str(id)
        self.eid = id

        self.speed = 400
        self.heading = heading
        self.initialPos = pos
        self.pitch = 0

        self.scale = scale
        self.power = 30
        self.distance = 1000
        self.isGone = False
        self.aspectTypes = [Physics, Renderable, Wake]

class lobster(Entity):
    def __init__(self, engine,id, pos=MyVector(0,0,0),vel = MyVector(0, 0, 0),yaw = 0, heading = 0, scale = (1,1,1)):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw, heading = heading)
        self.mesh = 'astatusMesh.mesh'
        self.uiname = 'lobster' + str(id)
        self.eid = id
        self.aspectTypes = [Physics, Renderable]

        self.timer = 0
        self.hit = False
        self.power = 100
        self.health = 100
        self.death = False

        self.speed = 0
        self.minSpeed = 50
        self.maxSpeed = 200
        self.move = False

        self.turningRate  = 2
        self.desiredHeading = 0
        self.heading = 0

        self.proximity = 50
        #if self.engine.gfxMgr.game2 == True:
        #    self.proximity = 10000
        self.initialPos = MyVector(pos.x,pos.y,pos.z)
        self.sightDistance = 500

        self.point = 300

class ship(Entity):
    def __init__(self, engine,id, pos=MyVector(0,0,0),vel = MyVector(0, 0, 0),yaw = 0, heading = 0, scale = (1,1,1)):
        Entity.__init__(self, engine, id, pos = pos, vel = vel, yaw = yaw, heading = heading)
        self.mesh = 'alienship.mesh'
        self.uiname = 'alienship'
        self.eid = id
        self.aspectTypes = [Physics, Renderable]

        self.timer = 0
        self.hit = False
        self.power = 100
        self.health = 100
        self.death = False

        self.speed = 0
        self.minSpeed = 50
        self.maxSpeed = 200
        self.move = False

        self.turningRate  = 2
        self.desiredHeading = 0
        self.heading = 0

        self.proximity = 50
        #if self.engine.gfxMgr.game2 == True:
        #    self.proximity = 10000
        self.initialPos = MyVector(pos.x,pos.y,pos.z)
        self.sightDistance = 500

        self.point = 300
