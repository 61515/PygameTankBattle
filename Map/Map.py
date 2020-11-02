from Unit.Land import *
from Unit.Coordinate import *


# 绘制地图类(第一层绘制,同时和地形碰撞,子弹碰撞检测等)


class Map:
    def __init__(self, stage):
        self.bg_size = self.width, self.height = 32 * 32, 30 * 32
        self.rows = 30
        self.cols = 32
        pygame.init()
        pygame.mixer.init()
        # 关卡数
        self.stage = stage

        self.load_map_from_file()
        self.generate_land_set()

    # 产生管理地形的集合
    def generate_land_set(self):
        self.borders = pygame.sprite.Group()
        self.ices = pygame.sprite.Group()
        self.irons = pygame.sprite.Group()
        self.jungles = pygame.sprite.Group()
        self.seas = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.blanks = pygame.sprite.Group()
        self.commanders = pygame.sprite.Group()
        for row_num in range(self.rows):
            for col_num in range(self.cols):
                str_map = self.round[row_num][col_num]
                # 基地
                if str_map in ["C8", "CA", "C9", "CB"]:
                    if str_map == "C8":
                        commander = Commander()
                        commander.rect.left, commander.rect.top = \
                            Coordinate.xy_to_left_top_pixel(row_num, col_num)
                        self.commanders.add(commander)
                    continue

                # 边界
                if str_map == "11":
                    border = Border()
                    border.rect.left, border.rect.top = \
                        Coordinate.xy_to_left_top_pixel(row_num, col_num)
                    self.borders.add(border)

                # 铁
                elif str_map == "10":
                    iron = Iron()
                    iron.rect.left, iron.rect.top = \
                        Coordinate.xy_to_left_top_pixel(row_num, col_num)
                    self.irons.add(iron)

                # 海洋
                elif str_map == "12":
                    sea = Sea()
                    sea.rect.left, sea.rect.top = \
                        Coordinate.xy_to_left_top_pixel(row_num, col_num)
                    self.seas.add(sea)

                # 丛林
                elif str_map == "22":
                    jungle = Jungle()
                    jungle.rect.left, jungle.rect.top = \
                        Coordinate.xy_to_left_top_pixel(row_num, col_num)
                    self.jungles.add(jungle)

                # 冰面
                elif str_map == "21":
                    ice = Ice()
                    ice.rect.left, ice.rect.top = \
                        Coordinate.xy_to_left_top_pixel(row_num, col_num)
                    self.ices.add(ice)

                # 空地
                elif str_map == "00":
                    blank = Blank()
                    blank.rect.left, blank.rect.top = \
                        Coordinate.xy_to_left_top_pixel(row_num, col_num)
                    self.blanks.add(blank)

                # 前面
                elif str_map[0] == "0":
                    wall = Wall()
                    wall.rect.left, wall.rect.top = \
                        Coordinate.xy_to_left_top_pixel(row_num, col_num)
                    if ord(str_map[1]) >= ord('A'):
                        wall.state = ord(str_map[1]) - ord('A') + 10
                    else:
                        wall.state = int(str_map[1])
                    self.walls.add(wall)

                # 其它地形情况,将此地形更新为空地
                else:
                    self.round[row_num][col_num] = "00"
                    blank = Blank()
                    blank.rect.left, blank.rect.top = \
                        Coordinate.xy_to_left_top_pixel(row_num, col_num)
                    self.blanks.add(blank)

    # 加载文件中的地图, 存储在round 的二维列表中
    def load_map_from_file(self):
        tmp_line = None
        line_num = 0
        for line in open("../Map/map.txt"):
            if line_num == self.stage:
                line = line.strip("\r\n")
                tmp_line = line
                break
            line_num += 1
        tmp_line = tmp_line.split(" ")

        self.round = []

        index = 0
        for row_num in range(self.rows):
            list_each_row = []
            for col_num in range(self.cols):
                str_map = tmp_line[index]
                index += 1
                list_each_row.append(str_map)
            self.round.append(list_each_row)

    # 在界面的更新 显示
    def display_update(self, screen, delay):
        # 清空无效的 墙体和铁块
        for wall in self.walls:
            if wall.state == 0:
                self.walls.remove(wall)

        for iron in self.irons:
            if iron.state == 0:
                self.irons.remove(iron)

        all_lands = [self.borders,
                     self.ices,
                     self.jungles,
                     self.seas,
                     self.walls,
                     self.irons,
                     self.commanders
                     ]
        for lands in all_lands:
            if lands == self.jungles:
                continue
            if lands == self.seas:
                for land in lands:
                    land.display(screen, delay)
                continue
            for land in lands:
                land.display(screen)

    # 更新草丛
    def display_jungle(self, screen):
        for jungle in self.jungles:
            jungle.display(screen)

    # 地形碰撞检测
    def check_land_collide(self, try_move_tank):
        # 若和地形有碰撞,返回 False
        if len(pygame.sprite.spritecollide(try_move_tank, self.borders, False)) > 0:
            return False
        if len(pygame.sprite.spritecollide(try_move_tank, self.seas, False)) > 0:
            return False
        if len(pygame.sprite.spritecollide(try_move_tank, self.commanders, False)) > 0:
            return False
        if len(pygame.sprite.spritecollide(try_move_tank, self.irons, False)) > 0:
            collide_irons = pygame.sprite.spritecollide(try_move_tank, self.irons, False)
            for collide_iron in collide_irons:
                if collide_iron.state == 1:
                    return False
        if len(pygame.sprite.spritecollide(try_move_tank, self.walls, False)) > 0:
            collide_walls = pygame.sprite.spritecollide(try_move_tank, self.walls, False)
            collide_group = pygame.sprite.Group()
            for collide_wall in collide_walls:
                # 左上
                state = collide_wall.state
                if (state & 1) > 0:
                    blank = Blank_16()
                    blank.rect.left, blank.rect.top = collide_wall.rect.left, collide_wall.rect.top
                    collide_group.add(blank)

                # 右上
                if (state & 2) > 0:
                    blank = Blank_16()
                    blank.rect.left, blank.rect.top = \
                        collide_wall.rect.left + collide_wall.rect.width // 2, collide_wall.rect.top
                    collide_group.add(blank)

                # 左下
                if (state & 4) > 0:
                    blank = Blank_16()
                    blank.rect.left, blank.rect.top = \
                        collide_wall.rect.left, collide_wall.rect.top + collide_wall.rect.height // 2
                    collide_group.add(blank)

                # 右下
                if (state & 8) > 0:
                    blank = Blank_16()
                    blank.rect.left, blank.rect.top = collide_wall.rect.left + collide_wall.rect.width // 2, \
                                                      collide_wall.rect.top + collide_wall.rect.height // 2
                    collide_group.add(blank)

            if len(pygame.sprite.spritecollide(try_move_tank, collide_group, False)) > 0:
                return False

        return True

    def check_bullet_collide(self, tank_bullet):
        # 子弹碰撞
        if len(pygame.sprite.spritecollide(tank_bullet, self.borders, False)) > 0:
            return False
        if len(pygame.sprite.spritecollide(tank_bullet, self.commanders, False)) > 0:
            for commander in self.commanders:
                commander.hp -= tank_bullet.power
                if commander.hp <= 0:
                    commander.image = commander.image_commander1
            return False

        if len(pygame.sprite.spritecollide(tank_bullet, self.jungles, False)) > 0:
            if tank_bullet.power >= 2:
                pygame.sprite.spritecollide(tank_bullet, self.jungles, True)
                return False

        if len(pygame.sprite.spritecollide(tank_bullet, self.irons, False)) > 0:
            collide_irons = pygame.sprite.spritecollide(tank_bullet, self.irons, False)
            if tank_bullet.power == 2:
                is_ok = True
                for collide_iron in collide_irons:
                    if collide_iron.state == 1:
                        collide_iron.state = 0
                        is_ok = False
                if not is_ok:
                    return False

            elif tank_bullet.power == 1:
                for collide_iron in collide_irons:
                    if collide_iron.state == 1:
                        return False

        if len(pygame.sprite.spritecollide(tank_bullet, self.walls, False)) > 0:
            collide_walls = pygame.sprite.spritecollide(tank_bullet, self.walls, False)

            if tank_bullet.image == tank_bullet.image_bullet_up:
                # 子弹是否存活
                is_ok = True
                for collide_wall in collide_walls:
                    if (collide_wall.state & 4) or (collide_wall.state & 8):
                        if self.check_small_collision(collide_wall, 4 + 8, tank_bullet):
                            if (collide_wall.state & 4) > 0:
                                collide_wall.state -= 4
                            if (collide_wall.state & 8) > 0:
                                collide_wall.state -= 8
                            is_ok = False
                    elif (collide_wall.state & 1) or (collide_wall.state & 2):
                        if self.check_small_collision(collide_wall, 1 + 2, tank_bullet):
                            if (collide_wall.state & 1) > 0:
                                collide_wall.state -= 1
                            if (collide_wall.state & 2) > 0:
                                collide_wall.state -= 2
                            is_ok = False
                return is_ok

            elif tank_bullet.image == tank_bullet.image_bullet_down:
                is_ok = True
                for collide_wall in collide_walls:
                    if (collide_wall.state & 1) or (collide_wall.state & 2):
                        if self.check_small_collision(collide_wall, 1 + 2, tank_bullet):
                            if (collide_wall.state & 1) > 0:
                                collide_wall.state -= 1
                            if (collide_wall.state & 2) > 0:
                                collide_wall.state -= 2
                            is_ok = False
                    elif (collide_wall.state & 4) or (collide_wall.state & 8):
                        if self.check_small_collision(collide_wall, 4 + 8, tank_bullet):
                            if (collide_wall.state & 4) > 0:
                                collide_wall.state -= 4
                            if (collide_wall.state & 8) > 0:
                                collide_wall.state -= 8
                            is_ok = False
                return is_ok

            elif tank_bullet.image == tank_bullet.image_bullet_left:
                is_ok = True
                for collide_wall in collide_walls:
                    if (collide_wall.state & 2) or (collide_wall.state & 8):
                        if self.check_small_collision(collide_wall, 2 + 8, tank_bullet):
                            if (collide_wall.state & 2) > 0:
                                collide_wall.state -= 2
                            if (collide_wall.state & 8) > 0:
                                collide_wall.state -= 8
                            is_ok = False
                    elif (collide_wall.state & 1) or (collide_wall.state & 4):
                        if self.check_small_collision(collide_wall, 1 + 4, tank_bullet):
                            if (collide_wall.state & 1) > 0:
                                collide_wall.state -= 1
                            if (collide_wall.state & 4) > 0:
                                collide_wall.state -= 4
                            is_ok = False
                return is_ok

            elif tank_bullet.image == tank_bullet.image_bullet_right:
                is_ok = True
                for collide_wall in collide_walls:
                    if (collide_wall.state & 1) or (collide_wall.state & 4):
                        if self.check_small_collision(collide_wall, 1 + 4, tank_bullet):
                            if (collide_wall.state & 1) > 0:
                                collide_wall.state -= 1
                            if (collide_wall.state & 4) > 0:
                                collide_wall.state -= 4
                            is_ok = False
                    elif (collide_wall.state & 2) or (collide_wall.state & 8):
                        if self.check_small_collision(collide_wall, 2 + 8, tank_bullet):
                            if (collide_wall.state & 2) > 0:
                                collide_wall.state -= 2
                            if (collide_wall.state & 8) > 0:
                                collide_wall.state -= 8
                            is_ok = False
                return is_ok

        return True

    def check_small_collision(self, collide_wall, collide_wall_part_state, tank_bullet):
        collide_group = pygame.sprite.Group()
        # 左上
        state = collide_wall_part_state
        if (state & 1) > 0:
            blank = Blank_16()
            blank.rect.left, blank.rect.top = collide_wall.rect.left, collide_wall.rect.top
            collide_group.add(blank)

        # 右上
        if (state & 2) > 0:
            blank = Blank_16()
            blank.rect.left, blank.rect.top = \
                collide_wall.rect.left + collide_wall.rect.width // 2, collide_wall.rect.top
            collide_group.add(blank)

        # 左下
        if (state & 4) > 0:
            blank = Blank_16()
            blank.rect.left, blank.rect.top = \
                collide_wall.rect.left, collide_wall.rect.top + collide_wall.rect.height // 2
            collide_group.add(blank)

        # 右下
        if (state & 8) > 0:
            blank = Blank_16()
            blank.rect.left, blank.rect.top = collide_wall.rect.left + collide_wall.rect.width // 2, \
                                              collide_wall.rect.top + collide_wall.rect.height // 2
            collide_group.add(blank)

        if len(pygame.sprite.spritecollide(tank_bullet, collide_group, False)) > 0:
            return True
        else:
            return False

    def check_missile_collide(self, tank_missile):
        if len(pygame.sprite.spritecollide(tank_missile, self.borders, False)) > 0:
            return False
        return True
