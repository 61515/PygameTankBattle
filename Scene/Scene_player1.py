import sys

from pygame.locals import *
from Map.Map import Map
from Unit.Mark import *
from Unit.Tank.Camp1_tank import Camp1_tank1
from Unit.Tank.Player1_tank import *
from Unit.Tank.Camp2_tank import *
from Unit.Boom import *
from Unit.Land import *
from Unit.Tools.Some_Tool import *


class Scene_player1:
    # 初始化当前scene 参数,加载当前关的地图,图片音频资源,生成两方阵营坦克,精灵组all_tank,boom_images爆炸列表,
    # 生成 道具列表 Tools
    def __init__(self, stage):
        pygame.init()
        pygame.mixer.init()
        self.stage = stage
        self.bg_size = self.width, self.height = 32 * 32, 30 * 32
        self.rows = 30
        self.cols = 32
        self.rounds_num = 35
        self.screen = pygame.display.set_mode(self.bg_size)
        pygame.display.set_caption("坦克大战")

        self.clock = pygame.time.Clock()

        self.load_image()
        self.load_map(stage)
        self.load_audio()

        self.all_tank = pygame.sprite.Group()
        self.generate_camp1()
        self.generate_camp2()

        self.boom_images = []
        self.tools = []

        self.generate_mark()

    # 加载Audio音频资源
    def load_audio(self):
        self.game_begin_sound = pygame.mixer.Sound("../Audio/GameBegin.wav")
        self.game_begin_sound.set_volume(0.03)
        self.running_enemy_sound = pygame.mixer.Sound("../Audio/Running_Enemy.wav")
        self.running_enemy_sound.set_volume(0.04)
        self.running_player_sound = pygame.mixer.Sound("../Audio/Running_Player_1.wav")
        self.running_player_sound.set_volume(0.04)
        self.game_over_sound = pygame.mixer.Sound("../Audio/GameOver.wav")
        self.game_over_sound.set_volume(0.04)
        self.game_win_sound = pygame.mixer.Sound("../Audio/GameWin.wav")
        self.game_win_sound.set_volume(0.04)
        self.game_shoot = pygame.mixer.Sound("../Audio/Shoot.wav")
        self.game_shoot.set_volume(0.02)
        self.boom_enemy = pygame.mixer.Sound("../Audio/boom_enemy.wav")
        self.boom_enemy.set_volume(0.04)
        self.boom_player = pygame.mixer.Sound("../Audio/boom_player.wav")
        self.boom_player.set_volume(0.04)
        self.brokenarmor = pygame.mixer.Sound("../Audio/BrokenArmor.wav")
        self.brokenarmor.set_volume(0.04)
        self.item_appear = pygame.mixer.Sound("../Audio/Item_Appear.wav")
        self.item_appear.set_volume(0.04)
        self.item_get = pygame.mixer.Sound("../Audio/Item_Get.wav")
        self.item_get.set_volume(0.04)

    # 加载当前黑色背景图
    def load_image(self):
        self.image_black_32 = pygame.image.load("../Image/Land/black_32.png").convert_alpha()
        self.image_black_16 = pygame.image.load("../Image/Land/black_16.png").convert_alpha()

    # 加载当前关的地形类
    def load_map(self, stage):
        self.map = Map(stage)

    # 产生阵营一坦克,玩家1坦克,并加入到camp1_group, all_tank
    def generate_camp1(self):
        self.camp1_group = pygame.sprite.Group()
        self.player1 = Player_Tank_2()
        self.camp1_group.add(self.player1)
        self.all_tank.add(self.camp1_group)
        # 产生蓝色坦克
        camp1_tank = Camp1_tank1()
        self.camp1_group.add(camp1_tank)
        self.all_tank.add(camp1_tank)

    # 产生阵营二坦克,并加入到camp2_group, all_tank
    def generate_camp2(self):
        self.camp2_pos_xy = [(2, 2), (2, 14), (2, 26)]
        self.camp2_group = pygame.sprite.Group()

    # 检查 当前坦克和地形,当前坦克和所有坦克之间的碰撞
    def check_tank_pos(self, try_move_tank, sprite):
        if self.map.check_land_collide(try_move_tank):

            self.all_tank.remove(sprite)
            num = len(pygame.sprite.spritecollide(try_move_tank, self.all_tank, False))
            self.all_tank.add(sprite)

            # 无坦克碰撞
            if num == 0:
                return True
            else:
                return False
        else:
            return False

    # 检查 子弹和地形的碰撞(若碰撞,添加小型爆炸效果 boom_images), 子弹和敌方阵营的碰撞(若碰撞,添加小型爆炸效果 boom_images,
    # 敌方坦克在all_tank和enemy_group消失,等待重新生成), 两阵营的子弹相互抵消,子弹与commander碰撞情况
    def check_bullet_pos(self, tank_bullet, is_player_bullet):
        if self.map.check_bullet_collide(tank_bullet) is False:
            boom_image = Boom_small()
            boom_image.rect.center = tank_bullet.rect.center

            self.boom_images.append(boom_image)
            return False

        enemy_group = None
        if tank_bullet.owner == 1:
            enemy_group = self.camp2_group
        elif tank_bullet.owner == 2:
            enemy_group = self.camp1_group

        collide_enemy_tanks = pygame.sprite.spritecollide(tank_bullet, enemy_group, False)
        for enemy_tank in collide_enemy_tanks:
            # 当前是 无敌时间
            if enemy_tank.guard.is_invincible():
                # 小型爆炸产生
                boom_image = Boom_small()
                boom_image.rect.center = tank_bullet.rect.center

                self.boom_images.append(boom_image)
                return False
            enemy_tank.hp -= tank_bullet.power
            if enemy_tank.hp <= 0:
                enemy_group.remove(enemy_tank)
                self.all_tank.remove(enemy_tank)
                boom_image = Tank_boom()
                boom_image.rect.center = enemy_tank.rect.center
                self.boom_images.append(boom_image)
                if is_player_bullet:
                    self.boom_enemy.play()
            else:
                boom_image = Boom_small()
                boom_image.rect.center = tank_bullet.rect.center

                self.boom_images.append(boom_image)
            return False

        # 检查两方阵营的子弹相互之间碰撞
        enemy_all_bullets = pygame.sprite.Group()
        for enemy_tank in enemy_group:
            for bullet in enemy_tank.bullets:
                if bullet.active:
                    enemy_all_bullets.add(bullet)
        collide_bullet = pygame.sprite.spritecollide(tank_bullet, enemy_all_bullets, True)
        if len(collide_bullet) > 0:
            for bullet in collide_bullet:
                bullet.active = False
            boom_image = Boom_small()
            boom_image.rect.center = tank_bullet.rect.center

            self.boom_images.append(boom_image)
            return False
        return True

    # 检查 导弹碰撞情况
    def check_missile_pos2(self, tank_missile, is_player_bullet):
        if self.map.check_missile_collide(tank_missile) is False:
            boom_image = Boom_small()
            boom_image.rect.center = tank_missile.rect.center

            self.boom_images.append(boom_image)
            return False

        enemy_group = None
        if tank_missile.owner == 1:
            enemy_group = self.camp2_group
        elif tank_missile.owner == 2:
            enemy_group = self.camp1_group

        collide_enemy_tanks = pygame.sprite.spritecollide(tank_missile, enemy_group, False)
        for enemy_tank in collide_enemy_tanks:
            # 当前是 无敌时间
            if enemy_tank.guard.is_invincible():
                # 小型爆炸产生
                boom_image = Boom_small()
                boom_image.rect.center = tank_missile.rect.center
                self.boom_images.append(boom_image)
                return False

            enemy_group.remove(enemy_tank)
            self.all_tank.remove(enemy_tank)
            boom_image = Tank_boom()
            boom_image.rect.center = enemy_tank.rect.center
            self.boom_images.append(boom_image)
            if is_player_bullet:
                self.boom_enemy.play()
            return False

        return True

    # 每 x 帧执行一次
    def do_delay(self, x):
        if self.delay % x == 0:
            return True
        return False

    # 游戏的当前循环
    def event_loop(self):
        # 初始化帧率计数,播放声音,设置阵营2坦克个数,不足4位时增援
        self.delay = 0
        self.game_begin_sound.play()
        camp2_tank_num = 20

        # 运行时的临时变量
        run_time = 1
        camp1_tank_num = 2
        my_habit = True
        camp1_group_cannot_move_time_frame = 0
        camp2_group_cannot_move_time_frame = 0

        while True:
            # 运行时, 1 为正常运行, 0 为暂停状态, 2 为结束状态
            # 处理事件
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if run_time == 1:
                            run_time = 0
                        elif run_time == 0:
                            run_time = 1
                    if event.key == K_h:
                        for commander in self.map.commanders:
                            if commander.enable is False:
                                commander.enable = True
                            else:
                                commander.enable = False
                    if event.key == K_m:
                        if camp1_tank_num == 2:
                            camp1_tank_num = 6
                        else:
                            camp1_tank_num = 2
                    if event.key == K_i:
                        num = 0
                        for mine in self.player1.mines:
                            if mine.active:
                                num += 1
                        self.player1.fire_mine()
                        for mine in self.player1.mines:
                            if mine.active:
                                num -= 1
                        if num == -1:
                            self.brokenarmor.play()

            if run_time == 1:
                # 处理键盘按键,玩家移动,发射子弹或者发射导弹
                key_pressed = pygame.key.get_pressed()
                if key_pressed[K_j] and self.player1.star_initial.is_completed():
                    if self.player1.fire_bullet():
                        self.game_shoot.play()
                if key_pressed[K_k] and self.player1.star_initial.is_completed():
                    if self.player1.fire_missile():
                        self.game_shoot.play()
                if key_pressed[K_l]:
                    self.generate_iron()
                if key_pressed[K_u]:
                    self.generate_jungle()
                if my_habit:
                    if not (key_pressed[K_s] and key_pressed[K_f] or key_pressed[K_e] and
                            key_pressed[K_d]) and self.player1.star_initial.is_completed():
                        if key_pressed[K_s]:
                            if self.check_tank_pos(self.player1.try_moveLeft(), self.player1):
                                self.player1.moveLeft()
                                # if self.do_delay(15):
                                #     self.running_player_sound.play()
                            # 尝试下左,上左
                            else:
                                if self.check_tank_pos(self.player1.try_moveUp(False).
                                                               try_moveLeft(False), self.player1):
                                    self.player1.moveUp()
                                    self.player1.moveLeft()
                                elif self.check_tank_pos(self.player1.try_moveDown(False).
                                                               try_moveLeft(False), self.player1):
                                    self.player1.moveDown()
                                    self.player1.moveLeft()
                        elif key_pressed[K_f]:
                            if self.check_tank_pos(self.player1.try_moveRight(), self.player1):
                                self.player1.moveRight()
                                # if self.do_delay(15):
                                #     self.running_player_sound.play()
                            else:
                                # 上右
                                if self.check_tank_pos(self.player1.try_moveUp(False).
                                                               try_moveRight(False), self.player1):
                                    self.player1.moveUp()
                                    self.player1.moveRight()
                                # 下右
                                elif self.check_tank_pos(self.player1.try_moveDown(False).
                                                               try_moveRight(False), self.player1):
                                    self.player1.moveDown()
                                    self.player1.moveRight()
                        elif key_pressed[K_e]:
                            if self.check_tank_pos(self.player1.try_moveUp(), self.player1):
                                self.player1.moveUp()
                                # if self.do_delay(15):
                                #     self.running_player_sound.play()
                            else:
                                # 左上
                                if self.check_tank_pos(self.player1.try_moveLeft(False).
                                                               try_moveUp(False), self.player1):
                                    self.player1.moveLeft()
                                    self.player1.moveUp()
                                # 右上
                                elif self.check_tank_pos(self.player1.try_moveRight(False).
                                                               try_moveUp(False), self.player1):
                                    self.player1.moveRight()
                                    self.player1.moveUp()
                        elif key_pressed[K_d]:
                            if self.check_tank_pos(self.player1.try_moveDown(), self.player1):
                                self.player1.moveDown()
                                # if self.do_delay(15):
                                #     self.running_player_sound.play()
                            else:
                                # 左下
                                if self.check_tank_pos(self.player1.try_moveLeft(False).
                                                               try_moveDown(False), self.player1):
                                    self.player1.moveLeft()
                                    self.player1.moveDown()
                                # 右下
                                elif self.check_tank_pos(self.player1.try_moveRight(False).
                                                                 try_moveDown(False), self.player1):
                                    self.player1.moveRight()
                                    self.player1.moveDown()
                else:
                    if not (key_pressed[K_a] and key_pressed[K_d] or key_pressed[K_w] and
                            key_pressed[K_s]) and self.player1.star_initial.is_completed():
                        if key_pressed[K_a]:
                            if self.check_tank_pos(self.player1.try_moveLeft(), self.player1):
                                self.player1.moveLeft()
                                # if self.do_delay(15):
                                #     self.running_player_sound.play()
                            # 尝试 上左,下左
                            else:
                                if self.check_tank_pos(self.player1.try_moveUp(False).
                                                               try_moveLeft(False), self.player1):
                                    self.player1.moveUp()
                                    self.player1.moveLeft()
                                elif self.check_tank_pos(self.player1.try_moveDown(False).
                                                                 try_moveLeft(False), self.player1):
                                    self.player1.moveDown()
                                    self.player1.moveLeft()
                        elif key_pressed[K_d]:
                            if self.check_tank_pos(self.player1.try_moveRight(), self.player1):
                                self.player1.moveRight()
                                # if self.do_delay(15):
                                #     self.running_player_sound.play()
                            else:
                                # 上右
                                if self.check_tank_pos(self.player1.try_moveUp(False).
                                                               try_moveRight(False), self.player1):
                                    self.player1.moveUp()
                                    self.player1.moveRight()
                                # 下右
                                elif self.check_tank_pos(self.player1.try_moveDown(False).
                                                               try_moveRight(False), self.player1):
                                    self.player1.moveDown()
                                    self.player1.moveRight()
                        elif key_pressed[K_w]:
                            if self.check_tank_pos(self.player1.try_moveUp(), self.player1):
                                self.player1.moveUp()
                                # if self.do_delay(15):
                                #     self.running_player_sound.play()
                            else:
                                # 左上
                                if self.check_tank_pos(self.player1.try_moveLeft(False).
                                                               try_moveUp(False), self.player1):
                                    self.player1.moveLeft()
                                    self.player1.moveUp()
                                # 右上
                                elif self.check_tank_pos(self.player1.try_moveRight(False).
                                                               try_moveUp(False), self.player1):
                                    self.player1.moveRight()
                                    self.player1.moveUp()
                        elif key_pressed[K_s]:
                            if self.check_tank_pos(self.player1.try_moveDown(), self.player1):
                                self.player1.moveDown()
                                # if self.do_delay(15):
                                #     self.running_player_sound.play()
                            else:
                                # 左下
                                if self.check_tank_pos(self.player1.try_moveLeft(False).
                                                               try_moveDown(False), self.player1):
                                    self.player1.moveLeft()
                                    self.player1.moveDown()
                                # 右下
                                elif self.check_tank_pos(self.player1.try_moveRight(False).
                                                                 try_moveDown(False), self.player1):
                                    self.player1.moveRight()
                                    self.player1.moveDown()

                # 处理阵营1cpu 坦克移动(星形图像已显示完毕),发射子弹的情况,死亡时无限复活, 处理基地发射导弹情况
                for camp1_tank in self.camp1_group:
                    if camp1_tank == self.player1:
                        continue
                    if camp1_tank.star_initial.is_completed():
                        if camp1_group_cannot_move_time_frame > 0:
                            camp1_group_cannot_move_time_frame -= 1
                            break
                        self.cpu_camp1_tank_move(camp1_tank)
                        # 发射子弹
                        if self.do_delay(10):
                            camp1_tank.fire_bullet(self.map.commanders)

                for i in range(max(0, camp1_tank_num - len(self.camp1_group) + 1)):
                    camp1_tank = Camp1_tank1()
                    if self.map.check_land_collide(camp1_tank) and \
                            len(pygame.sprite.spritecollide(camp1_tank, self.all_tank, False)) == 0:
                        self.all_tank.add(camp1_tank)
                        self.camp1_group.add(camp1_tank)

                for commander in self.map.commanders:
                    if commander.enable:
                        commander.fire_missile()

                # 处理阵营2cpu 坦克移动,发射子弹的情况,成员不足时 补员
                for camp2_tank in self.camp2_group:
                    if camp2_tank.star_initial.is_completed():
                        if camp2_group_cannot_move_time_frame > 0:
                            camp2_group_cannot_move_time_frame -= 1
                            break
                        self.cpu_camp2_tank_move(camp2_tank)
                        # 发射子弹
                        if self.do_delay(10):
                            camp2_tank.fire_bullet()
                # if self.camp2_group:
                #     if self.do_delay(20):
                #         self.running_enemy_sound.play()

                if len(self.camp2_group) < 4 and camp2_tank_num > 0:
                    num = min(camp2_tank_num, 4 - len(self.camp2_group))
                    for i in range(num):
                        for j in range(3):
                            # 随机产生 坦克类型
                            rand = random.randint(1, 3)
                            camp2_tank = None
                            if rand == 1:
                                camp2_tank = Camp2_tank1(self.camp2_pos_xy[j])
                            elif rand == 2:
                                camp2_tank = Camp2_tank2(self.camp2_pos_xy[j])
                            elif rand == 3:
                                camp2_tank = Camp2_tank3(self.camp2_pos_xy[j])

                            if self.map.check_land_collide(camp2_tank) and \
                                    len(pygame.sprite.spritecollide(camp2_tank, self.all_tank, False)) == 0:
                                self.all_tank.add(camp2_tank)
                                self.camp2_group.add(camp2_tank)
                                camp2_tank_num -= 1
                                break

                # 所有活动子弹移动,碰撞(地形,坦克)情况
                all_active_bullet = []
                # 阵营1 坦克子弹
                for camp1_tank in self.camp1_group:
                    for tank_bullet in camp1_tank.bullets:
                        all_active_bullet.append(tank_bullet)
                # 阵营2 坦克子弹
                for camp2_tank in self.camp2_group:
                    for tank_bullet in camp2_tank.bullets:
                        all_active_bullet.append(tank_bullet)

                for tank_bullet in all_active_bullet:
                    is_player_bullet = False
                    if tank_bullet in self.player1.bullets:
                        is_player_bullet = True

                    if tank_bullet.active:
                        if self.check_bullet_pos(tank_bullet, is_player_bullet) is False:
                            tank_bullet.active = False
                            continue
                        # 移动最小的单位像素, 看是否发生地形碰撞, 寸进法
                        each_pixel = 16
                        times = tank_bullet.speed // each_pixel
                        remind = tank_bullet.speed % each_pixel

                        if tank_bullet.image == tank_bullet.image_bullet_up:
                            for i in range(times):
                                tank_bullet.rect.top -= each_pixel
                                if self.check_bullet_pos(tank_bullet, is_player_bullet) is False:
                                    tank_bullet.active = False
                                    break
                            if tank_bullet.active:
                                tank_bullet.rect.top -= remind
                                if self.check_bullet_pos(tank_bullet, is_player_bullet) is False:
                                    tank_bullet.active = False

                        elif tank_bullet.image == tank_bullet.image_bullet_down:
                            for i in range(times):
                                tank_bullet.rect.top += each_pixel
                                if self.check_bullet_pos(tank_bullet, is_player_bullet) is False:
                                    tank_bullet.active = False
                                    break
                            if tank_bullet.active:
                                tank_bullet.rect.top += remind
                                if self.check_bullet_pos(tank_bullet, is_player_bullet) is False:
                                    tank_bullet.active = False

                        elif tank_bullet.image == tank_bullet.image_bullet_left:
                            for i in range(times):
                                tank_bullet.rect.left -= each_pixel
                                if self.check_bullet_pos(tank_bullet, is_player_bullet) is False:
                                    tank_bullet.active = False
                                    break
                            if tank_bullet.active:
                                tank_bullet.rect.left -= remind
                                if self.check_bullet_pos(tank_bullet, is_player_bullet) is False:
                                    tank_bullet.active = False

                        elif tank_bullet.image == tank_bullet.image_bullet_right:
                            for i in range(times):
                                tank_bullet.rect.left += each_pixel
                                if self.check_bullet_pos(tank_bullet, is_player_bullet) is False:
                                    tank_bullet.active = False
                                    break
                            if tank_bullet.active:
                                tank_bullet.rect.left += remind
                                if self.check_bullet_pos(tank_bullet, is_player_bullet) is False:
                                    tank_bullet.active = False

                # 所有 活动导弹移动,碰撞(地形,坦克)情况
                all_active_missiles = []
                # 玩家1 坦克导弹
                for missile in self.player1.missiles:
                    all_active_missiles.append(missile)

                for commander in self.map.commanders:
                    for missile in commander.missiles:
                        all_active_missiles.append(missile)

                for missile in all_active_missiles:
                    if missile.active:
                        is_player_missile = False
                        if missile in self.player1.missiles:
                            is_player_missile = True

                        if self.check_missile_pos2(missile, is_player_missile) is False:
                            missile.active = False
                            continue
                        # 移动最小的单位像素, 看是否发生地形碰撞, 寸进法
                        each_pixel = 16
                        times = missile.speed // each_pixel
                        remind = missile.speed % each_pixel

                        if missile.image == missile.image_bullet_up:
                            for i in range(times):
                                missile.rect.top -= each_pixel
                                if self.check_missile_pos2(missile, is_player_missile) is False:
                                    missile.active = False
                                    break
                            if missile.active:
                                missile.rect.top -= remind
                                if self.check_missile_pos2(missile, is_player_missile) is False:
                                    missile.active = False

                        elif missile.image == missile.image_bullet_down:
                            for i in range(times):
                                missile.rect.top += each_pixel
                                if self.check_missile_pos2(missile, is_player_missile) is False:
                                    missile.active = False
                                    break
                            if missile.active:
                                missile.rect.top += remind
                                if self.check_missile_pos2(missile, is_player_missile) is False:
                                    missile.active = False

                        elif missile.image == missile.image_bullet_left:
                            for i in range(times):
                                missile.rect.left -= each_pixel
                                if self.check_missile_pos2(missile, is_player_missile) is False:
                                    missile.active = False
                                    break
                            if missile.active:
                                missile.rect.left -= remind
                                if self.check_missile_pos2(missile, is_player_missile) is False:
                                    missile.active = False

                        elif missile.image == missile.image_bullet_right:
                            for i in range(times):
                                missile.rect.left += each_pixel
                                if self.check_missile_pos2(missile, is_player_missile) is False:
                                    missile.active = False
                                    break
                            if missile.active:
                                missile.rect.left += remind
                                if self.check_missile_pos2(missile, is_player_missile) is False:
                                    missile.active = False

                # 所有 地雷碰撞(地形,坦克)情况
                all_active_mines = []
                for mine in self.player1.mines:
                    all_active_mines.append(mine)

                for mine in all_active_mines:
                    if mine.active:
                        enemy_group = None
                        if mine.owner == 1:
                            enemy_group = self.camp2_group
                        elif mine.owner == 2:
                            enemy_group = self.camp1_group

                        collide_enemy_tanks = pygame.sprite.spritecollide(mine, enemy_group, True)
                        for enemy_tank in collide_enemy_tanks:
                            self.all_tank.remove(enemy_tank)
                            boom_image = Tank_boom()
                            boom_image.rect.center = enemy_tank.rect.center
                            self.boom_images.append(boom_image)
                            mine.active = False
                            self.boom_enemy.play()

                # 处理道具碰撞
                for tool in self.tools:
                    collide_tanks = pygame.sprite.spritecollide(tool, self.all_tank, False)

                    # 防护罩
                    if isinstance(tool, Armor):
                        for collide_tank in collide_tanks:
                            collide_tank.guard.all_frame = 130 * 2
                            if collide_tank == self.player1:
                                self.item_get.play()

                    # 爆炸的情况
                    if isinstance(tool, Explode):

                        will_explode_camps = []
                        for collide_tank in collide_tanks:
                            if collide_tank in self.camp1_group:
                                will_explode_camps.append(2)
                            elif collide_tank in self.camp2_group:
                                will_explode_camps.append(1)

                        if 1 in will_explode_camps:
                            for camp1_tank in self.camp1_group:
                                camp1_tank.hp -= 1
                                if camp1_tank.hp <= 0:
                                    self.camp1_group.remove(camp1_tank)
                                    self.all_tank.remove(camp1_tank)
                                    boom_image = Tank_boom()
                                    boom_image.rect.center = camp1_tank.rect.center
                                    self.boom_images.append(boom_image)
                                else:
                                    # 小型爆炸
                                    boom_small = Boom_small()
                                    boom_small.rect.center = camp1_tank.rect.center
                                    self.boom_images.append(boom_small)

                            self.boom_enemy.play()

                        if 2 in will_explode_camps:
                            for camp2_tank in self.camp2_group:
                                camp2_tank.hp -= 1
                                if camp2_tank.hp <= 0:
                                    self.camp2_group.remove(camp2_tank)
                                    self.all_tank.remove(camp2_tank)
                                    boom_image = Tank_boom()
                                    boom_image.rect.center = camp2_tank.rect.center
                                    self.boom_images.append(boom_image)
                                else:
                                    # 小型爆炸
                                    boom_small = Boom_small()
                                    boom_small.rect.center = camp2_tank.rect.center
                                    self.boom_images.append(boom_small)
                            self.boom_player.play()

                    # 定时器的情况
                    if isinstance(tool, Timer):
                        will_timer_camps = []
                        for collide_tank in collide_tanks:
                            if collide_tank in self.camp1_group:
                                will_timer_camps.append(2)
                            elif collide_tank in self.camp2_group:
                                will_timer_camps.append(1)

                        if 1 in will_timer_camps:
                            camp1_group_cannot_move_time_frame = 120

                        if 2 in will_timer_camps:
                            camp2_group_cannot_move_time_frame = 120

                    # 枪的情况(增加生命值3)
                    if isinstance(tool, Gun):
                        for collide_tank in collide_tanks:
                            collide_tank.hp += 3
                            if collide_tank.hp > collide_tank.sum_hp:
                                collide_tank.hp = collide_tank.sum_hp + 1
                            if collide_tank == self.player1:
                                self.item_get.play()

                    # 星的情况(增加生命值1)
                    if isinstance(tool, Star):
                        for collide_tank in collide_tanks:
                            collide_tank.hp += 1
                            if collide_tank.hp > collide_tank.sum_hp:
                                collide_tank.hp = collide_tank.sum_hp + 1
                            if collide_tank == self.player1:
                                self.item_get.play()

                    # 消除当前道具
                    if collide_tanks:
                        self.tools.remove(tool)

                # 生成道具列表
                if self.delay > 0 and self.do_delay(30 * 10):
                    self.generate_Tools()

            # 填充背景色
            self.screen.fill([0, 0, 0])
            # 绘制地图
            self.map.display_update(self.screen, self.delay)

            # 处理玩家死亡情况或者commander 被击中情况,绘制阵营1坦克
            if self.player1 not in self.camp1_group:
                self.boom_player.play()
                if self.player1.life > 0:
                    self.player1.re_set()
                    # 判断当前是否 无碰撞
                    if len(pygame.sprite.spritecollide(self.player1, self.all_tank, False)) == 0:
                        self.camp1_group.add(self.player1)
                        self.all_tank.add(self.player1)
                        self.player1.life -= 1
            is_destroy = False
            for commander in self.map.commanders:
                if commander.image == commander.image_commander1:
                    is_destroy = True
                    if run_time < 2:
                        self.boom_player.play()
            if (self.player1 not in self.camp1_group) or is_destroy:
                if run_time < 2:
                    run_time = 2

            for camp1_tank in self.camp1_group:
                camp1_tank.display(self.screen, self.delay)

            # 处理所有阵营2坦克死亡情况,绘制阵营2坦克
            if len(self.camp2_group) == 0 and camp2_tank_num == 0:
                if run_time < 4:
                    run_time = 4

            for camp2_tank in self.camp2_group:
                camp2_tank.display(self.screen, self.delay)

            # 绘制爆炸图像, 位置信息 boom_images
            for boom_image in self.boom_images:
                boom_image.display(self.screen)
                if boom_image.image_play_continuously[boom_image.play_index] is None:
                    self.boom_images.remove(boom_image)

            # 绘制所有坦克的血槽,基地血量
            for tank in self.all_tank:
                offset = tank.rect.width * tank.hp / tank.sum_hp
                pygame.draw.line(self.screen, (0, 255, 0), (tank.rect.left, tank.rect.top),
                                 (tank.rect.left + offset, tank.rect.top), 2)
            for commander in self.map.commanders:
                offset = commander.rect.width * commander.hp / commander.sum_hp
                pygame.draw.line(self.screen, (0, 255, 0), (commander.rect.left, commander.rect.top),
                                 (commander.rect.left + offset, commander.rect.top), 2)

            # 绘制草丛
            self.map.display_jungle(self.screen)

            # 绘制道具
            for tool in self.tools:
                tool.display(self.screen, self.delay)

            # 绘制右半边 情景
            # 敌方坦克 数目
            my_font = pygame.font.SysFont('arial', 40)
            text_surface1 = my_font.render(str(camp2_tank_num), True, (255, 0, 0))
            text_rect = text_surface1.get_rect()
            text_rect.center = (950, 200)
            self.screen.blit(text_surface1, text_rect)
            self.enemy_mark.display(self.screen)

            # 我方坦克数目
            text_surface2 = my_font.render(str(self.player1.life), True, (255, 0, 0))
            text_rect = text_surface2.get_rect()
            text_rect.center = (950, 500)
            self.screen.blit(text_surface2, text_rect)
            self.player_mark.display(self.screen)

            text_surface3 = my_font.render(str(self.stage + 1), True, (255, 0, 0))
            text_rect = text_surface3.get_rect()
            text_rect.center = (950, 800)
            self.screen.blit(text_surface3, text_rect)
            self.flag.display(self.screen)

            # 游戏结束时, 播放音乐
            if run_time == 2:
                self.game_over_sound.play()
                run_time = 3
                self.delay = 1

            # 屏幕显示 Game Over! 页面
            if run_time == 3:
                my_font = pygame.font.SysFont('arial', 40)
                text_surface = my_font.render("Game Over!", True, (255, 0, 0))
                text_rect = text_surface.get_rect()
                text_rect.center = (32 * 16, 30 * 16)
                self.screen.blit(text_surface, text_rect)
                if self.do_delay(40):
                    return False

            # 当前关已过,播放声音
            if run_time == 4:
                self.game_win_sound.play()
                self.delay = 1
                run_time = 5

            # 屏幕显示 已过关! 页面
            if run_time == 5:
                my_font = pygame.font.SysFont('arial', 40)
                text_surface = my_font.render("Congratulations!", True, (255, 0, 0))
                text_rect = text_surface.get_rect()
                text_rect.center = (32 * 16, 30 * 16)
                self.screen.blit(text_surface, text_rect)
                if self.do_delay(40):
                    return True

            # 控制帧率,帧结束
            self.delay += 1
            self.delay %= 10000
            pygame.display.flip()
            self.clock.tick(35)

    # cpu 坦克随机移动 的算法实现
    def cpu_camp2_tank_move(self, cpu_tank):

        # 改变方向
        if self.do_delay(10):
            movable_direction = []
            if self.check_tank_pos(cpu_tank.try_moveUp(is_change_direction=False), cpu_tank):
                movable_direction.append(1)
            if self.check_tank_pos(cpu_tank.try_moveDown(is_change_direction=False), cpu_tank):
                movable_direction.append(2)
            if self.check_tank_pos(cpu_tank.try_moveLeft(is_change_direction=False), cpu_tank):
                movable_direction.append(3)
            if self.check_tank_pos(cpu_tank.try_moveRight(is_change_direction=False), cpu_tank):
                movable_direction.append(4)

            # 不能回溯原来的位置
            if len(movable_direction) > 1:
                if cpu_tank.direction == 1:
                    if movable_direction.count(2):
                        movable_direction.remove(2)
                elif cpu_tank.direction == 2:
                    if movable_direction.count(1):
                        movable_direction.remove(1)
                elif cpu_tank.direction == 3:
                    if movable_direction.count(4):
                        movable_direction.remove(4)
                elif cpu_tank.direction == 4:
                    if movable_direction.count(3):
                        movable_direction.remove(3)

            rand_direction = random.randint(1, 4)
            if len(movable_direction) > 0:
                rand_direction = random.choice(movable_direction)
            cpu_tank.direction = rand_direction

        if cpu_tank.direction == 1:
            if self.check_tank_pos(cpu_tank.try_moveUp(is_change_direction=True), cpu_tank):
                cpu_tank.moveUp()
        elif cpu_tank.direction == 2:
            if self.check_tank_pos(cpu_tank.try_moveDown(is_change_direction=True), cpu_tank):
                cpu_tank.moveDown()
        elif cpu_tank.direction == 3:
            if self.check_tank_pos(cpu_tank.try_moveLeft(is_change_direction=True), cpu_tank):
                cpu_tank.moveLeft()
        elif cpu_tank.direction == 4:
            if self.check_tank_pos(cpu_tank.try_moveRight(is_change_direction=True), cpu_tank):
                cpu_tank.moveRight()

    def cpu_camp1_tank_move(self, cpu_tank):

        # 改变方向
        if self.do_delay(10):
            movable_direction = []
            if self.check_tank_pos(cpu_tank.try_moveUp(is_change_direction=False), cpu_tank):
                for i in range(3):
                    movable_direction.append(1)
            if self.check_tank_pos(cpu_tank.try_moveDown(is_change_direction=False), cpu_tank):
                movable_direction.append(2)
            if self.check_tank_pos(cpu_tank.try_moveLeft(is_change_direction=False), cpu_tank):
                movable_direction.append(3)
                movable_direction.append(3)
            if self.check_tank_pos(cpu_tank.try_moveRight(is_change_direction=False), cpu_tank):
                movable_direction.append(4)
                movable_direction.append(4)

            # 不能回溯原来的位置
            if len(movable_direction) > 1:
                if cpu_tank.direction == 1:
                    if movable_direction.count(2):
                        movable_direction.remove(2)
                elif cpu_tank.direction == 2:
                    if movable_direction.count(1):
                        movable_direction.remove(1)
                elif cpu_tank.direction == 3:
                    if movable_direction.count(4):
                        movable_direction.remove(4)
                elif cpu_tank.direction == 4:
                    if movable_direction.count(3):
                        movable_direction.remove(3)

            rand_direction = random.randint(1, 4)
            if len(movable_direction) > 0:
                rand_direction = random.choice(movable_direction)
            cpu_tank.direction = rand_direction

        if cpu_tank.direction == 1:
            if self.check_tank_pos(cpu_tank.try_moveUp(is_change_direction=True), cpu_tank):
                cpu_tank.moveUp()
        elif cpu_tank.direction == 2:
            if self.check_tank_pos(cpu_tank.try_moveDown(is_change_direction=True), cpu_tank):
                cpu_tank.moveDown()
        elif cpu_tank.direction == 3:
            if self.check_tank_pos(cpu_tank.try_moveLeft(is_change_direction=True), cpu_tank):
                cpu_tank.moveLeft()
        elif cpu_tank.direction == 4:
            if self.check_tank_pos(cpu_tank.try_moveRight(is_change_direction=True), cpu_tank):
                cpu_tank.moveRight()

    def generate_iron(self):
        # 生成两个铁块, 判断是否相撞

        if self.player1.cache_image[0] == self.player1.image_player1_2_up1:
            iron1 = Iron()
            iron1.rect.left, iron1.rect.top = self.player1.rect.left, self.player1.rect.top - iron1.rect.height
            iron2 = Iron()
            iron2.rect.left, iron2.rect.top = self.player1.rect.left + iron2.rect.width, \
                                              self.player1.rect.top - iron2.rect.height
            is_ok = 0
            if len(pygame.sprite.spritecollide(iron1, self.all_tank, False)) == 0:
                is_ok += 1
            if len(pygame.sprite.spritecollide(iron2, self.all_tank, False)) == 0:
                is_ok += 1
            if self.map.check_land_collide(iron1) and \
                    len(pygame.sprite.spritecollide(iron1, self.map.jungles, False)) == 0 and \
                    len(pygame.sprite.spritecollide(iron1, self.map.ices, False)) == 0:
                is_ok += 1
            if self.map.check_land_collide(iron2) and \
                    len(pygame.sprite.spritecollide(iron2, self.map.jungles, False)) == 0 and \
                    len(pygame.sprite.spritecollide(iron2, self.map.ices, False)) == 0:
                is_ok += 1

            if is_ok == 4:
                self.map.irons.add(iron1)
                self.map.irons.add(iron2)

        if self.player1.cache_image[0] == self.player1.image_player1_2_down1:
            iron1 = Iron()
            iron1.rect.left, iron1.rect.top = self.player1.rect.left, self.player1.rect.top + self.player1.rect.height
            iron2 = Iron()
            iron2.rect.left, iron2.rect.top = self.player1.rect.left + iron2.rect.width, \
                                              self.player1.rect.top + self.player1.rect.height
            is_ok = 0
            if len(pygame.sprite.spritecollide(iron1, self.all_tank, False)) == 0:
                is_ok += 1
            if len(pygame.sprite.spritecollide(iron2, self.all_tank, False)) == 0:
                is_ok += 1
            if self.map.check_land_collide(iron1) and \
                    len(pygame.sprite.spritecollide(iron1, self.map.jungles, False)) == 0 and \
                    len(pygame.sprite.spritecollide(iron1, self.map.ices, False)) == 0:
                is_ok += 1
            if self.map.check_land_collide(iron2) and \
                    len(pygame.sprite.spritecollide(iron2, self.map.jungles, False)) == 0 and \
                    len(pygame.sprite.spritecollide(iron2, self.map.ices, False)) == 0:
                is_ok += 1

            if is_ok == 4:
                self.map.irons.add(iron1)
                self.map.irons.add(iron2)

        if self.player1.cache_image[0] == self.player1.image_player1_2_left1:
            iron1 = Iron()
            iron1.rect.left, iron1.rect.top = self.player1.rect.left - iron1.rect.width, \
                                              self.player1.rect.top
            iron2 = Iron()
            iron2.rect.left, iron2.rect.top = self.player1.rect.left - iron2.rect.width, \
                                              self.player1.rect.top + iron2.rect.height
            is_ok = 0
            if len(pygame.sprite.spritecollide(iron1, self.all_tank, False)) == 0:
                is_ok += 1
            if len(pygame.sprite.spritecollide(iron2, self.all_tank, False)) == 0:
                is_ok += 1
            if self.map.check_land_collide(iron1) and \
                    len(pygame.sprite.spritecollide(iron1, self.map.jungles, False)) == 0 and \
                    len(pygame.sprite.spritecollide(iron1, self.map.ices, False)) == 0:
                is_ok += 1
            if self.map.check_land_collide(iron2) and \
                    len(pygame.sprite.spritecollide(iron2, self.map.jungles, False)) == 0 and \
                    len(pygame.sprite.spritecollide(iron2, self.map.ices, False)) == 0:
                is_ok += 1

            if is_ok == 4:
                self.map.irons.add(iron1)
                self.map.irons.add(iron2)

        if self.player1.cache_image[0] == self.player1.image_player1_2_right1:
            iron1 = Iron()
            iron1.rect.left, iron1.rect.top = self.player1.rect.left + self.player1.rect.width, \
                                              self.player1.rect.top
            iron2 = Iron()
            iron2.rect.left, iron2.rect.top = self.player1.rect.left + self.player1.rect.width, \
                                              self.player1.rect.top + iron2.rect.height
            is_ok = 0
            if len(pygame.sprite.spritecollide(iron1, self.all_tank, False)) == 0:
                is_ok += 1
            if len(pygame.sprite.spritecollide(iron2, self.all_tank, False)) == 0:
                is_ok += 1
            if self.map.check_land_collide(iron1) and \
                    len(pygame.sprite.spritecollide(iron1, self.map.jungles, False)) == 0 and \
                    len(pygame.sprite.spritecollide(iron1, self.map.ices, False)) == 0:
                is_ok += 1
            if self.map.check_land_collide(iron2) and \
                    len(pygame.sprite.spritecollide(iron2, self.map.jungles, False)) == 0 and \
                    len(pygame.sprite.spritecollide(iron2, self.map.ices, False)) == 0:
                is_ok += 1

            if is_ok == 4:
                self.map.irons.add(iron1)
                self.map.irons.add(iron2)

    def generate_jungle(self):
        jungle1 = Jungle()
        jungle1.rect.left, jungle1.rect.top = self.player1.rect.left, self.player1.rect.top
        jungle2 = Jungle()
        jungle2.rect.left, jungle2.rect.top = self.player1.rect.left + jungle2.rect.width, self.player1.rect.top
        jungle3 = Jungle()
        jungle3.rect.left, jungle3.rect.top = self.player1.rect.left, self.player1.rect.top + jungle3.rect.height
        jungle4 = Jungle()
        jungle4.rect.left, jungle4.rect.top = self.player1.rect.left + jungle4.rect.width, \
                                              self.player1.rect.top + jungle4.rect.height
        is_ok = 0
        if self.map.check_land_collide(jungle1) and \
                len(pygame.sprite.spritecollide(jungle1, self.map.jungles, False)) == 0 and \
                len(pygame.sprite.spritecollide(jungle1, self.map.ices, False)) == 0:
            is_ok += 1
        if self.map.check_land_collide(jungle2) and \
                len(pygame.sprite.spritecollide(jungle2, self.map.jungles, False)) == 0 and \
                len(pygame.sprite.spritecollide(jungle2, self.map.ices, False)) == 0:
            is_ok += 1
        if self.map.check_land_collide(jungle3) and \
                len(pygame.sprite.spritecollide(jungle3, self.map.jungles, False)) == 0 and \
                len(pygame.sprite.spritecollide(jungle3, self.map.ices, False)) == 0:
            is_ok += 1
        if self.map.check_land_collide(jungle4) and \
                len(pygame.sprite.spritecollide(jungle4, self.map.jungles, False)) == 0 and \
                len(pygame.sprite.spritecollide(jungle4, self.map.ices, False)) == 0:
            is_ok += 1
        if is_ok == 4:
            self.map.jungles.add(jungle1)
            self.map.jungles.add(jungle2)
            self.map.jungles.add(jungle3)
            self.map.jungles.add(jungle4)

    def generate_Tools(self):
        if len(self.tools) > 0:
            return

        tools = [1, 2, 3, 6, 7]
        rd = random.choice(tools)
        # 不和其它碰撞
        try_times = 8
        while True:
            rd_left = random.randint(60, 820)
            rd_top = random.randint(65, 820)

            armor = Armor()
            armor.rect.left = rd_left - 64 - 32
            armor.rect.right = rd_left + 64 + 64 + 32
            armor.rect.top = rd_top - 64 - 32
            armor.rect.bottom = rd_top + 64 + 64 + 32

            if len(pygame.sprite.spritecollide(armor, self.all_tank, False)) == 0:
                break
            try_times -= 1
            if try_times == 0:
                break
        if rd == 1:
            armor = Armor()
            armor.rect.left = rd_left
            armor.rect.top = rd_top
            self.tools.append(armor)
            self.item_appear.play()
        elif rd == 2:
            explode = Explode()
            explode.rect.left = rd_left
            explode.rect.top = rd_top
            self.tools.append(explode)
            self.item_appear.play()
        elif rd == 3:
            gun = Gun()
            gun.rect.left = rd_left
            gun.rect.top = rd_top
            self.tools.append(gun)
            self.item_appear.play()
        elif rd == 6:
            star = Star()
            star.rect.left = rd_left
            star.rect.top = rd_top
            self.tools.append(star)
            self.item_appear.play()
        elif rd == 7:
            timer = Timer()
            timer.rect.left = rd_left
            timer.rect.top = rd_top
            self.tools.append(timer)
            self.item_appear.play()

    def generate_mark(self):
        self.enemy_mark = Enemy_mark()
        self.enemy_mark.rect.center = (950, 160)
        self.player_mark = Player_mark()
        self.player_mark.rect.center = (950, 460)
        self.flag = Flag()
        self.flag.rect.center = (950, 760)
