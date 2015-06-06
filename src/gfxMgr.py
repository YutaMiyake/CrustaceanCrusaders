import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import math
from vector import MyVector

class GfxMgr(OIS.KeyListener):
    def __init__(self, engine):
        self.engine = engine
        OIS.KeyListener.__init__(self)

    def init(self):
        self.game1 = False
        self.game2 = False
        self.game3 = False
        self.gameRunning = False

        self.createRoot()
        self.defineResources()
        self.setupRenderSystem()
        self.createRenderWindow()
        self.initializeResourceGroups()
        self.setupScene()

    def tick(self, dtime):
        if self.game3:
          self.updateTPV2Camera()
        self.updateTPVCamera()
        self.root.renderOneFrame()
        self.updateGUI()

 # The Root constructor for the ogre
    def createRoot(self):
        self.root = ogre.Root()
 
    # Here the resources are read from the resources.cfg
    def defineResources(self):
        cf = ogre.ConfigFile()
        cf.load("resources.cfg")
 
        seci = cf.getSectionIterator()
        while seci.hasMoreElements():
            secName = seci.peekNextKey()
            settings = seci.getNext()
 
            for item in settings:
                typeName = item.key
                archName = item.value
                ogre.ResourceGroupManager.getSingleton().addResourceLocation(archName, typeName, secName)
 
    # Create and configure the rendering system (either DirectX or OpenGL) here
    def setupRenderSystem(self):
        if not self.root.restoreConfig() and not self.root.showConfigDialog():
            raise Exception("User canceled the config dialog -> Application.setupRenderSystem()")
 
    def createRenderWindow(self):
        self.root.initialise(True, "Render Window")
 
    # Initialize the resources here (which were read from resources.cfg in defineResources()
    def initializeResourceGroups(self):
        ogre.TextureManager.getSingleton().setDefaultNumMipmaps(5)
        ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()

    def setupScene(self):
        self.sceneManager = self.root.createSceneManager(ogre.ST_GENERIC, "Default SceneManager")
        self.sceneManager.ambientLight = 1, 1, 1

        # Menu
        self.overlayManager = ogre.OverlayManager.getSingleton() 
        
        self.menuMode = True
        self.menu =  self.overlayManager.getByName("GUI/Menu")
        self.frame = self.overlayManager.getOverlayElement("GUI/Menu/frame")
        self.menuMenu =  self.overlayManager.getOverlayElement("GUI/Menu/menu")
        self.menuItems = []
        self.menuItems.append(self.overlayManager.getOverlayElement("GUI/Menu/start"))
        self.menuItems.append(self.overlayManager.getOverlayElement("GUI/Menu/challenge"))
        self.menuItems.append(self.overlayManager.getOverlayElement("GUI/Menu/versus"))
        self.menuItems.append(self.overlayManager.getOverlayElement("GUI/Menu/instructions"))
        
        self.selectedItem = self.menuItems[0]
        self.selectedItemIndex = 0
        self.numItem = len(self.menuItems)
        self.selectedItem.setColourBottom((0,0,1.0))

        #vs menu
        self.vsmenu = self.overlayManager.getByName("GUI/vsmenu")
        self.vsframe = self.overlayManager.getOverlayElement("GUI/vsmenu/frame")
        self.vsmenuMode = False
        self.vsmenuMenu = self.overlayManager.getOverlayElement("GUI/vsmenu/items")

        self.vsmenuItems = []
        self.vsmenuItems.append(self.overlayManager.getOverlayElement("GUI/vsmenu/normal"))
        self.vsmenuItems.append(self.overlayManager.getOverlayElement("GUI/vsmenu/challenge"))

        self.selectedVsItem = self.vsmenuItems[0]
        self.selectedVsItemIndex = 0
        self.numVsItem = len(self.vsmenuItems)
        self.selectedVsItem.setColourBottom((0,0,1.0))

        # Instructions Menu
        self.imenu = self.overlayManager.getByName("GUI/imenu")
        self.instructionMode = False
        self.iframe = self.overlayManager.getOverlayElement("GUI/imenu/frame")

        # win/loss screen
        self.gameOver = False

        self.winnerText = self.overlayManager.getOverlayElement("GUI/Winner/text")
        self.winnerScreen = self.overlayManager.getByName("GUI/Winner")
        self.winnerFrame = self.overlayManager.getOverlayElement("GUI/Winner/frame")
        self.winner = 0

        self.gameOverScreen = self.overlayManager.getByName("GUI/Gameover")
        self.gameOverFrame = self.overlayManager.getOverlayElement("GUI/Gameover/frame")

        self.Victory = False
        self.VictoryScreen = self.overlayManager.getByName("GUI/Victory")
        self.VictoryFrame = self.overlayManager.getOverlayElement("GUI/Victory/frame")

        # HUD
        self.hearts = self.overlayManager.getByName("GUI/Hearts")
        self.maxHeart = 3
        self.numHeart = 3
        self.heartArr = []
        for i in range(self.maxHeart):
          self.heartArr.append(self.overlayManager.getOverlayElement("GUI/Hearts/heart"+str(i%3)))

        self.hearts2 = self.overlayManager.getByName("GUI/Hearts2")
        self.maxHeart2 = 3
        self.numHeart2 = 3
        self.heartArr2 = []
        for i in range(self.maxHeart2):
          self.heartArr2.append(self.overlayManager.getOverlayElement("GUI/Hearts2/heart"+str(i%3)))

        self.weapons = self.overlayManager.getByName("GUI/Weapons")
        self.selectedWeaponIndex = 0
        self.weaponArr = []
        self.weaponArr.append(self.overlayManager.getOverlayElement("GUI/Weapons/fire"))

        self.targetMark = self.overlayManager.getByName("GUI/Target")
        self.scoreboard = self.overlayManager.getByName("GUI/Score")
        self.scoreArea = self.overlayManager.getOverlayElement("GUI/Score/score")

        # camera
        self.camera = self.sceneManager.createCamera("Camera")
        self.camera.nearClipDistance = 5
        self.camera.lookAt((0,0,0))
        self.camera.setQueryFlags(0)

        self.camera2 = self.sceneManager.createCamera("Camera2")
        self.camera2.nearClipDistance = 5
        self.camera2.lookAt((0,0,0))
        self.camera2.setQueryFlags(0)
        
        # general camera node     
        self.camYawNode = self.sceneManager.getRootSceneNode().createChildSceneNode('CamNode1', (0, 200, 400))
        self.camYawNode.yaw(ogre.Degree(0))
        self.camPitchNode = self.camYawNode.createChildSceneNode('PitchNode1')
        self.camPitchNode.attachObject(self.camera)

        # TPV
        self.TPVCamNode = self.sceneManager.getRootSceneNode().createChildSceneNode('TPVCamNode', (0, 0, 0))
        self.TPVRad = 0
        self.TPVCamNode.yaw(self.TPVRad)
        self.TPVOn = False
        self.TPVCamPitchNode = self.TPVCamNode.createChildSceneNode('TPVCamPitchNode')

        self.TPV2CamNode = self.sceneManager.getRootSceneNode().createChildSceneNode('TPV2CamNode', (0, 0, 0))
        self.TPV2Rad = 0
        self.TPV2CamNode.yaw(self.TPV2Rad)
        self.TPV2CamPitchNode = self.TPV2CamNode.createChildSceneNode('TPV2CamPitchNode')

        # viewport
        self.viewPort = self.root.getAutoCreatedWindow().addViewport(self.camera, 0, 0, 0, 1.0,1.0)

        # ground plane.
        self.groundPlane = ogre.Plane ((0, 1, 0), 0)
        meshManager = ogre.MeshManager.getSingleton()
        meshManager.createPlane ('Ground', 'General', self.groundPlane,
                                     10000, 10000, 20, 20, True, 1, 5, 5, (0, 0, 1))
        self.ground = self.sceneManager.createEntity('GroundEntity', 'Ground')
        self.sceneManager.getRootSceneNode().createChildSceneNode().attachObject (self.ground)
        self.ground.setMaterialName ('dancetile')
        self.ground.castShadows = False
        self.ground.setVisible(False)
        self.GBBOX = self.ground.getWorldBoundingBox(True)

    def stop(self):
        del self.root

    def showMenu(self):
        self.menuMode = True
        self.frame.show()

    def showIMenu(self):
        self.instructionMode = True
        self.imenu.show()

    def hideMenu(self):
        self.menuMode = False
        self.frame.hide()

    def hideVsMenu(self):
        self.vsmenuMode = False
        self.vsmenu.hide()

    def hideIMenu(self):
        self.instructionMode = False
        self.imenu.hide()

    def showHUD(self):
        self.hearts.show()
        self.weapons.show()
        self.targetMark.show()
        self.scoreboard.show()

    def showHUD2(self):
        self.hearts.show()
        self.hearts2.show()
        self.weapons.show()
        self.targetMark.show()

    def showEnv(self):
      # set sky
      plane = ogre.Plane((0,-1,0),-10)
      self.sceneManager.setSkyPlane(True, plane,"star_effect1",100,45,True,0.5,150,150)
      #self.overlayManager.getOverlayElement("GUI/logo")

      # enable ground
      self.ground.setVisible(True)

    def updateGUI(self):
        if self.menuMode:
            self.frame.setDimensions(self.viewPort.actualWidth,self.viewPort.actualHeight)

        elif self.instructionMode:
          self.iframe.setDimensions(self.viewPort.actualWidth,self.viewPort.actualHeight)

        elif self.vsmenuMode:
          self.vsframe.setDimensions(self.viewPort.actualWidth,self.viewPort.actualHeight)

        if self.gameOver:
            self.gameOverFrame.setDimensions(self.viewPort.actualWidth,self.viewPort.actualHeight)
            self.winnerFrame.setDimensions(self.viewPort.actualWidth,self.viewPort.actualHeight)

            if self.game3:
              self.winnerText.setCaption( "Player"+str(self.winner)+" win")
              self.winnerScreen.show()
            else:
              self.gameOverScreen.show()

        if self.Victory:
            self.VictoryFrame.setDimensions(self.viewPort.actualWidth,self.viewPort.actualHeight)
            self.VictoryScreen.show()

        if not self.game3 and self.gameRunning:
            self.scoreArea.setCaption(str(self.engine.entityMgr.player.score))

    def goUpVsMenu(self):
        self.engine.gfxMgr.selectedVsItem.setColourBottom((0,0,0))
        self.selectedVsItemIndex = self.selectedVsItemIndex + 1
        self.selectedVsItem = self.vsmenuItems[self.selectedVsItemIndex % self.numVsItem]
        self.selectedVsItem.setColourBottom((0,0,1.0))

    def goDownVsMenu(self):
        self.engine.gfxMgr.selectedVsItem.setColourBottom((0,0,0))
        self.selectedVsItemIndex = self.selectedVsItemIndex - 1
        self.selectedVsItem = self.vsmenuItems[self.selectedVsItemIndex % self.numVsItem]
        self.selectedVsItem.setColourBottom((0,0,1.0))

    def gotoSelectedVsItem(self):
      cap = self.selectedVsItem.getCaption()

      if cap == "Normal Mode":
        self.hideVsMenu()
        self.game3 = True
        self.TPV2CamPitchNode.attachObject(self.camera2)
        self.root.getAutoCreatedWindow().removeViewport(0)
        self.viewPort = self.root.getAutoCreatedWindow().addViewport(self.camera, 1, 0, 0, 0.5,1.0)
        self.viewPort2 = self.root.getAutoCreatedWindow().addViewport(self.camera2, 0, 0.5, 0, 0.5, 1.0) 
        self.showEnv()
        self.showHUD2()
        self.engine.gameMgr.game3()
        self.engine.collisionMgr.makeStaticQuadTree()
        self.engine.sndMgr.playbgm2()
        self.initTPVCamera()
        self.useTPVCamera()
        self.initTPV2Camera()
        self.gameRunning = True
        
      elif cap == "Challenge Mode":
        self.hideVsMenu()
        self.game3 = True
        self.game2 = True
        self.TPV2CamPitchNode.attachObject(self.camera2)
        self.root.getAutoCreatedWindow().removeViewport(0)
        self.viewPort = self.root.getAutoCreatedWindow().addViewport(self.camera, 1, 0, 0, 0.5,1.0)
        self.viewPort2 = self.root.getAutoCreatedWindow().addViewport(self.camera2, 0, 0.5, 0, 0.5, 1.0) 
        self.showEnv()
        self.showHUD2()
        self.engine.gameMgr.game2()
        self.engine.collisionMgr.makeStaticQuadTree()
        self.engine.sndMgr.playbgm2()
        self.initTPVCamera()
        self.useTPVCamera()
        self.initTPV2Camera()
        self.gameRunning = True

    def goUpMenu(self):
        self.engine.gfxMgr.selectedItem.setColourBottom((0,0,0))
        self.selectedItemIndex = self.selectedItemIndex + 1
        self.selectedItem = self.menuItems[self.selectedItemIndex % self.numItem]
        self.selectedItem.setColourBottom((0,0,1.0))

    def goDownMenu(self):
        self.engine.gfxMgr.selectedItem.setColourBottom((0,0,0))
        self.selectedItemIndex = self.selectedItemIndex - 1
        self.selectedItem = self.menuItems[self.selectedItemIndex % self.numItem]
        self.selectedItem.setColourBottom((0,0,1.0))

    def gotoSelectedItem(self):
        cap = self.selectedItem.getCaption()

        if cap == "Normal Mode":
           self.engine.gameMgr.game1() 
           self.game1 = True
           self.engine.collisionMgr.makeStaticQuadTree() 
           self.hideMenu()
           self.engine.sndMgr.playbgm2()
           self.showHUD()
           self.showEnv()
           self.initTPVCamera()
           self.useTPVCamera()
           self.gameRunning = True

        elif cap == "Challenge Mode":
           self.game2 = True
           self.engine.gameMgr.game2()
           self.engine.collisionMgr.makeStaticQuadTree() 
           self.hideMenu()
           self.engine.sndMgr.playbgm2()
           self.showHUD()
           self.showEnv()
           self.initTPVCamera()
           self.useTPVCamera()
           self.gameRunning = True   

        elif cap == "Instructions":
           self.hideMenu()
           self.showIMenu()

        elif cap == "VS Mode":
          self.vsmenuMode = True
          self.hideMenu()
          self.vsmenu.show()
          
    # heart management
    def updateHeart(self, num):
           self.numHeart += num

           if self.numHeart >= self.maxHeart:
              self.numHeart = self.maxHeart

           elif self.numHeart <= 0:
              self.numHeart = 0
              for i in range(self.maxHeart):
                  self.heartArr[i].setMaterialName("GUI/Hearts/zeroheartText")

           current = self.numHeart
           ctr = 0

           self.clearHeart()

           for i in range(int(self.maxHeart-current)):
                self.heartArr[self.maxHeart-1-i].setMaterialName("GUI/Hearts/zeroheartText")

           while(current >= 1.0):
               self.heartArr[ctr].setMaterialName("GUI/Hearts/heartText")
               ctr = ctr+1
               current = current - 1;

           if current == 0.5:
              self.heartArr[ctr].setMaterialName("GUI/Hearts/halfheartText")

    def clearHeart(self):
        for ctr in range(self.maxHeart):
            self.heartArr[ctr].setMaterialName("")

    def updateHeart2(self, num):
           self.numHeart2 += num

           if self.numHeart2 >= self.maxHeart2:
              self.numHeart2 = self.maxHeart2

           elif self.numHeart2 <= 0:
              self.numHeart2 = 0
              for i in range(self.maxHeart2):
                  self.heartArr2[i].setMaterialName("GUI/Hearts/zeroheartText")

           current = self.numHeart2
           ctr = 0

           self.clearHeart2()

           for i in range(int(self.maxHeart2-current)):
                self.heartArr2[self.maxHeart2-1-i].setMaterialName("GUI/Hearts/zeroheartText")

           while(current >= 1.0):
               self.heartArr2[ctr].setMaterialName("GUI/Hearts/heartText")
               ctr = ctr+1
               current = current - 1;

           if current == 0.5:
              self.heartArr2[ctr].setMaterialName("GUI/Hearts/halfheartText")

    def clearHeart2(self):
        for ctr in range(self.maxHeart2):
            self.heartArr2[ctr].setMaterialName("")

    # Camera
    def useCamera(self):
        if self.TPVOn:
           self.camera.parentSceneNode.detachObject(self.camera)
           self.sceneManager.getSceneNode("PitchNode1").attachObject(self.camera)
           self.TPVOn = False
    
    def useTPVCamera(self):
        if self.engine.entityMgr.player != None:
           self.camera.parentSceneNode.detachObject(self.camera)
           self.sceneManager.getSceneNode("TPVCamPitchNode").attachObject(self.camera)
           self.TPVOn = True

    def initTPVCamera(self):
        p1 = self.engine.entityMgr.player
        self.camera.yaw(ogre.Degree(90))
        direction = MyVector(-20*math.sin(p1.heading),0, -20*math.cos(p1.heading))
        self.TPVCamNode.setPosition(p1.pos.x+direction.x,p1.pos.y+90,p1.pos.z+direction.z)
        self.TPVRad = p1.heading
        self.TPVPitch = p1.pitch

    def updateTPVCamera(self):
       if self.TPVOn:
          p1 = self.engine.entityMgr.player 
          direction = MyVector(-20*math.sin(p1.heading),0, -20*math.cos(p1.heading))
          self.TPVCamNode.setPosition(p1.pos.x+direction.x,p1.pos.y+90,p1.pos.z+direction.z)
          self.TPVCamNode.yaw(-(self.TPVRad - p1.heading))
          self.TPVRad = p1.heading
          self.TPVCamPitchNode.roll(p1.pitch-self.TPVPitch)
          self.TPVPitch = p1.pitch

    def initTPV2Camera(self):
        p2 = self.engine.entityMgr.player2
        self.camera2.yaw(ogre.Degree(90))
        direction = MyVector(-20*math.sin(p2.heading),0, -20*math.cos(p2.heading))
        self.TPV2CamNode.setPosition(p2.pos.x+direction.x,p2.pos.y+90,p2.pos.z+direction.z)
        self.TPV2Rad = p2.heading
        self.TPV2Pitch = p2.pitch

    def updateTPV2Camera(self):
       if self.TPVOn:
          p2 = self.engine.entityMgr.player2
          direction = MyVector(-20*math.sin(p2.heading),0, -20*math.cos(p2.heading))
          self.TPV2CamNode.setPosition(p2.pos.x+direction.x,p2.pos.y+90,p2.pos.z+direction.z)
          self.TPV2CamNode.yaw(-(self.TPV2Rad - p2.heading))
          self.TPV2Rad = p2.heading
          self.TPV2CamPitchNode.roll(p2.pitch - self.TPV2Pitch)
          self.TPV2Pitch = p2.pitch