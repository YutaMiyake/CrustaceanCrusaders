#Yuta Miyake
from vector import MyVector
import math

class GameMgr:
    def __init__(self, engine):
        self.engine = engine
        print "starting Game mgr"
        pass

    def init(self):
        pass
        
    def game1(self):

        #player
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[1], pos = MyVector(-500, 0, -100))

        #maze
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(-1350,50,2700),scale = (10,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(-1350,50,-450),scale = (35,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(-1350,50,4500),scale = (10,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(-900,50,1800),scale = (10,5,10))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(-900,50,3600),scale = (10,5,10))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(-900,50,-2250),scale = (10,5,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(-450,50,-3600),scale = (20,5,10))

        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(0,50,450), scale = (8,5,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(0,50,-450), scale = (8,5,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(450,50,2250), scale = (17,5,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(50,50,4050), scale = (9,5,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(900,50,4050), scale = (8,5,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(0,50,-2250), scale = (8,5,1))

        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(450,50,0), scale = (10,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(450,50,-900),scale = (10,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(450,50,900),scale = (10,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(450,50,-2650),scale = (9,5,1),heading = math.pi/2)

        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(900,50,3150),scale = (8,5,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(900,50,1350),scale = (8,5,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(900,50,-450),scale = (8,5,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(900,50,-1350),scale = (8,5,1)) 
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(1350,50,-3150),scale = (16,5,1))

        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(1350,50,950),scale = (9,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(1350,50,0),scale = (10,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(1350,50,-1800),scale = (10,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(1350,50,2700),scale = (10,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(1350,50,4500),scale = (10,5,1),heading = math.pi/2)

        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(2250,50,-1400),scale = (10,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(2250,50,-400),scale = (10,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(2250,50, 600),scale = (10,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(2250,50,1600),scale = (10,5,1),heading = math.pi/2)

        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(3600,50,-900),scale = (10,5,10))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(3600,50,-1800),scale = (10,5,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(3600,50,1800),scale = (20,5,5))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(3600,50,3200),scale = (5,5,20))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(3600,50,-3600),scale = (10,5,10))

        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(4050,50,-450),scale = (10,5,10))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(4500,50,-1800),scale = (10,5,1))


        #shields
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[5], pos = MyVector(-1350,50,-4500),scale = (1,5,9))

        # center position
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(0,50,0), scale = (1,1,1))
        p = self.engine.gfxMgr.sceneManager.createParticleSystem('fire1_P', "myParticle/Fire")
        node = self.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode('fire1_Pnode')
        node.translate(MyVector(50,150,0))
        node.attachObject(p)
        
        # walls around the ground
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(0,50,-5000), scale = (100,40,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(0,50,5000), scale = (100,40,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(-5000,50,0), heading = -math.pi/2, scale = (100,40,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(5000,50,0), heading = -math.pi/2, scale = (100,40,1))

        #spawn enemy
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(-900,0,900), heading = math.pi/2)
        
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(100,0,900), heading = -math.pi)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(100,0,1000), heading = -math.pi)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(100,0,1100), heading = -math.pi)
        
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(-100,0,-900), heading = -math.pi)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(-100,0,-700), heading = -math.pi)

        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(-50,0,-1700))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(-50,0,-1900))
        
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(1200,0,-1000))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(1200,0,-800))
        
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(-1200,0,-4500))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(-1200,0,-4300))

        #ship
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[6], pos = MyVector(-4000,50,4500), scale = (100,100,100), heading = -math.pi/2)

        #pickup shield
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[7], pos = MyVector(-700,50,-100), scale = (10,10,10), heading = -math.pi/2)


        
    def game2(self):
        #player
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[1], pos = MyVector(-600, 0, 110))
        
        if self.engine.gfxMgr.game3:
            self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[1], pos = MyVector(-300, 0, -10))
    
    def game3(self):

        #player
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[1], pos = MyVector(-500, 0, -10))

        #player2
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[1], pos = MyVector(-300, 0, -10))
        
        #maze
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(-1350,50,2700),scale = (10,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(-1350,50,-450),scale = (35,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(-1350,50,4500),scale = (10,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(-900,50,1800),scale = (10,5,10))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(-900,50,3600),scale = (10,5,10))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(-900,50,-2250),scale = (10,5,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(-450,50,-3600),scale = (20,5,10))

        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(0,50,450), scale = (8,5,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(0,50,-450), scale = (8,5,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(450,50,2250), scale = (17,5,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(50,50,4050), scale = (9,5,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(900,50,4050), scale = (8,5,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(0,50,-2250), scale = (8,5,1))

        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(450,50,0), scale = (10,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(450,50,-900),scale = (10,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(450,50,900),scale = (10,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(450,50,-2650),scale = (9,5,1),heading = math.pi/2)

        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(900,50,3150),scale = (8,5,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(900,50,1350),scale = (8,5,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(900,50,-450),scale = (8,5,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(900,50,-1350),scale = (8,5,1)) 
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(1350,50,-3150),scale = (16,5,1))

        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(1350,50,950),scale = (9,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(1350,50,0),scale = (10,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(1350,50,-1800),scale = (10,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(1350,50,2700),scale = (10,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(1350,50,4500),scale = (10,5,1),heading = math.pi/2)

        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(2250,50,-1400),scale = (10,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(2250,50,-400),scale = (10,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(2250,50, 600),scale = (10,5,1),heading = math.pi/2)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(2250,50,1600),scale = (10,5,1),heading = math.pi/2)

        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(3600,50,-900),scale = (10,5,10))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(3600,50,-1800),scale = (10,5,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(3600,50,1800),scale = (20,5,5))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(3600,50,3200),scale = (5,5,20))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(3600,50,-3600),scale = (10,5,10))

        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(4050,50,-450),scale = (10,5,10))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(4500,50,-1800),scale = (10,5,1))


        #shields
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[5], pos = MyVector(-1350,50,-4500),scale = (1,5,9))

        # center
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(50,50,0), scale = (1,1,1))
        p = self.engine.gfxMgr.sceneManager.createParticleSystem('fire1_P', "myParticle/Fire")
        node = self.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode('fire1_Pnode')
        node.translate(MyVector(50,150,0))
        node.attachObject(p)
        
        # walls around the ground
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(0,50,-5000), scale = (100,40,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(0,50,5000), scale = (100,40,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(-5000,50,0), heading = -math.pi/2, scale = (100,40,1))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[2], pos = MyVector(5000,50,0), heading = -math.pi/2, scale = (100,40,1))
        

        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(-900,0,900), heading = math.pi/2)
        
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(100,0,900), heading = -math.pi)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(100,0,1000), heading = -math.pi)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(100,0,1100), heading = -math.pi)
        
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(-100,0,-900), heading = -math.pi)
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(-100,0,-700), heading = -math.pi)

        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(-50,0,-1800))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(-50,0,-1900))
        
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(1200,0,-1000))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(1200,0,-900))
        
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(-1200,0,-4500))
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[0], pos = MyVector(-1200,0,-4300))

        #ship
        self.engine.entityMgr.createEnt(self.engine.entityMgr.entTypes[6], pos = MyVector(-4000,50,4500), scale = (100,100,100), heading = -math.pi/2)


    def tick(self, dt):
        pass

    def stop(self):
        pass
        

