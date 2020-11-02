import pygame
from pygame.locals import *
import sys
import time

from Scene.Scene_intermission import Scene_Intermission
from Scene.Scene_player1 import Scene_player1


class Starter:

    # pygame 初始化
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.bg_size = self.width, self.height = 32 * 32, 30 * 32
        self.screen = pygame.display.set_mode(self.bg_size)
        pygame.display.set_caption("坦克大战")
        self.clock = pygame.time.Clock()
        self.load_Audio()
        self.load_image()

    # 加载音频
    def load_Audio(self):
        self.game_bgm1 = pygame.mixer.Sound("../Audio/GameBgm1.wav")
        self.game_bgm1.set_volume(0.03)
        self.game_bgm2 = pygame.mixer.Sound("../Audio/GameBgm2.wav")
        self.game_bgm2.set_volume(0.03)
        self.game_bgm3 = pygame.mixer.Sound("../Audio/GameBgm3.wav")
        self.game_bgm3.set_volume(0.03)
        self.game_bgm4 = pygame.mixer.Sound("../Audio/GameBgm4.wav")
        self.game_bgm4.set_volume(0.03)

    # 加载图形
    def load_image(self):
        self.image_starter = pygame.image.load("../Image/Scene_0/tank_logo.png")
        self.image_player1_0_right1 = pygame.image.load("../Image/Player1_Tank/player1_0_right1.png")
        self.image_player1_0_right2 = pygame.image.load("../Image/Player1_Tank/player1_0_right2.png")

    # x帧执行一次,若执行,返回true
    def do_delay(self, x):
        if self.delay % x == 0:
            return 1
        else:
            return 0

    def event_loop(self):
        # 控制几帧改变一次图像
        self.delay = 0
        self.game_bgms = [self.game_bgm1, self.game_bgm2, self.game_bgm1, self.game_bgm4]
        sound_index = 0
        self.game_bgms[sound_index].play(-1)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        i = 0
                        while True:
                            scene_intermission = Scene_Intermission()
                            i = scene_intermission.event_loop(i)
                            scene_player1 = Scene_player1(i)
                            if not scene_player1.event_loop():
                                break
                            else:
                                # 换背景音乐
                                self.game_bgms[sound_index].stop()
                                sound_index += 1
                                sound_index %= 4
                                self.game_bgms[sound_index].play(-1)
                            i += 1
                            i %= 35

            self.screen.fill([0, 0, 0])
            self.screen.blit(self.image_starter, (0, 0))
            if self.do_delay(2):
                self.screen.blit(self.image_player1_0_right1, (270, 480))
            else:
                self.screen.blit(self.image_player1_0_right2, (270, 480))
            pygame.display.flip()
            self.clock.tick(20)

            self.delay += 1
            self.delay %= 100
