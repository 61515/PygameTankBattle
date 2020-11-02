import pygame


# 随机生成道具
class Armor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.rect = self.image.get_rect()
        self.show = 1

    def load_image(self):
        self.image = pygame.image.load("../Image/Tools/Armor.png").convert_alpha()

    def display(self, screen, delay):
        if delay % 8 == 0:
            self.show ^= 1

        if self.show:
            screen.blit(self.image, self.rect)


class Explode(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.rect = self.image.get_rect()
        self.show = 1

    def load_image(self):
        self.image = pygame.image.load("../Image/Tools/explode.png").convert_alpha()

    def display(self, screen, delay):
        if delay % 8 == 0:
            self.show ^= 1

        if self.show:
            screen.blit(self.image, self.rect)


class Gun(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.rect = self.image.get_rect()
        self.show = 1

    def load_image(self):
        self.image = pygame.image.load("../Image/Tools/gun.png").convert_alpha()

    def display(self, screen, delay):
        if delay % 8 == 0:
            self.show ^= 1

        if self.show:
            screen.blit(self.image, self.rect)


class Star(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.rect = self.image.get_rect()
        self.show = 1

    def load_image(self):
        self.image = pygame.image.load("../Image/Tools/star.png").convert_alpha()

    def display(self, screen, delay):
        if delay % 8 == 0:
            self.show ^= 1

        if self.show:
            screen.blit(self.image, self.rect)


class Timer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.rect = self.image.get_rect()
        self.show = 1

    def load_image(self):
        self.image = pygame.image.load("../Image/Tools/timer.png").convert_alpha()

    def display(self, screen, delay):
        if delay % 8 == 0:
            self.show ^= 1

        if self.show:
            screen.blit(self.image, self.rect)
