import pygame
from pygame.locals import *

class SndMgr:

    def __init__(self, engine):
        self.engine = engine

    def init(self):
        pygame.init()
        self.playMenubgm()
        self.bullet_sound = pygame.mixer.Sound("media/sounds/pewbot.wav")
        self.bullet_sound.set_volume(0.3)
        self.bloop_sound = pygame.mixer.Sound("media/sounds/bloop.wav")
        self.walk_sound = pygame.mixer.Sound("media/sounds/walk2.wav")

        self.bot_attack = pygame.mixer.Sound("media/sounds/bot_kill2.wav")   
        self.bot_death = pygame.mixer.Sound("media/sounds/bot_death.wav")
        self.bot_hug = pygame.mixer.Sound("media/sounds/bot_hug.wav")
        self.bot_hurtme = pygame.mixer.Sound("media/sounds/bot_hurtme.wav")
        self.bot_kill = pygame.mixer.Sound("media/sounds/bot_kill.wav")
        self.bot_oh = pygame.mixer.Sound("media/sounds/bot_oh.wav")
        self.bot_ow = pygame.mixer.Sound("media/sounds/bot_ow.wav")
        self.bot_stop = pygame.mixer.Sound("media/sounds/bot_stop.wav")
        self.bot_stop2 = pygame.mixer.Sound("media/sounds/bot_stop2.wav")
        self.bot_walk_sound = pygame.mixer.Sound("media/sounds/ching.wav")   

        self.effect_boom2 = pygame.mixer.Sound("media/sounds/effect_boom2.wav")
        self.effect_fanfare = pygame.mixer.Sound("media/sounds/effect_fanfare.wav")

        self.effect_hum = pygame.mixer.Sound("media/sounds/hum.wav")

        self.player_ow = pygame.mixer.Sound("media/sounds/player_ow.wav")

    def tick(self, dtime):
        pass

    def stop(self):
        pass

    def playMenubgm(self):
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.load("media/sounds/party.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(.5)

    def playBullet(self):
        self.bullet_sound.play()
        pass

    def playbgm2(self):
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.load("media/sounds/Drumrun.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

    def playhum(self):
        self.effect_hum.play()
        
        

    def playwaa(self):
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.load("media/sounds/waa_waa.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def playwalk(self):
        self.walk_sound.play()
        self.walk_sound.set_volume(2)
        
    def playbloop(self):
        self.bloop_sound.set_volume(0.2)
        self.bloop_sound.play()

    def playbot_attack(self):
        self.bot_attack.set_volume(1)
        self.bot_attack.play()

    def playbot_walk(self):
        self.bot_walk_sound.set_volume(1)
        self.bot_walk_sound.play()

    def playbot_death(self):
        self.bot_death.set_volume(1)
        self.bot_death.play()

    def playbot_hug(self):
        self.bot_hug.set_volume(1)
        self.bot_hug.play()

    def playbot_hurtme(self):
        self.bot_hurtme.set_volume(1)
        self.bot_hurtme.play()

    def playbot_kill(self):
        self.bot_kill.set_volume(0.4)
        self.bot_kill.play()

    def playbot_oh(self):
        self.bot_oh.set_volume(1)
        self.bot_oh.play()

    def playbot_ow(self):
        self.bot_ow.set_volume(1)
        self.bot_ow.play()

    def playbot_stop(self):
        self.bot_stop.set_volume(1)
        self.bot_stop.play()

    def playbot_stop2(self):
        self.bot_stop2.set_volume(1)
        self.bot_stop2.play()

    def playeffect_boom2(self):
        self.effect_boom2.set_volume(.8)
        self.effect_boom2.play()

    def playeffect_fanfare(self):
        self.effect_boom2.set_volume(1)
        self.effect_fanfare.play()

    def playplayer_ow(self):
        self.player_ow.set_volume(.5)
        self.player_ow.play()
