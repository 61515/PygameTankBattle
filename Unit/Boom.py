import pygame


class Boom_small:

    def __init__(self):
        self.load_image()
        self.rect = self.image_boom0.get_rect()

        self.play_index = 0
        self.image_play_continuously = [self.image_boom0, self.image_boom1, None]

    def load_image(self):
        self.image_boom0 = pygame.image.load("../Image/Boom/boom0.png").convert_alpha()
        self.image_boom1 = pygame.image.load("../Image/Boom/boom1.png").convert_alpha()

    # 在屏幕的显示
    def display(self, screen):
        screen.blit(self.image_play_continuously[self.play_index], self.rect)
        self.play_index += 1


class Tank_boom:
    def __init__(self):
        self.load_image()
        self.rect = self.image_boom0.get_rect()

        self.play_index = 0
        self.image_play_continuously = [self.image_boom0, self.image_boom1, self.image_boom2,
                                        self.image_boom3, self.image_boom4, self.image_boom0, None]

    def load_image(self):
        self.image_boom0 = pygame.image.load("../Image/Boom/boom0.png").convert_alpha()
        self.image_boom1 = pygame.image.load("../Image/Boom/boom1.png").convert_alpha()
        self.image_boom2 = pygame.image.load("../Image/Boom/boom2.png").convert_alpha()
        self.image_boom3 = pygame.image.load("../Image/Boom/boom3.png").convert_alpha()
        self.image_boom4 = pygame.image.load("../Image/Boom/boom4.png").convert_alpha()

    # 在屏幕的显示
    def display(self, screen):
        screen.blit(self.image_play_continuously[self.play_index], self.rect)
        self.play_index += 1
