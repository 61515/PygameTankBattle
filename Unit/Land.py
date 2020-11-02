import pygame
import random

from Unit.Tank.Tank_missile import Missile1_camp1


class Blank(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.rect = self.image_black_32.get_rect()

    def load_image(self):
        self.image_black_32 = pygame.image.load("../Image/Land/black_32.png").convert_alpha()

    def display(self, screen):
        screen.blit(self.image_black_32, self.rect)


class Blank_16(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.rect = self.image_black_16.get_rect()

    def load_image(self):
        self.image_black_16 = pygame.image.load("../Image/Land/black_16.png").convert_alpha()

    def display(self, screen):
        screen.blit(self.image_black_16, self.rect)


class Border(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.rect = self.image_border.get_rect()

    def load_image(self):
        self.image_border = pygame.image.load("../Image/Land/border.png").convert_alpha()

    def display(self, screen):
        screen.blit(self.image_border, self.rect)


class Ice(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.rect = self.image_ice.get_rect()

    def load_image(self):
        self.image_ice = pygame.image.load("../Image/Land/ice.png").convert_alpha()

    def display(self, screen):
        screen.blit(self.image_ice, self.rect)


class Iron(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.rect = self.image_iron.get_rect()
        self.state = 1

    def load_image(self):
        self.image_iron = pygame.image.load("../Image/Land/iron.png").convert_alpha()

    def display(self, screen):
        if self.state == 1:
            screen.blit(self.image_iron, self.rect)


class Jungle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.rect = self.image_jungle.get_rect()

    def load_image(self):
        self.image_jungle = pygame.image.load("../Image/Land/jungle.png").convert_alpha()

    def display(self, screen):
        screen.blit(self.image_jungle, self.rect)


class Sea(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.rect = self.image_sea0.get_rect()

    def load_image(self):
        self.image_sea0 = pygame.image.load("../Image/Land/sea0.png").convert_alpha()
        self.image_sea1 = pygame.image.load("../Image/Land/sea1.png").convert_alpha()
        self.image = self.image_sea0

    def display(self, screen, delay):
        if delay % 10 == 0:
            if self.image == self.image_sea0:
                self.image = self.image_sea1
            else:
                self.image = self.image_sea0
        screen.blit(self.image, self.rect)


class Wall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.rect = self.image_wall.get_rect()
        self.black_rect = self.image_black_16.get_rect()
        self.state = 16

    def load_image(self):
        self.image_wall = pygame.image.load("../Image/Land/wall.png").convert_alpha()
        self.image_black_16 = pygame.image.load("../Image/Land/black_16.png").convert_alpha()

    def display(self, screen):
        screen.blit(self.image_wall, self.rect)

        # 左上
        if (self.state & 1) == 0:
            self.black_rect.left, self.black_rect.top = self.rect.left, self.rect.top
            screen.blit(self.image_black_16, self.black_rect)

        # 右上
        if (self.state & 2) == 0:
            self.black_rect.left, self.black_rect.top = self.rect.centerx, self.rect.top
            screen.blit(self.image_black_16, self.black_rect)

        # 左下
        if (self.state & 4) == 0:
            self.black_rect.left, self.black_rect.top = self.rect.left, self.rect.centery
            screen.blit(self.image_black_16, self.black_rect)

        # 右下
        if (self.state & 8) == 0:
            self.black_rect.left, self.black_rect.top = self.rect.centerx, self.rect.centery
            screen.blit(self.image_black_16, self.black_rect)


class Commander(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.rect = self.image_commander0.get_rect()
        self.image = self.image_commander0
        self.enable = False

        # 生成自己的导弹
        self.generate_missile()
        # 自己的血量
        self.hp = 30
        self.sum_hp = 30

    def load_image(self):
        self.image_commander0 = pygame.image.load("../Image/Home/commander0.png").convert_alpha()
        self.image_commander1 = pygame.image.load("../Image/Home/commander1.png").convert_alpha()
        self.image_black_32 = pygame.image.load("../Image/Land/black_32.png").convert_alpha()

    def display(self, screen):
        screen.blit(self.image, self.rect)
        for missile in self.missiles:
            if missile.active:
                screen.blit(missile.image, missile.rect)

    def generate_missile(self):
        self.missiles = [Missile1_camp1(), Missile1_camp1()]

    def fire_missile(self):
        rd_direction = [1, 1, 1, 2, 3, 1, 2, 3, 1, 1]
        for missile in self.missiles:
            if not missile.active:
                rd = random.choice(rd_direction)
                if rd == 1:
                    missile.image = missile.image_bullet_up
                    missile.rect.left = self.rect.left + self.rect.width // 2 - 14
                    missile.rect.top = self.rect.top
                elif rd == 2:
                    missile.image = missile.image_bullet_left
                    missile.rect.left = self.rect.left
                    missile.rect.top = self.rect.top + self.rect.height // 2 - 14
                elif rd == 3:
                    missile.image = missile.image_bullet_right
                    missile.rect.left = self.rect.left + self.rect.width
                    missile.rect.top = self.rect.top + self.rect.height // 2 - 14
                missile.active = True
