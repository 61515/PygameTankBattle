import pygame
# 地雷


class Mine(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.rect = self.image_mine.get_rect()
        # 1 为我方阵营, 2 为敌方阵营
        self.owner = 1
        # 此刻是否处于被激活状态, 若是,则绘制子弹
        self.active = False

    def load_image(self):
        self.image_mine = pygame.image.load("../Image/Tools/mine.png").convert_alpha()
