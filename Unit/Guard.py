import pygame


class Guard_tank_generate:

    def is_invincible(self):
        if self.all_frame > 0:
            return True
        return False

    def __init__(self):
        self.load_image()
        self.all_frame = 60
        self.rect = self.image_guard.get_rect()

    def load_image(self):
        self.image_guard = pygame.image.load("../Image/Tools/guard.png").convert_alpha()

    # 在屏幕的显示
    def display(self, screen):
        if self.all_frame > 0:
            screen.blit(self.image_guard, self.rect)
            self.all_frame -= 1
