import pygame


class Enemy_mark(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.rect = self.image.get_rect()

    def load_image(self):
        self.image = pygame.image.load("../Image/Mark/enemy_mark.png").convert_alpha()

    def display(self, screen):
        screen.blit(self.image, self.rect)


class Player_mark(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.rect = self.image.get_rect()

    def load_image(self):
        self.image = pygame.image.load("../Image/Mark/player_mark.png").convert_alpha()

    def display(self, screen):
        screen.blit(self.image, self.rect)


class Flag(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.rect = self.image.get_rect()

    def load_image(self):
        self.image = pygame.image.load("../Image/Mark/flag.png").convert_alpha()

    def display(self, screen):
        screen.blit(self.image, self.rect)
