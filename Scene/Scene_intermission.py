import pygame
from pygame.locals import *
import sys


class Scene_Intermission:

    # pygame 初始化
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.bg_size = self.width, self.height = 32 * 32, 30 * 32
        self.screen = pygame.display.set_mode(self.bg_size)
        pygame.display.set_caption("坦克大战")
        self.clock = pygame.time.Clock()
        self.load_image()

    def event_loop(self, stage):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return stage
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        stage += 1
                        stage %= 35
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        stage -= 1
                        stage %= 35

            self.screen.blit(self.image_Intermission, (0, 0))
            my_font = pygame.font.SysFont('arial', 60)
            text_surface = my_font.render('stage  ' + str(stage + 1), True, (0, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.center = (500, 265)
            self.screen.blit(text_surface, text_rect)
            pygame.display.flip()
            self.clock.tick(20)

    def load_image(self):
        self.image_Intermission = pygame.image.load("../Image/Scene_0/Intermission.png")