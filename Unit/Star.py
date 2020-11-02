import pygame


class Star_tank_generate:
    # 判断当前的初始星形图像是否显示完毕
    def is_completed(self):
        if self.image_play_continuously[self.play_index]:
            return False
        return True

    def __init__(self):
        self.load_image()
        self.rect = self.image_star0.get_rect()

        self.play_index = 0
        self.image_play_continuously = []
        times = 4
        for i in range(times):
            self.image_play_continuously.append(self.image_star0)
        for i in range(times):
            self.image_play_continuously.append(self.image_star1)
        for i in range(times):
            self.image_play_continuously.append(self.image_star2)
        for i in range(times):
            self.image_play_continuously.append(self.image_star3)
        self.image_play_continuously.append(None)

    def load_image(self):
        self.image_star0 = pygame.image.load("../Image/Star/star0.png").convert_alpha()
        self.image_star1 = pygame.image.load("../Image/Star/star1.png").convert_alpha()
        self.image_star2 = pygame.image.load("../Image/Star/star2.png").convert_alpha()
        self.image_star3 = pygame.image.load("../Image/Star/star3.png").convert_alpha()

    # 在屏幕的显示
    def display(self, screen):
        screen.blit(self.image_play_continuously[self.play_index], self.rect)
        self.play_index += 1
