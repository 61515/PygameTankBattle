import pygame
# 坦克的普通子弹


class Bullet1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.rect = self.image_bullet_down.get_rect()
        # 速度,威力,方向,归属阵营
        self.speed = 8
        self.power = 1
        # 图像 即 方向
        self.image = None
        # 1 为我方阵营, 2 为敌方阵营
        self.owner = 1
        # 此刻是否处于被激活状态, 若是,则绘制子弹
        self.active = False

    def load_image(self):
        self.image_bullet_down = pygame.image.load("../Image/Bullet/bullet_down.png").convert_alpha()
        self.image_bullet_left = pygame.image.load("../Image/Bullet/bullet_left.png").convert_alpha()
        self.image_bullet_right = pygame.image.load("../Image/Bullet/bullet_right.png").convert_alpha()
        self.image_bullet_up = pygame.image.load("../Image/Bullet/bullet_up.png").convert_alpha()


class Bullet1_camp1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.rect = self.image_bullet_down.get_rect()
        # 速度,威力,方向,归属阵营
        self.speed = 8
        self.power = 1
        # 图像 即 方向
        self.image = None
        # 1 为我方阵营, 2 为敌方阵营
        self.owner = 1
        # 此刻是否处于被激活状态, 若是,则绘制子弹
        self.active = False

    def load_image(self):
        self.image_bullet_down = pygame.image.load("../Image/Bullet/bullet_camp1_down.png").convert_alpha()
        self.image_bullet_left = pygame.image.load("../Image/Bullet/bullet_camp1_left.png").convert_alpha()
        self.image_bullet_right = pygame.image.load("../Image/Bullet/bullet_camp1_right.png").convert_alpha()
        self.image_bullet_up = pygame.image.load("../Image/Bullet/bullet_camp1_up.png").convert_alpha()
