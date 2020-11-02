from Unit.Coordinate import Coordinate
from Unit.Guard import Guard_tank_generate
from Unit.Star import Star_tank_generate
from Unit.Tank.Tank_bullet import *


class Camp2_tank1(pygame.sprite.Sprite):
    try_move_tank = None

    def __init__(self, start_pos_xy):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.cache_image = self.image_enemy0_down1, self.image_enemy0_down2
        self.rect = self.cache_image[0].get_rect()
        self.rect.left, self.rect.top = Coordinate.xy_to_left_top_pixel(start_pos_xy[0], start_pos_xy[1])

        self.speed = 2
        self.direction = 2

        # 生成自己的子弹
        self.generate_bullet()
        # 产生 防护罩
        self.generate_guard()
        # 产生 星形图像
        self.star_initial = Star_tank_generate()
        self.star_initial.rect.center = self.rect.center
        # 自己的血量
        self.hp = 2
        self.sum_hp = 2

    # 轻型坦克有 1 发子弹
    def generate_bullet(self):
        bullet1 = Bullet1()
        bullet1.owner = 2
        self.bullets = [bullet1]

    # 发射子弹
    def fire_bullet(self):
        for bullet in self.bullets:
            if bullet.active == 0:
                # 子弹初始化
                bullet.active = 1
                if self.image_enemy0_up1 in self.cache_image:
                    bullet.image = bullet.image_bullet_up
                    bullet.rect.left = self.rect.left + self.rect.width // 2 - 10
                    bullet.rect.top = self.rect.top
                elif self.image_enemy0_down1 in self.cache_image:
                    bullet.image = bullet.image_bullet_down
                    bullet.rect.left = self.rect.left + self.rect.width // 2 - 10
                    bullet.rect.top = self.rect.top + self.rect.height
                elif self.image_enemy0_left1 in self.cache_image:
                    bullet.image = bullet.image_bullet_left
                    bullet.rect.left = self.rect.left
                    bullet.rect.top = self.rect.top + self.rect.height // 2 - 10
                elif self.image_enemy0_right1 in self.cache_image:
                    bullet.image = bullet.image_bullet_right
                    bullet.rect.left = self.rect.left + self.rect.width
                    bullet.rect.top = self.rect.top + self.rect.height // 2 - 10
                break

    def generate_guard(self):
        self.guard = Guard_tank_generate()

    # 坦克最初的星型 显示
    def display_star(self, screen):
        self.star_initial.display(screen)

    # 在屏幕的显示
    def display(self, screen, delay):
        self.guard.rect.center = self.rect.center
        self.guard.display(screen)

        if self.star_initial.is_completed() is False:
            self.display_star(screen)
            return

        screen.blit(self.cache_image[delay % 2], self.rect)
        # 显示子弹
        for bullet in self.bullets:
            if bullet.active == 1:
                screen.blit(bullet.image, bullet.rect)

    def load_image(self):
        # 下图
        self.image_enemy0_down1 = pygame.image.load("../Image/Enemy_Tank1/enemy0_down1.png").convert_alpha()
        self.image_enemy0_down2 = pygame.image.load("../Image/Enemy_Tank1/enemy0_down2.png").convert_alpha()
        # 左图
        self.image_enemy0_left1 = pygame.image.load("../Image/Enemy_Tank1/enemy0_left1.png").convert_alpha()
        self.image_enemy0_left2 = pygame.image.load("../Image/Enemy_Tank1/enemy0_left2.png").convert_alpha()
        # 右图
        self.image_enemy0_right1 = pygame.image.load("../Image/Enemy_Tank1/enemy0_right1.png").convert_alpha()
        self.image_enemy0_right2 = pygame.image.load("../Image/Enemy_Tank1/enemy0_right2.png").convert_alpha()
        # 上图
        self.image_enemy0_up1 = pygame.image.load("../Image/Enemy_Tank1/enemy0_up1.png").convert_alpha()
        self.image_enemy0_up2 = pygame.image.load("../Image/Enemy_Tank1/enemy0_up2.png").convert_alpha()

    def get_try_move_tank(self):
        if Camp2_tank1.try_move_tank is None:
            Camp2_tank1.try_move_tank = Camp2_tank1((0, 0))
        try_move_tank = Camp2_tank1.try_move_tank
        try_move_tank.rect.left = self.rect.left
        try_move_tank.rect.top = self.rect.top
        try_move_tank.speed = self.speed
        return try_move_tank

    # 返回一个深拷贝的对象
    def try_moveUp(self, is_change_direction):
        if is_change_direction:
            self.cache_image = self.image_enemy0_up1, self.image_enemy0_up2
            self.direction = 1

        try_move_tank = self.get_try_move_tank()
        try_move_tank.moveUp()
        return try_move_tank

    def try_moveDown(self, is_change_direction):
        if is_change_direction:
            self.cache_image = self.image_enemy0_down1, self.image_enemy0_down2
            self.direction = 2

        try_move_tank = self.get_try_move_tank()
        try_move_tank.moveDown()
        return try_move_tank

    def try_moveLeft(self, is_change_direction):
        if is_change_direction:
            self.cache_image = self.image_enemy0_left1, self.image_enemy0_left2
            self.direction = 3

        try_move_tank = self.get_try_move_tank()
        try_move_tank.moveLeft()
        return try_move_tank

    def try_moveRight(self, is_change_direction):
        if is_change_direction:
            self.cache_image = self.image_enemy0_right1, self.image_enemy0_right2
            self.direction = 4

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


class Camp2_tank2(pygame.sprite.Sprite):
    try_move_tank = None

    def __init__(self, start_pos_xy):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.cache_image = self.image_enemy0_down1, self.image_enemy0_down2
        self.rect = self.cache_image[0].get_rect()
        self.rect.left, self.rect.top = Coordinate.xy_to_left_top_pixel(start_pos_xy[0], start_pos_xy[1])

        self.speed = 4
        self.direction = 2

        # 生成自己的子弹
        self.generate_bullet()
        # 产生 防护罩
        self.generate_guard()
        # 产生 星形图像
        self.star_initial = Star_tank_generate()
        self.star_initial.rect.center = self.rect.center
        # 自己的血量
        self.hp = 2
        self.sum_hp = 2

    # 轻型坦克有 1 发子弹
    def generate_bullet(self):
        bullet1 = Bullet1()
        bullet1.owner = 2
        self.bullets = [bullet1]

    # 发射子弹
    def fire_bullet(self):
        for bullet in self.bullets:
            if bullet.active == 0:
                # 子弹初始化
                bullet.active = 1
                if self.image_enemy0_up1 in self.cache_image:
                    bullet.image = bullet.image_bullet_up
                    bullet.rect.left = self.rect.left + self.rect.width // 2 - 10
                    bullet.rect.top = self.rect.top
                elif self.image_enemy0_down1 in self.cache_image:
                    bullet.image = bullet.image_bullet_down
                    bullet.rect.left = self.rect.left + self.rect.width // 2 - 10
                    bullet.rect.top = self.rect.top + self.rect.height
                elif self.image_enemy0_left1 in self.cache_image:
                    bullet.image = bullet.image_bullet_left
                    bullet.rect.left = self.rect.left
                    bullet.rect.top = self.rect.top + self.rect.height // 2 - 10
                elif self.image_enemy0_right1 in self.cache_image:
                    bullet.image = bullet.image_bullet_right
                    bullet.rect.left = self.rect.left + self.rect.width
                    bullet.rect.top = self.rect.top + self.rect.height // 2 - 10
                break

    def generate_guard(self):
        self.guard = Guard_tank_generate()

    # 坦克最初的星型 显示
    def display_star(self, screen):
        self.star_initial.display(screen)

    # 在屏幕的显示
    def display(self, screen, delay):
        self.guard.rect.center = self.rect.center
        self.guard.display(screen)

        if self.star_initial.is_completed() is False:
            self.display_star(screen)
            return

        screen.blit(self.cache_image[delay % 2], self.rect)
        # 显示子弹
        for bullet in self.bullets:
            if bullet.active == 1:
                screen.blit(bullet.image, bullet.rect)

    def load_image(self):
        # 下图
        self.image_enemy0_down1 = pygame.image.load("../Image/Enemy_Tank1/enemy1_down1.png").convert_alpha()
        self.image_enemy0_down2 = pygame.image.load("../Image/Enemy_Tank1/enemy1_down2.png").convert_alpha()
        # 左图
        self.image_enemy0_left1 = pygame.image.load("../Image/Enemy_Tank1/enemy1_left1.png").convert_alpha()
        self.image_enemy0_left2 = pygame.image.load("../Image/Enemy_Tank1/enemy1_left2.png").convert_alpha()
        # 右图
        self.image_enemy0_right1 = pygame.image.load("../Image/Enemy_Tank1/enemy1_right1.png").convert_alpha()
        self.image_enemy0_right2 = pygame.image.load("../Image/Enemy_Tank1/enemy1_right2.png").convert_alpha()
        # 上图
        self.image_enemy0_up1 = pygame.image.load("../Image/Enemy_Tank1/enemy1_up1.png").convert_alpha()
        self.image_enemy0_up2 = pygame.image.load("../Image/Enemy_Tank1/enemy1_up2.png").convert_alpha()

    def get_try_move_tank(self):
        if Camp2_tank1.try_move_tank is None:
            Camp2_tank1.try_move_tank = Camp2_tank1((0, 0))
        try_move_tank = Camp2_tank1.try_move_tank
        try_move_tank.rect.left = self.rect.left
        try_move_tank.rect.top = self.rect.top
        try_move_tank.speed = self.speed
        return try_move_tank

    # 返回一个深拷贝的对象
    def try_moveUp(self, is_change_direction):
        if is_change_direction:
            self.cache_image = self.image_enemy0_up1, self.image_enemy0_up2
            self.direction = 1

        try_move_tank = self.get_try_move_tank()
        try_move_tank.moveUp()
        return try_move_tank

    def try_moveDown(self, is_change_direction):
        if is_change_direction:
            self.cache_image = self.image_enemy0_down1, self.image_enemy0_down2
            self.direction = 2

        try_move_tank = self.get_try_move_tank()
        try_move_tank.moveDown()
        return try_move_tank

    def try_moveLeft(self, is_change_direction):
        if is_change_direction:
            self.cache_image = self.image_enemy0_left1, self.image_enemy0_left2
            self.direction = 3

        try_move_tank = self.get_try_move_tank()
        try_move_tank.moveLeft()
        return try_move_tank

    def try_moveRight(self, is_change_direction):
        if is_change_direction:
            self.cache_image = self.image_enemy0_right1, self.image_enemy0_right2
            self.direction = 4

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


class Camp2_tank3(pygame.sprite.Sprite):
    try_move_tank = None

    def __init__(self, start_pos_xy):
        pygame.sprite.Sprite.__init__(self)
        self.load_image()
        self.cache_image = self.image_enemy0_down1, self.image_enemy0_down2
        self.rect = self.cache_image[0].get_rect()
        self.rect.left, self.rect.top = Coordinate.xy_to_left_top_pixel(start_pos_xy[0], start_pos_xy[1])

        self.speed = 2
        self.direction = 2

        # 生成自己的子弹
        self.generate_bullet()
        # 产生 防护罩
        self.generate_guard()
        # 产生 星形图像
        self.star_initial = Star_tank_generate()
        self.star_initial.rect.center = self.rect.center
        # 自己的血量
        self.hp = 3
        self.sum_hp = 3

    def generate_bullet(self):
        bullet1 = Bullet1()
        bullet1.owner = 2
        bullet1.power = 2
        bullet2 = Bullet1()
        bullet2.owner = 2
        bullet2.power = 2
        self.bullets = [bullet1, bullet2]

    # 发射子弹
    def fire_bullet(self):
        for bullet in self.bullets:
            if bullet.active == 0:
                # 子弹初始化
                bullet.active = 1
                if self.image_enemy0_up1 in self.cache_image:
                    bullet.image = bullet.image_bullet_up
                    bullet.rect.left = self.rect.left + self.rect.width // 2 - 10
                    bullet.rect.top = self.rect.top
                elif self.image_enemy0_down1 in self.cache_image:
                    bullet.image = bullet.image_bullet_down
                    bullet.rect.left = self.rect.left + self.rect.width // 2 - 10
                    bullet.rect.top = self.rect.top + self.rect.height
                elif self.image_enemy0_left1 in self.cache_image:
                    bullet.image = bullet.image_bullet_left
                    bullet.rect.left = self.rect.left
                    bullet.rect.top = self.rect.top + self.rect.height // 2 - 10
                elif self.image_enemy0_right1 in self.cache_image:
                    bullet.image = bullet.image_bullet_right
                    bullet.rect.left = self.rect.left + self.rect.width
                    bullet.rect.top = self.rect.top + self.rect.height // 2 - 10
                break

    def generate_guard(self):
        self.guard = Guard_tank_generate()

    # 坦克最初的星型 显示
    def display_star(self, screen):
        self.star_initial.display(screen)

    # 在屏幕的显示
    def display(self, screen, delay):
        self.guard.rect.center = self.rect.center
        self.guard.display(screen)

        if self.star_initial.is_completed() is False:
            self.display_star(screen)
            return

        screen.blit(self.cache_image[delay % 2], self.rect)
        # 显示子弹
        for bullet in self.bullets:
            if bullet.active == 1:
                screen.blit(bullet.image, bullet.rect)

    def load_image(self):
        # 下图
        self.image_enemy0_down1 = pygame.image.load("../Image/Enemy_Tank1/enemy3_down1.png").convert_alpha()
        self.image_enemy0_down2 = pygame.image.load("../Image/Enemy_Tank1/enemy3_down2.png").convert_alpha()
        # 左图
        self.image_enemy0_left1 = pygame.image.load("../Image/Enemy_Tank1/enemy3_left1.png").convert_alpha()
        self.image_enemy0_left2 = pygame.image.load("../Image/Enemy_Tank1/enemy3_left2.png").convert_alpha()
        # 右图
        self.image_enemy0_right1 = pygame.image.load("../Image/Enemy_Tank1/enemy3_right1.png").convert_alpha()
        self.image_enemy0_right2 = pygame.image.load("../Image/Enemy_Tank1/enemy3_right2.png").convert_alpha()
        # 上图
        self.image_enemy0_up1 = pygame.image.load("../Image/Enemy_Tank1/enemy3_up1.png").convert_alpha()
        self.image_enemy0_up2 = pygame.image.load("../Image/Enemy_Tank1/enemy3_up2.png").convert_alpha()

    def get_try_move_tank(self):
        if Camp2_tank1.try_move_tank is None:
            Camp2_tank1.try_move_tank = Camp2_tank1((0, 0))
        try_move_tank = Camp2_tank1.try_move_tank
        try_move_tank.rect.left = self.rect.left
        try_move_tank.rect.top = self.rect.top
        try_move_tank.speed = self.speed
        return try_move_tank

    # 返回一个深拷贝的对象
    def try_moveUp(self, is_change_direction):
        if is_change_direction:
            self.cache_image = self.image_enemy0_up1, self.image_enemy0_up2
            self.direction = 1

        try_move_tank = self.get_try_move_tank()
        try_move_tank.moveUp()
        return try_move_tank

    def try_moveDown(self, is_change_direction):
        if is_change_direction:
            self.cache_image = self.image_enemy0_down1, self.image_enemy0_down2
            self.direction = 2

        try_move_tank = self.get_try_move_tank()
        try_move_tank.moveDown()
        return try_move_tank

    def try_moveLeft(self, is_change_direction):
        if is_change_direction:
            self.cache_image = self.image_enemy0_left1, self.image_enemy0_left2
            self.direction = 3

        try_move_tank = self.get_try_move_tank()
        try_move_tank.moveLeft()
        return try_move_tank

    def try_moveRight(self, is_change_direction):
        if is_change_direction:
            self.cache_image = self.image_enemy0_right1, self.image_enemy0_right2
            self.direction = 4

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