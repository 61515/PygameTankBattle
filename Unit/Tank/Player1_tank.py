import pygame

from Unit.Guard import Guard_tank_generate
from Unit.Star import Star_tank_generate
from Unit.Tank.Tank_bullet import Bullet1_camp1
from Unit.Coordinate import Coordinate
from Unit.Tank.Tank_mine import Mine
from Unit.Tank.Tank_missile import Missile1_camp1


# # slight 坦克
# class Player_Tank_0(pygame.sprite.Sprite):
#     # 单例模式
#     try_move_tank = None
#
#     def __init__(self):
#         pygame.sprite.Sprite.__init__(self)
#         self.load_image()
#         self.cache_image = self.image_player1_0_up1, self.image_player1_0_up2
#         self.delayed = 0
#         self.rect = self.cache_image[0].get_rect()
#         self.rect.left, self.rect.top = Coordinate.xy_to_left_top_pixel(26, 11)
#         self.speed = 8
#         self.life = 2
#         # 生成自己的子弹
#         self.generate_bullet()
#
#     # 重置当前坦克
#     def re_set(self):
#         self.cache_image = self.image_player1_0_up1, self.image_player1_0_up2
#         self.rect = self.cache_image[0].get_rect()
#         self.rect.left, self.rect.top = Coordinate.xy_to_left_top_pixel(26, 11)
#         self.speed = 8
#
#     # 轻型坦克有 1 发子弹
#     def generate_bullet(self):
#         self.bullets = [Bullet1()]
#
#     # 发射子弹
#     def fire_bullet(self):
#         for bullet in self.bullets:
#             if bullet.active == 0:
#                 # 子弹初始化
#                 bullet.active = 1
#                 if self.image_player1_0_up1 in self.cache_image:
#                     bullet.image = bullet.image_bullet_up
#                     bullet.rect.left = self.rect.left + self.rect.width // 2 - 10
#                     bullet.rect.top = self.rect.top
#                 elif self.image_player1_0_down1 in self.cache_image:
#                     bullet.image = bullet.image_bullet_down
#                     bullet.rect.left = self.rect.left + self.rect.width // 2 - 10
#                     bullet.rect.top = self.rect.top + self.rect.height
#                 elif self.image_player1_0_left1 in self.cache_image:
#                     bullet.image = bullet.image_bullet_left
#                     bullet.rect.left = self.rect.left
#                     bullet.rect.top = self.rect.top + self.rect.height // 2 - 10
#                 elif self.image_player1_0_right1 in self.cache_image:
#                     bullet.image = bullet.image_bullet_right
#                     bullet.rect.left = self.rect.left + self.rect.width
#                     bullet.rect.top = self.rect.top + self.rect.height // 2 - 10
#                 break
#
#     # 在屏幕的显示
#     def display(self, screen, delay):
#         if delay % 2 == 0:
#             self.delayed ^= 1
#         screen.blit(self.cache_image[self.delayed], self.rect)
#         # 显示子弹
#         for bullet in self.bullets:
#             if bullet.active == 1:
#                 screen.blit(bullet.image, bullet.rect)
#
#     def load_image(self):
#         # 下图
#         self.image_player1_0_down1 = pygame.image.load("../Image/Player1_Tank/player1_0_down1.png").convert_alpha()
#         self.image_player1_0_down2 = pygame.image.load("../Image/Player1_Tank/player1_0_down2.png").convert_alpha()
#         # 左图
#         self.image_player1_0_left1 = pygame.image.load("../Image/Player1_Tank/player1_0_left1.png").convert_alpha()
#         self.image_player1_0_left2 = pygame.image.load("../Image/Player1_Tank/player1_0_left2.png").convert_alpha()
#         # 右图
#         self.image_player1_0_right1 = pygame.image.load("../Image/Player1_Tank/player1_0_right1.png").convert_alpha()
#         self.image_player1_0_right2 = pygame.image.load("../Image/Player1_Tank/player1_0_right2.png").convert_alpha()
#         # 上图
#         self.image_player1_0_up1 = pygame.image.load("../Image/Player1_Tank/player1_0_up1.png").convert_alpha()
#         self.image_player1_0_up2 = pygame.image.load("../Image/Player1_Tank/player1_0_up2.png").convert_alpha()
#
#     def get_try_move_tank(self):
#         if Player_Tank_2.try_move_tank is None:
#             Player_Tank_2.try_move_tank = Player_Tank_2()
#         try_move_tank = Player_Tank_2.try_move_tank
#         try_move_tank.rect.left = self.rect.left
#         try_move_tank.rect.top = self.rect.top
#         try_move_tank.speed = self.speed
#         return try_move_tank
#
#     # 返回一个深拷贝的对象
#     def try_moveUp(self):
#         self.cache_image = self.image_player1_0_up1, self.image_player1_0_up2
#         try_move_tank = self.get_try_move_tank()
#         try_move_tank.moveUp()
#         return try_move_tank
#
#     def try_moveDown(self):
#         self.cache_image = self.image_player1_0_down1, self.image_player1_0_down2
#         try_move_tank = self.get_try_move_tank()
#         try_move_tank.moveDown()
#         return try_move_tank
#
#     def try_moveLeft(self):
#         self.cache_image = self.image_player1_0_left1, self.image_player1_0_left2
#         try_move_tank = self.get_try_move_tank()
#         try_move_tank.moveLeft()
#         return try_move_tank
#
#     def try_moveRight(self):
#         self.cache_image = self.image_player1_0_right1, self.image_player1_0_right2
#         try_move_tank = self.get_try_move_tank()
#         try_move_tank.moveRight()
#         return try_move_tank
#
#     def moveUp(self):
#         self.rect.top -= self.speed
#
#     def moveDown(self):
#         self.rect.top += self.speed
#
#     def moveLeft(self):
#         self.rect.left -= self.speed
#
#     def moveRight(self):
#         self.rect.left += self.speed
#
#
# # Midium 坦克
# class Player_Tank_1(pygame.sprite.Sprite):
#     # 单例模式
#     try_move_tank = None
#
#     def __init__(self):
#         pygame.sprite.Sprite.__init__(self)
#         self.load_image()
#         self.cache_image = self.image_player1_1_up1, self.image_player1_1_up2
#         self.delayed = 0
#         self.rect = self.cache_image[0].get_rect()
#         self.rect.left, self.rect.top = Coordinate.xy_to_left_top_pixel(26, 11)
#         self.speed = 8
#         self.life = 2
#         # 生成自己的子弹
#         self.generate_bullet()
#
#     # 重置当前坦克
#     def re_set(self):
#         self.cache_image = self.image_player1_1_up1, self.image_player1_1_up2
#         self.rect = self.cache_image[0].get_rect()
#         self.rect.left, self.rect.top = Coordinate.xy_to_left_top_pixel(26, 11)
#         self.speed = 8
#
#     # 中型坦克有 1 发子弹
#     def generate_bullet(self):
#         self.bullets = [Bullet1()]
#
#     # 发射子弹
#     def fire_bullet(self):
#         for bullet in self.bullets:
#             if bullet.active == 0:
#                 # 子弹初始化
#                 bullet.active = 1
#                 if self.image_player1_1_up1 in self.cache_image:
#                     bullet.image = bullet.image_bullet_up
#                     bullet.rect.left = self.rect.left + self.rect.width // 2 - 10
#                     bullet.rect.top = self.rect.top
#                 elif self.image_player1_1_down1 in self.cache_image:
#                     bullet.image = bullet.image_bullet_down
#                     bullet.rect.left = self.rect.left + self.rect.width // 2 - 10
#                     bullet.rect.top = self.rect.top + self.rect.height
#                 elif self.image_player1_1_left1 in self.cache_image:
#                     bullet.image = bullet.image_bullet_left
#                     bullet.rect.left = self.rect.left
#                     bullet.rect.top = self.rect.top + self.rect.height // 2 - 10
#                 elif self.image_player1_1_right1 in self.cache_image:
#                     bullet.image = bullet.image_bullet_right
#                     bullet.rect.left = self.rect.left + self.rect.width
#                     bullet.rect.top = self.rect.top + self.rect.height // 2 - 10
#                 break
#
#     # 在屏幕的显示
#     def display(self, screen, delay):
#         if delay % 2 == 0:
#             self.delayed ^= 1
#         screen.blit(self.cache_image[self.delayed], self.rect)
#         # 显示子弹
#         for bullet in self.bullets:
#             if bullet.active == 1:
#                 screen.blit(bullet.image, bullet.rect)
#
#     def load_image(self):
#         # 下图
#         self.image_player1_1_down1 = pygame.image.load("../Image/Player1_Tank/player1_1_down1.png").convert_alpha()
#         self.image_player1_1_down2 = pygame.image.load("../Image/Player1_Tank/player1_1_down2.png").convert_alpha()
#         # 左图
#         self.image_player1_1_left1 = pygame.image.load("../Image/Player1_Tank/player1_1_left1.png").convert_alpha()
#         self.image_player1_1_left2 = pygame.image.load("../Image/Player1_Tank/player1_1_left2.png").convert_alpha()
#         # 右图
#         self.image_player1_1_right1 = pygame.image.load("../Image/Player1_Tank/player1_1_right1.png").convert_alpha()
#         self.image_player1_1_right2 = pygame.image.load("../Image/Player1_Tank/player1_1_right2.png").convert_alpha()
#         # 上图
#         self.image_player1_1_up1 = pygame.image.load("../Image/Player1_Tank/player1_1_up1.png").convert_alpha()
#         self.image_player1_1_up2 = pygame.image.load("../Image/Player1_Tank/player1_1_up2.png").convert_alpha()
#
#     def get_try_move_tank(self):
#         if Player_Tank_2.try_move_tank is None:
#             Player_Tank_2.try_move_tank = Player_Tank_2()
#         try_move_tank = Player_Tank_2.try_move_tank
#         try_move_tank.rect.left = self.rect.left
#         try_move_tank.rect.top = self.rect.top
#         try_move_tank.speed = self.speed
#         return try_move_tank
#
#     # 返回一个深拷贝的对象
#     def try_moveUp(self):
#         self.cache_image = self.image_player1_1_up1, self.image_player1_1_up2
#         try_move_tank = self.get_try_move_tank()
#         try_move_tank.moveUp()
#         return try_move_tank
#
#     def try_moveDown(self):
#         self.cache_image = self.image_player1_1_down1, self.image_player1_1_down2
#         try_move_tank = self.get_try_move_tank()
#         try_move_tank.moveDown()
#         return try_move_tank
#
#     def try_moveLeft(self):
#         self.cache_image = self.image_player1_1_left1, self.image_player1_1_left2
#         try_move_tank = self.get_try_move_tank()
#         try_move_tank.moveLeft()
#         return try_move_tank
#
#     def try_moveRight(self):
#         self.cache_image = self.image_player1_1_right1, self.image_player1_1_right2
#         try_move_tank = self.get_try_move_tank()
#         try_move_tank.moveRight()
#         return try_move_tank
#
#     def moveUp(self):
#         self.rect.top -= self.speed
#
#     def moveDown(self):
#         self.rect.top += self.speed
#
#     def moveLeft(self):
#         self.rect.left -= self.speed
#
#     def moveRight(self):
#         self.rect.left += self.speed
#

# Height 坦克


class Player_Tank_2(pygame.sprite.Sprite):
    # 单例模式
    try_move_tank = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.cache_image = self.image_player1_2_up1, self.image_player1_2_up2
        self.delayed = 0
        self.rect = self.cache_image[0].get_rect()
        self.rect.left, self.rect.top = Coordinate.xy_to_left_top_pixel(26, 11)
        self.speed = 4
        self.life = 10
        # 生成自己的子弹
        self.generate_bullet()
        # 生成自己的导弹
        self.generate_missile()
        # 生成自己的地雷
        self.generate_mine()
        # 产生 防护罩
        self.generate_guard()
        # 产生 星形图像
        self.star_initial = Star_tank_generate()
        self.star_initial.rect.center = self.rect.center
        # 自己的血量
        self.hp = 3
        self.sum_hp = 3

    # 重置当前坦克
    def re_set(self):
        self.cache_image = self.image_player1_2_up1, self.image_player1_2_up2
        self.rect = self.cache_image[0].get_rect()
        self.rect.left, self.rect.top = Coordinate.xy_to_left_top_pixel(26, 11)
        self.speed = 4
        self.star_initial = Star_tank_generate()
        self.star_initial.rect.center = self.rect.center
        # 产生 防护罩
        self.generate_guard()
        self.hp = 3

    # 重型坦克有 2 发子弹
    def generate_bullet(self):
        self.bullets = [Bullet1_camp1(), Bullet1_camp1()]
        for bullet in self.bullets:
            bullet.power = 2
            bullet.speed = 12

    # 发射子弹
    def fire_bullet(self):
        all_bullets = pygame.sprite.Group()
        for bullet in self.bullets:
            if not bullet.active:
                # 子弹初始化
                if self.image_player1_2_up1 in self.cache_image:
                    bullet.image = bullet.image_bullet_up
                    bullet.rect.left = self.rect.left + self.rect.width // 2 - 10
                    bullet.rect.top = self.rect.top
                elif self.image_player1_2_down1 in self.cache_image:
                    bullet.image = bullet.image_bullet_down
                    bullet.rect.left = self.rect.left + self.rect.width // 2 - 10
                    bullet.rect.top = self.rect.top + self.rect.height
                elif self.image_player1_2_left1 in self.cache_image:
                    bullet.image = bullet.image_bullet_left
                    bullet.rect.left = self.rect.left
                    bullet.rect.top = self.rect.top + self.rect.height // 2 - 10
                elif self.image_player1_2_right1 in self.cache_image:
                    bullet.image = bullet.image_bullet_right
                    bullet.rect.left = self.rect.left + self.rect.width
                    bullet.rect.top = self.rect.top + self.rect.height // 2 - 10
                # 当前生成的子弹不和前面的子弹有碰撞
                if len(pygame.sprite.spritecollide(bullet, all_bullets, False)) == 0:
                    bullet.active = True
                    return True
                break
            else:
                all_bullets.add(bullet)
        return False

    def generate_missile(self):
        self.missiles = [Missile1_camp1()]

    def fire_missile(self):
        for missile in self.missiles:
            if not missile.active:
                if self.image_player1_2_up1 in self.cache_image:
                    missile.image = missile.image_bullet_up
                    missile.rect.left = self.rect.left + self.rect.width // 2 - 14
                    missile.rect.top = self.rect.top
                elif self.image_player1_2_down1 in self.cache_image:
                    missile.image = missile.image_bullet_down
                    missile.rect.left = self.rect.left + self.rect.width // 2 - 14
                    missile.rect.top = self.rect.top + self.rect.height
                elif self.image_player1_2_left1 in self.cache_image:
                    missile.image = missile.image_bullet_left
                    missile.rect.left = self.rect.left
                    missile.rect.top = self.rect.top + self.rect.height // 2 - 14
                elif self.image_player1_2_right1 in self.cache_image:
                    missile.image = missile.image_bullet_right
                    missile.rect.left = self.rect.left + self.rect.width
                    missile.rect.top = self.rect.top + self.rect.height // 2 - 14
                missile.active = True
                return True
        return False

    def generate_mine(self):
        self.mines = [Mine(), Mine(), Mine()]

    def fire_mine(self):
        # 不会和原来的 地雷重合
        all_mines = pygame.sprite.Group()
        for mine in self.mines:
            if mine.active:
                all_mines.add(mine)

        for mine in self.mines:
            if not mine.active:
                mine.rect.center = self.rect.center
                if len(pygame.sprite.spritecollide(mine, all_mines, False)) == 0:
                    mine.active = True
                break

    def generate_guard(self):
        self.guard = Guard_tank_generate()

    # 坦克最初的星型 显示
    def display_star(self, screen):
        self.star_initial.display(screen)

    # 在屏幕的显示
    def display(self, screen, delay):
        # 显示地雷
        for mine in self.mines:
            if mine.active:
                screen.blit(mine.image_mine, mine.rect)

        self.guard.rect.center = self.rect.center
        self.guard.display(screen)

        if self.star_initial.is_completed() is False:
            self.display_star(screen)
            return

        if delay % 2 == 0:
            self.delayed ^= 1
        screen.blit(self.cache_image[self.delayed], self.rect)
        # 显示子弹
        for bullet in self.bullets:
            if bullet.active:
                screen.blit(bullet.image, bullet.rect)
        # 显示导弹
        for missile in self.missiles:
            if missile.active:
                screen.blit(missile.image, missile.rect)

    def load_image(self):
        # 下图
        self.image_player1_2_down1 = pygame.image.load("../Image/Player1_Tank/player1_2_down1.png").convert_alpha()
        self.image_player1_2_down2 = pygame.image.load("../Image/Player1_Tank/player1_2_down2.png").convert_alpha()
        # 左图
        self.image_player1_2_left1 = pygame.image.load("../Image/Player1_Tank/player1_2_left1.png").convert_alpha()
        self.image_player1_2_left2 = pygame.image.load("../Image/Player1_Tank/player1_2_left2.png").convert_alpha()
        # 右图
        self.image_player1_2_right1 = pygame.image.load("../Image/Player1_Tank/player1_2_right1.png").convert_alpha()
        self.image_player1_2_right2 = pygame.image.load("../Image/Player1_Tank/player1_2_right2.png").convert_alpha()
        # 上图
        self.image_player1_2_up1 = pygame.image.load("../Image/Player1_Tank/player1_2_up1.png").convert_alpha()
        self.image_player1_2_up2 = pygame.image.load("../Image/Player1_Tank/player1_2_up2.png").convert_alpha()

    def get_try_move_tank(self):
        if Player_Tank_2.try_move_tank is None:
            Player_Tank_2.try_move_tank = Player_Tank_2()
        try_move_tank = Player_Tank_2.try_move_tank
        try_move_tank.rect.left = self.rect.left
        try_move_tank.rect.top = self.rect.top
        try_move_tank.speed = self.speed
        return try_move_tank

    # 返回一个深拷贝的对象
    def try_moveUp(self, is_change_direction=True):
        if is_change_direction:
            self.cache_image = self.image_player1_2_up1, self.image_player1_2_up2

        try_move_tank = self.get_try_move_tank()
        try_move_tank.moveUp()
        return try_move_tank

    def try_moveDown(self, is_change_direction=True):
        if is_change_direction:
            self.cache_image = self.image_player1_2_down1, self.image_player1_2_down2

        try_move_tank = self.get_try_move_tank()
        try_move_tank.moveDown()
        return try_move_tank

    def try_moveLeft(self, is_change_direction=True):
        if is_change_direction:
            self.cache_image = self.image_player1_2_left1, self.image_player1_2_left2

        try_move_tank = self.get_try_move_tank()
        try_move_tank.moveLeft()
        return try_move_tank

    def try_moveRight(self, is_change_direction=True):
        if is_change_direction:
            self.cache_image = self.image_player1_2_right1, self.image_player1_2_right2

        try_move_tank = self.get_try_move_tank()
        try_move_tank.moveRight()
        return try_move_tank

    def moveUp(self):
        self.rect.top -= self.speed

    def moveDown(self):
        self.rect.top += self.speed

    def moveLeft(self):
        self.rect.left -= self.speed

    def moveRight(self):
        self.rect.left += self.speed
