
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import utils

class InputMgr(OIS.KeyListener, OIS.MouseListener, OIS.JoyStickListener):
    def __init__(self, engine):
        self.engine = engine
        self.toggle = 0.1
        self.rotate = 0.1
	self.yaw = 0.1
	self.pitch = 0.1;
        self.transVector = ogre.Vector3(0, 0, 0);

        self.move = 500
        
        OIS.KeyListener.__init__(self)
        OIS.MouseListener.__init__(self)
        OIS.JoyStickListener.__init__(self)

    def init(self):
        # initialize an input system
        windowHandle = 0
        renderWindow = self.engine.gfxMgr.root.getAutoCreatedWindow()

        import platform
        int64 = False
        for bit in platform.architecture():
            if '64' in bit:
                int64 = True
        if int64:
            windowHandle = renderWindow.getCustomAttributeUnsignedLong("WINDOW")
        else:
            windowHandle = renderWindow.getCustomAttributeInt("WINDOW")
        t = [("x11_mouse_grab", "false"), ("x11_mouse_hide", "false")]
        paramList = [("WINDOW", str(windowHandle))]

        paramList.extend(t)
        self.inputManager = OIS.createPythonInputSystem(paramList)
 
        # Now InputManager is initialized for use. Keyboard and Mouse objects
        # must still be initialized separately
        self.keyboard = None
        self.mouse    = None

        try:
            self.keyboard = self.inputManager.createInputObjectKeyboard(OIS.OISKeyboard, True)
            self.mouse = self.inputManager.createInputObjectMouse(OIS.OISMouse, True)
        except Exception, e:
            print "No Keyboard or mouse!!!!"
            raise e
        if self.keyboard:
            self.keyboard.setEventCallback(self)
        if self.mouse:
            self.mouse.setEventCallback(self)

        # camera
        self.camera = self.engine.gfxMgr.camera
        self.camYawNode = self.engine.gfxMgr.camYawNode
        self.camPitchNode = self.engine.gfxMgr.camPitchNode

    def stop(self):
        # clean everything up (= delete)
        self.inputManager.destroyInputObjectKeyboard(self.keyboard)
        self.inputManager.destroyInputObjectMouse(self.mouse)
        OIS.InputManager.destroyInputSystem(self.inputManager)
        self.inputManager = None
      
    def tick(self, dtime):
        self.toggle -= dtime
        self.dtime = dtime
        self.keyboard.capture()
        self.mouse.capture()
        self.keyPressed(dtime)

        if self.engine.gfxMgr.gameRunning and not self.engine.gfxMgr.TPVOn:
           # Rotate the camera based on time.
           self.camYawNode.yaw(ogre.Radian(self.yaw))
           self.camPitchNode.roll(ogre.Radian(self.pitch))

           # Translate the camera based on time.
           self.camYawNode.translate(self.camYawNode.orientation
                               * self.transVector
                               * dtime)

#------------------------------------------------------------------------------ 
    # KeyListner
    def keyPressed(self, evt):

        player = self.engine.entityMgr.player
        player2 = self.engine.entityMgr.player2

        # end game
        if self.keyboard.isKeyDown(OIS.KC_ESCAPE):
            self.engine.stop()

        # instruction mode
        if self.engine.gfxMgr.instructionMode:
            if self.toggle <= 0:
                self.toggle = 0.1
                if self.keyboard.isKeyDown(OIS.KC_SPACE) or self.keyboard.isKeyDown(OIS.KC_RETURN):
                    self.engine.gfxMgr.hideIMenu()
                    self.engine.gfxMgr.showMenu()

        # menu mode
        elif self.engine.gfxMgr.menuMode:
            if self.toggle <= 0:
                self.toggle = 0.1
                if self.keyboard.isKeyDown(OIS.KC_DOWN):
                    self.engine.gfxMgr.goUpMenu()

                if self.keyboard.isKeyDown(OIS.KC_UP):
                    self.engine.gfxMgr.goDownMenu()

                if self.keyboard.isKeyDown(OIS.KC_SPACE) or self.keyboard.isKeyDown(OIS.KC_RETURN):
                    self.engine.gfxMgr.gotoSelectedItem()

        # vs menu mode
        elif self.engine.gfxMgr.vsmenuMode:
            if self.toggle <= 0:
                self.toggle = 0.1
                if self.keyboard.isKeyDown(OIS.KC_DOWN):
                    self.engine.gfxMgr.goUpVsMenu()

                if self.keyboard.isKeyDown(OIS.KC_UP):
                    self.engine.gfxMgr.goDownVsMenu()

                if self.keyboard.isKeyDown(OIS.KC_SPACE) or self.keyboard.isKeyDown(OIS.KC_RETURN):
                    self.engine.gfxMgr.gotoSelectedVsItem()

        if not self.engine.gfxMgr.gameRunning:
            return

        # game mode
        if self.engine.gfxMgr.TPVOn:
            if not self.engine.gfxMgr.gameOver and player != None:
                # Turn Left.
                if  self.keyboard.isKeyDown(OIS.KC_A):
                    player.heading += self.rotate
                
                # Turn Right.
                if  self.keyboard.isKeyDown(OIS.KC_D):
                    player.heading -= self.rotate

                if self.keyboard.isKeyDown(OIS.KC_LSHIFT):
                    player.runSpeed = +1000
                else:
                   player.runSpeed = 500


                if self.keyboard.isKeyDown(OIS.KC_Z):
                    player.pitch -= self.rotate
                if self.keyboard.isKeyDown(OIS.KC_X):
                    player.pitch += self.rotate

        if self.engine.gfxMgr.game3:
            if not self.engine.gfxMgr.gameOver and player2 != None:
                # Turn Left.
                if  self.keyboard.isKeyDown(OIS.KC_LEFT):
                    player2.heading += self.rotate
                
                # Turn Right.
                if  self.keyboard.isKeyDown(OIS.KC_RIGHT):
                    player2.heading -= self.rotate
                
                if self.keyboard.isKeyDown(OIS.KC_RSHIFT):
                    player2.runSpeed = +1000
                else:
                    player2.runSpeed = 500

        if not self.engine.gfxMgr.TPVOn:
            self.handleCamera()

        if self.toggle > 0:
            return True
        else:
            self.toggle = 0.1

        #TPV Camera -----------------------------
        if self.keyboard.isKeyDown(OIS.KC_Y):
           self.engine.gfxMgr.useCamera()
        elif self.keyboard.isKeyDown(OIS.KC_T):  
           self.engine.gfxMgr.useTPVCamera()

        return True
            

    def keyReleased(self, evt):
        if evt.key == OIS.KC_SPACE:
            if self.engine.controlMgr.chargeToggle:
               self.engine.controlMgr.release()

        if evt.key == OIS.KC_RETURN:
            if self.engine.controlMgr.chargeToggle2:
                self.engine.controlMgr.release2()
        return True

    def handleCamera(self):
        self.transVector = ogre.Vector3(0, 0, 0)
        self.yaw = 0.0
        self.pitch = 0.0
        # Move Forward.
        if self.keyboard.isKeyDown(OIS.KC_W):
            self.transVector.x -= self.move
        # Move Backward.
        if self.keyboard.isKeyDown(OIS.KC_S):
            self.transVector.x += self.move
        # Strafe Left.
        if self.keyboard.isKeyDown(OIS.KC_A):
            self.transVector.z += self.move
        # Strafe Right.
        if  self.keyboard.isKeyDown(OIS.KC_D):
            self.transVector.z -= self.move
        # Move Up.        
        if self.keyboard.isKeyDown(OIS.KC_P):
            self.transVector.y += self.move
        # Move Down.
        if self.keyboard.isKeyDown(OIS.KC_L):
            self.transVector.y -= self.move

        # Rotate the camera
        if self.keyboard.isKeyDown(OIS.KC_Q):
            self.yaw = self.rotate
        if self.keyboard.isKeyDown(OIS.KC_E):
            self.yaw = -self.rotate
        if self.keyboard.isKeyDown(OIS.KC_Z):
            self.pitch = -self.rotate
        if self.keyboard.isKeyDown(OIS.KC_X):
            self.pitch = self.rotate

#------------------------------------------------------------------------------  
    # MouseListener   
    def mouseMoved(self, evt):
        self.handleMouseMoved(evt)
        self.oldMs = self.ms
        return True

    def mousePressed(self, evt, id):
        self.handleMousePressed(evt, id)
        return True

    def mouseReleased(self, evt, id):
        if self.engine.gfxMgr.game3:
            if id == OIS.MB_Left and self.engine.controlMgr.chargeToggle2:
                self.engine.controlMgr.release2()
        else:
            if id == OIS.MB_Left and self.engine.controlMgr.chargeToggle:
                self.engine.controlMgr.release()
        return True

    def handleMousePressed(self,evd,id):
        self.mouse.capture()
        self.mousePos = self.getMousePos()

        if self.engine.gfxMgr.menuMode:
            textElem = self.engine.gfxMgr.menuMenu.findElementAt(*self.mousePos)
            if textElem and textElem.getCaption() != "":
                self.engine.gfxMgr.selectedItem = textElem
                self.engine.gfxMgr.gotoSelectedItem()

        elif self.engine.gfxMgr.vsmenuMode:
            textElem = self.engine.gfxMgr.vsmenuMenu.findElementAt(*self.mousePos)
            if textElem and textElem.getCaption() != "":
                self.engine.gfxMgr.selectedVsItem = textElem
                self.engine.gfxMgr.gotoSelectedVsItem()

        elif not self.engine.gfxMgr.gameOver and self.engine.gfxMgr.TPVOn and id == OIS.MB_Left: 
                if self.engine.gfxMgr.game3: 
                    self.engine.controlMgr.charge2(self.dtime)
                else:
                    self.engine.controlMgr.charge(self.dtime)

    def getMousePos(self):
        self.ms = self.mouse.getMouseState()
        self.ms.width = self.engine.gfxMgr.viewPort.actualWidth 
        self.ms.height = self.engine.gfxMgr.viewPort.actualHeight
        return (self.ms.X.abs/float(self.ms.width), self.ms.Y.abs/float(self.ms.height))

    def handleMouseMoved(self, evt):
        self.mousePos =self.getMousePos()

        if self.engine.gfxMgr.menuMode:
            textElem = self.engine.gfxMgr.menuMenu.findElementAt(*self.mousePos)

            if textElem and textElem.getCaption() != "":
                self.engine.gfxMgr.selectedItem.setColourBottom((0,0,0))
                self.engine.gfxMgr.selectedItem = textElem
                self.engine.gfxMgr.selectedItem.setColourBottom((0,0,1.0))

        # vs menu mode
        elif self.engine.gfxMgr.vsmenuMode:
            textElem = self.engine.gfxMgr.vsmenuMenu.findElementAt(*self.mousePos)

            if textElem and textElem.getCaption() != "":
                self.engine.gfxMgr.selectedVsItem.setColourBottom((0,0,0))
                self.engine.gfxMgr.selectedVsItem = textElem
                self.engine.gfxMgr.selectedVsItem.setColourBottom((0,0,1.0))


        if not self.engine.gfxMgr.gameOver and self.engine.gfxMgr.TPVOn:    
            if self.engine.gfxMgr.game3:
                player = self.engine.entityMgr.player2
            else:
                player = self.engine.entityMgr.player                

            if player != None:
                if self.ms.buttonDown(OIS.MB_Right):
                    player.heading += ogre.Degree(-0.1
                                            * self.ms.X.rel-self.oldMs.X.rel).valueRadians()
                    pitch = -ogre.Degree(-0.1* self.ms.Y.rel-self.oldMs.Y.rel).valueRadians()
                    player.pitch += pitch


#------------------------------------------------------------------------------  
    # JoystickListener
    def buttonPressed(self, evt, button):
        return True
    def buttonReleased(self, evt, button):
        return True
    def axisMoved(self, evt, axis):
        return True
        

