import quadtree
import random
from vector import MyVector
import math

class CollisionMgr:
    def __init__(self, engine):
        self.engine = engine
        self.toggle = 0.1
        self.delay = 0
        self.counter = 0

    def init(self):
        pass

    def makeStaticQuadTree(self):
        rect = self.getRect(self.engine.gfxMgr.GBBOX)
        self.sQuadT = quadtree.QuadTree(0,rect)

        for ent in self.engine.entityMgr.ents:
            self.sQuadT.insert(self.getRect(ent.aspects[1].bBox, ent))

        for shield in self.engine.entityMgr.shields:
            self.sQuadT.insert(self.getRect(shield.aspects[1].bBox, shield))

        for items in self.engine.entityMgr.pickups:
            self.sQuadT.insert(self.getRect(items.aspects[1].bBox,items))

    def makeDynamicQuadTree(self):
        rect = self.getRect(self.engine.gfxMgr.GBBOX)
        self.dQuadT = quadtree.QuadTree(0,rect)

        for enem in self.engine.entityMgr.enems:
            enem.aspects[1].updateBBox()
            self.dQuadT.insert(self.getRect(enem.aspects[1].bBox, enem))

    def getRect(self, bBox, ent = None):
        BTL, TTL, TTR, BTR, TBR, TBL, BBL, BBR = bBox.getAllCorners()
        return quadtree.Rect(BTL.x,BTL.z,abs(BTL.x-BBR.x),abs(BTL.z-BBL.z), bBox, ent)
        
    def tick(self,dtime):
        if not self.engine.gfxMgr.gameOver and not self.engine.gfxMgr.menuMode:
            self.makeDynamicQuadTree()
            self.checkCollisions(dtime)

    def stop(self):
        self.sQuadT.clear()
        self.dQuadT.clear()

    def game3(self,dtime):
        player = self.engine.entityMgr.player
        player2 = self.engine.entityMgr.player2

        if player == None or player2 == None:
            return
        
        pBBox = player.aspects[1].ogreEnt.getWorldBoundingBox(True)
        pRect = self.getRect(pBBox, player)
        objects1 = self.sQuadT.retrieve([],pRect)
        enems1 = self.dQuadT.retrieve([],pRect)

        p2BBox = player2.aspects[1].ogreEnt.getWorldBoundingBox(True)
        p2Rect = self.getRect(p2BBox, player2)
        objects2 = self.sQuadT.retrieve([],p2Rect) 
        enems2 = self.dQuadT.retrieve([],p2Rect)

        # player and player
        diff = player.pos - player2.pos
        squaredDistance = diff.squaredLength()
        if(squaredDistance <= player.proximity**2):
            player.pos-=player.vel*dtime
            player2.pos-=player2.vel*dtime

        # objects and player1
        for obj in objects1:
            sqDistance = self.squaredDistance(obj.bBox,player.pos)
            if sqDistance < obj.ent.proximity**2:
                player.pos-=player.vel*dtime

        # enemies:
        for i in range(len(enems1)):
            for j in range(i+1, len(enems1)):
                if enems1[j].bBox.intersects(enems1[i].bBox):
                    enems1[j].ent.pos -= enems1[j].ent.vel*dtime

            # enemy and static objects
            # it cannot include every possible enemies moving toward player
            eRect = self.getRect(enems1[i].bBox)
            objects2 = self.sQuadT.retrieve([],eRect)
            for obj2 in objects2:
                sqDistance = self.squaredDistance(obj2.bBox,enems1[i].ent.pos)
                if sqDistance < obj2.ent.proximity**2:
                    enems1[i].ent.pos-=enems1[i].ent.vel*dtime

            # enemy and player1
            if player.damage and player.timer == 0:
                player.health -= enems1[i].ent.power
                self.engine.gfxMgr.updateHeart(-0.5)
                self.engine.sndMgr.playplayer_ow()
                self.engine.sndMgr.playbot_attack()
                player.timer = 3
                if player.health <= 0:
                    player.death = True
                    print "Player1 Dead -- GAME OVER --"
                    self.engine.gfxMgr.winner = 2
                    self.engine.gfxMgr.gameOver = True

            diff = player.pos - enems1[i].ent.pos
            squaredDistance = diff.squaredLength()

            if squaredDistance <= enems1[i].ent.proximity**2:
                player.pos-=player.vel*dtime

        # bullets:
        if len(self.engine.entityMgr.bullets):
            #for bullet in self.engine.entityMgr.bullets:
            #    bullet.aspects[1].updateBBox()

            #bRect = self.getRect(self.engine.entityMgr.bullets[0].aspects[1].bBox)
            #enems = self.dQuadT.retrieve([],bRect)
            #objs = self.sQuadT.retrieve([],bRect)

            for bullet in self.engine.entityMgr.bullets:
                bullet.aspects[1].updateBBox()
                bRect = self.getRect(bullet.aspects[1].bBox)
                enems = self.dQuadT.retrieve([],bRect)
                objs = self.sQuadT.retrieve([],bRect)
                for obj in objs:
                    if obj.bBox.intersects(bullet.pos):
                        bullet.isGone = True

                if p2BBox.intersects(bullet.pos):
                    bullet.isGone = True
                    if player2.timer <= 0:
                        player2.damage = True
                        player2.health -= 200
                        self.engine.gfxMgr.updateHeart2(-1)
                        print "Player2 Health: "+str(player2.health)
                        player2.timer = 3
                        if player2.health <= 0:
                            player2.death = True
                            self.engine.gfxMgr.winner = 1
                            self.engine.gfxMgr.gameOver = True
                            print "Player2 Dead -- GAME OVER --"

                for enem in enems:
                    if not enem.ent.lockOn and not enem.ent.causion:
                        diff = bullet.pos - enem.ent.pos
                        squaredDistance = diff.squaredLength()
                        if squaredDistance <= enem.ent.sightDistance**2:
                            rad = math.atan2(-diff.z,(diff.x+0.000001))
                            enem.ent.desiredHeading = rad
                            enem.ent.causion = True

                    if enem.bBox.intersects(bullet.pos):
                        enem.ent.health -= bullet.power
                        self.engine.sndMgr.playeffect_boom2()
                        enem.ent.aspects[1].ogreEnt.setMaterialName("firetext")
                        player.score += 10

                        # death checking
                        if enem.ent.health <= 0:
                            enem.ent.death = True
                            self.engine.sndMgr.playbot_death()
                            player.score += enem.ent.point

                        botSound_num = random.randint(1,6)

                        self.counter = self.counter + dtime
                        soundEnabled = False

                        if self.counter > self.delay:
                            soundEnabled = True
                            self.counter = 0

                        if soundEnabled == True:
                            if botSound_num == 1:
                                self.engine.sndMgr.playbot_hug() #1 sec
                                self.delay = self.delay+.011
                                soundEnabled = False
                            elif botSound_num == 2:
                                self.engine.sndMgr.playbot_hurtme() #4 sec
                                self.delay = self.delay+.045
                                soundEnabled = False
                            elif botSound_num == 3:
                                self.engine.sndMgr.playbot_oh() #0.5 sec
                                self.delay = self.delay+.006
                                soundEnabled = False
                            elif botSound_num == 4:
                                self.engine.sndMgr.playbot_ow() #0.5 sec
                                self.delay = self.delay+.006
                                soundEnabled = False
                            elif botSound_num == 5:
                                self.engine.sndMgr.playbot_stop() #0.5 sec
                                self.delay = self.delay+.006
                                soundEnabled = False
                            elif botSound_num == 6:
                                self.engine.sndMgr.playbot_stop2() #0.5 sec
                                self.delay = self.delay+.006
                                soundEnabled = False

                        enem.ent.timer = 0.1
                        enem.ent.hit = True
                        bullet.isGone = True

        # player 2 ==================================================
        if len(self.engine.entityMgr.bullets2):
            
            #for bullet in self.engine.entityMgr.bullets2:
            #    bullet.aspects[1].updateBBox()

            #bRect = self.getRect(self.engine.entityMgr.bullets2[0].aspects[1].bBox)
            #enems = self.dQuadT.retrieve([],bRect)
            #objs = self.sQuadT.retrieve([],bRect)

            for bullet in self.engine.entityMgr.bullets2:
                bullet.aspects[1].updateBBox()
                bRect = self.getRect(bullet.aspects[1].bBox)
                enems = self.dQuadT.retrieve([],bRect)
                objs = self.sQuadT.retrieve([],bRect)
                for obj in objs:
                    if obj.bBox.intersects(bullet.pos):
                        bullet.isGone = True

                if pBBox.intersects(bullet.pos):
                    bullet.isGone = True
                    if player.timer <= 0:
                        player.damage = True
                        player.health -= 200
                        self.engine.gfxMgr.updateHeart(-1)
                        print "Player1 Health: "+str(player.health)
                        player.timer = 3
                        if player.health <= 0:
                            player.death = True
                            self.engine.gfxMgr.winner = 2
                            self.engine.gfxMgr.gameOver = True
                            print "Player1 Dead -- GAME OVER --"

                for enem in enems:
                    if not enem.ent.lockOn and not enem.ent.causion:
                        diff = bullet.pos - enem.ent.pos
                        squaredDistance = diff.squaredLength()
                        if squaredDistance <= enem.ent.sightDistance**2:
                            rad = math.atan2(-diff.z,(diff.x+0.000001))
                            enem.ent.desiredHeading = rad
                            enem.ent.causion = True

                    if enem.bBox.intersects(bullet.pos):
                        enem.ent.health -= bullet.power
                        self.engine.sndMgr.playeffect_boom2()
                        enem.ent.aspects[1].ogreEnt.setMaterialName("firetext")
                        player.score += 10

                        # death checking
                        if enem.ent.health <= 0:
                            enem.ent.death = True
                            self.engine.sndMgr.playbot_death()
                            player.score += enem.ent.point

                        botSound_num = random.randint(1,6)

                        self.counter = self.counter + dtime
                        soundEnabled = False

                        if self.counter > self.delay:
                            soundEnabled = True
                            self.counter = 0

                        if soundEnabled == True:
                            if botSound_num == 1:
                                self.engine.sndMgr.playbot_hug() #1 sec
                                self.delay = self.delay+.011
                                soundEnabled = False
                            elif botSound_num == 2:
                                self.engine.sndMgr.playbot_hurtme() #4 sec
                                self.delay = self.delay+.045
                                soundEnabled = False
                            elif botSound_num == 3:
                                self.engine.sndMgr.playbot_oh() #0.5 sec
                                self.delay = self.delay+.006
                                soundEnabled = False
                            elif botSound_num == 4:
                                self.engine.sndMgr.playbot_ow() #0.5 sec
                                self.delay = self.delay+.006
                                soundEnabled = False
                            elif botSound_num == 5:
                                self.engine.sndMgr.playbot_stop() #0.5 sec
                                self.delay = self.delay+.006
                                soundEnabled = False
                            elif botSound_num == 6:
                                self.engine.sndMgr.playbot_stop2() #0.5 sec
                                self.delay = self.delay+.006
                                soundEnabled = False

                        enem.ent.timer = 0.1
                        enem.ent.hit = True
                        bullet.isGone = True

        for obj in objects2:
            sqDistance = self.squaredDistance(obj.bBox,player2.pos)
            if sqDistance < obj.ent.proximity**2:
                player2.pos-=player2.vel*dtime

        for i in range(len(enems2)):
            for j in range(i+1, len(enems2)):
                if enems2[j].bBox.intersects(enems2[i].bBox):
                    enems2[j].ent.pos -= enems2[j].ent.vel*dtime

            # enemy and static objects
            # it cannot include every possible enemies moving toward player
            eRect = self.getRect(enems2[i].bBox)
            objects2 = self.sQuadT.retrieve([],eRect)
            for obj2 in objects2:
                sqDistance = self.squaredDistance(obj2.bBox,enems2[i].ent.pos)
                if sqDistance < obj2.ent.proximity**2:
                    enems2[i].ent.pos-=enems2[i].ent.vel*dtime

            # enemy and player
            if player2.damage and player2.timer == 0:
                player2.health -= enems2[i].ent.power
                self.engine.gfxMgr.updateHeart2(-0.5)
                self.engine.sndMgr.playplayer_ow()
                self.engine.sndMgr.playbot_attack()
                player2.timer = 3
                if player2.health <= 0:
                    player2.death = True
                    print "Player2 Dead -- GAME OVER --"
                    self.engine.gfxMgr.gameOver = True
                    self.engine.gfxMgr.winner = 1

            diff = player2.pos - enems2[i].ent.pos
            squaredDistance = diff.squaredLength()

            if squaredDistance <= enems2[i].ent.proximity**2:
                player2.pos-=player2.vel*dtime

    def checkCollisions(self,dtime):
        if self.engine.gfxMgr.game3:
            self.game3(dtime)
        else:
            self.game1(dtime)

    def game1(self,dtime):
        player = self.engine.entityMgr.player
        if player == None:
            return
        
        pBBox = player.aspects[1].ogreEnt.getWorldBoundingBox(True)
        pRect = self.getRect(pBBox, player)
        objects1 = self.sQuadT.retrieve([],pRect)
        enems = self.dQuadT.retrieve([],pRect)

        # player and static objects & bullet and static objects
        for obj in objects1:
            sqDistance = self.squaredDistance(obj.bBox,player.pos)
            if obj.ent.uiname == "shield":
                if obj.ent.shieldsOn:
                    if sqDistance < obj.ent.proximity**2:
                        player.pos-=player.vel*dtime
 
            elif obj.ent.mesh == 'shield.mesh':
                if obj.ent.death == False:
                    if sqDistance < obj.ent.proximity**2:
                        #player.pos-=player.vel*dtime
                        obj.ent.death = True
                        self.engine.gfxMgr.updateHeart(+1)
                        player.health += 200
                        self.engine.sndMgr.playhum()
 
            else:
                if sqDistance < obj.ent.proximity**2:
                    player.pos-=player.vel*dtime
 
                    if obj.ent.uiname == "alienship":
                        self.engine.gfxMgr.Victory = True
                        self.engine.sndMgr.playeffect_fanfare()
                        print "WIN"

            #for bullet in self.engine.entityMgr.bullets:
            #    bullet.aspects[1].updateBBox()
            #    if obj.bBox.intersects(bullet.pos):
            #            bullet.isGone = True

        if len(self.engine.entityMgr.bullets):
            #for bullet in self.engine.entityMgr.bullets:
           #     bullet.aspects[1].updateBBox()

            #bRect = self.getRect(self.engine.entityMgr.bullets[0].aspects[1].bBox)
            #enems = self.dQuadT.retrieve([],bRect)
            #objs = self.sQuadT.retrieve([],bRect)

            for bullet in self.engine.entityMgr.bullets:
                bullet.aspects[1].updateBBox()
                bRect = self.getRect(bullet.aspects[1].bBox)
                enems = self.dQuadT.retrieve([],bRect)
                objs = self.sQuadT.retrieve([],bRect)
                for obj in objs:
                    if obj.bBox.intersects(bullet.pos):
                        bullet.isGone = True

                for enem in enems:
                    if not enem.ent.lockOn and not enem.ent.causion:
                        diff = bullet.pos - enem.ent.pos
                        squaredDistance = diff.squaredLength()
                        if squaredDistance <= enem.ent.sightDistance**2:
                            rad = math.atan2(-diff.z,(diff.x+0.000001))
                            enem.ent.desiredHeading = rad
                            enem.ent.causion = True

                    if enem.bBox.intersects(bullet.pos):
                        enem.ent.health -= bullet.power
                        self.engine.sndMgr.playeffect_boom2()
                        enem.ent.aspects[1].ogreEnt.setMaterialName("firetext")
                        player.score += 10

                        # death checking
                        if enem.ent.health <= 0:
                            enem.ent.death = True
                            self.engine.sndMgr.playbot_death()
                            player.score += enem.ent.point

                        botSound_num = random.randint(1,6)

                        self.counter = self.counter + dtime
                        soundEnabled = False

                        if self.counter > self.delay:
                            soundEnabled = True
                            self.counter = 0

                        if soundEnabled == True:
                            if botSound_num == 1:
                                self.engine.sndMgr.playbot_hug() #1 sec
                                self.delay = self.delay+.011
                                soundEnabled = False
                            elif botSound_num == 2:
                                self.engine.sndMgr.playbot_hurtme() #4 sec
                                self.delay = self.delay+.045
                                soundEnabled = False
                            elif botSound_num == 3:
                                self.engine.sndMgr.playbot_oh() #0.5 sec
                                self.delay = self.delay+.006
                                soundEnabled = False
                            elif botSound_num == 4:
                                self.engine.sndMgr.playbot_ow() #0.5 sec
                                self.delay = self.delay+.006
                                soundEnabled = False
                            elif botSound_num == 5:
                                self.engine.sndMgr.playbot_stop() #0.5 sec
                                self.delay = self.delay+.006
                                soundEnabled = False
                            elif botSound_num == 6:
                                self.engine.sndMgr.playbot_stop2() #0.5 sec
                                self.delay = self.delay+.006
                                soundEnabled = False

                        enem.ent.timer = 0.1
                        enem.ent.hit = True
                        bullet.isGone = True

        for i in range(len(enems)):
            for j in range(i+1, len(enems)):
                if enems[j].bBox.intersects(enems[i].bBox):
                    enems[j].ent.pos -= enems[j].ent.vel*dtime

            # enemy and static objects
            # it cannot include every possible enemies moving toward player
            eRect = self.getRect(enems[i].bBox)
            objects2 = self.sQuadT.retrieve([],eRect)
            for obj2 in objects2:
                sqDistance = self.squaredDistance(obj2.bBox,enems[i].ent.pos)
                if sqDistance < obj2.ent.proximity**2:
                    enems[i].ent.pos-=enems[i].ent.vel*dtime

            # if enems[i].bBox.intersects(pBBox):
            #    player.pos-=player.vel*dtime

            # enemy and player
            if player.damage and player.timer == 0:
                player.health -= enems[i].ent.power
                self.engine.gfxMgr.updateHeart(-0.5)
                self.engine.sndMgr.playplayer_ow()
                #self.engine.sndMgr.playbot_kill()
                self.engine.sndMgr.playbot_attack()
                print player.health
                player.timer = 3
                #player.damage = True
                if player.health <= 0:
                    player.death = True
                    print "Player Dead -- GAME OVER --"
                    self.engine.gfxMgr.gameOver = True
                    #self.engine.sndMgr.playwaa()

            diff = player.pos - enems[i].ent.pos
            squaredDistance = diff.squaredLength()

            if squaredDistance <= enems[i].ent.proximity**2:
                player.pos-=player.vel*dtime

    def squaredDistance(self,box,v):
        if box.contains(v):
            return 0;
        else:
            maxDist = MyVector(0,0,0)

            if (v.x < box.getMinimum().x):
                maxDist.x = box.getMinimum().x - v.x;
            elif (v.x > box.getMaximum().x):
                maxDist.x = v.x - box.getMaximum().x;
            if (v.y < box.getMinimum().y):
                maxDist.y = box.getMinimum().y - v.y;
            elif (v.y > box.getMaximum().y):
                maxDist.y = v.y - box.getMaximum().y;
             
            if (v.z < box.getMinimum().z):
                maxDist.z = box.getMinimum().z - v.z;
            elif (v.z > box.getMaximum().z):
                maxDist.z = v.z - box.getMaximum().z;
            return maxDist.squaredLength();


                
