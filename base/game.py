import pygame
import random
import sys
import time

sys.path.append('../base')

from base.config import setting, window_height, window_width, frame_rate
from base.enemy import EnemyType1,EnemyType2, EnemyType3
from base.missile import Missile
from base.animation import Animation
from base.shared_lib import t
from util import out_of_screen, distance_between


class Game:
    def __init__(self, game_id, difficulty='easy'):
        self.state = 'running'
        self.game_id = game_id
        self.enemies = []
        self.players = {}
        self.hostile_bullets = []
        self.missile = []
        self.friendly_bullets = []
        self.props = []
        self.running_state = False
        self.difficult = difficulty
        self.start_time = time.time()

        self.current_time = self.start_time
        self.pause_time_point = self.current_time
        self.recover_from_pause = False
        self.timer = {
            'game_tick': 0,
            'enemy_spawn': 0,
        }

        self.random = random.Random()
        self.random.seed(self.current_time)

        self.animation = {
            'hostile_bullet_explosion': [],
            'friendly_bullet_explosion': [],
            'enemy_catch_fire': [],
            'enemy_explosion': [],
        }

    def enemy_spawn(self, pos=(0, 0), enemy_type=1):
        # 随机生成一个敌机种类
        # enemy_type = self.random.randint(1,2)
        if pos == (0, 0):
            pos = self.random.randint(0, window_width - 100), 30
        if self.timer['enemy_spawn'] > setting[self.difficult]['enemy_spawn_time']:
            ch = random.randint(1, 2)
            temp = None
            if ch == 1:
                temp = EnemyType2(
                    basic_setting={
                        'x': pos[0],
                        'y': pos[1],
                        'size': t.lib['GREEN_SPACE_SHIP'].get_size(),
                        'texture_name': 'GREEN_SPACE_SHIP'
                    },
                    inertia_setting={
                        'max_speed': 2
                    },
                    plane_setting={
                        'health': setting[self.difficult]['enemy_health']['enemy_1']
                    },
                    enemy_setting={
                        'fire_cool_down_frame': 45,
                    },
                )
                temp.init_move((0, 2))
            elif ch == 2:
                temp = EnemyType3(
                    basic_setting={
                        'x': pos[0],
                        'y': pos[1],
                        'size': t.lib['GREEN_SPACE_SHIP'].get_size(),
                        'texture_name': 'GREEN_SPACE_SHIP'
                    },
                    inertia_setting={
                        'max_speed': 2
                    },
                    plane_setting={
                        'health': setting[self.difficult]['enemy_health']['enemy_1']
                    },
                    enemy_setting={
                        'fire_cool_down_frame': 90,
                    },
                )
                temp.init_move((0, 2))
            self.enemies.append(temp)
            self.timer['enemy_spawn'] = 0

    def update_timer(self):
        # 推算自从上次update以来经过的时间，并更新所有寄存器的值
        time_past = time.time() - self.current_time
        self.current_time = time.time()
        if self.recover_from_pause:
            self.recover_from_pause = False
            time_past = 0
            for key, value in self.timer.items():
                self.timer[key] += time_past
            # print(self.timer)
        else:
            for key, value in self.timer.items():
                self.timer[key] += time_past
        return self.timer['game_tick']

    def enemy_move(self):
        for enemy in self.enemies:
            enemy.update()

    def enemy_shoot(self):
        for enemy in self.enemies:
            flag, b = enemy.shoot(self.players)
            if flag:
                self.hostile_bullets.append(b)

    def player_shoot(self):
        for key, value in self.players.items():
            flag, b = value.shoot()
            if flag:
                self.friendly_bullets.append(b)

    def player_self_defense(self):
        for key, player in self.players.items():
            missile_list = []
            for b in self.hostile_bullets:
                if isinstance(b, Missile):
                    missile_list.append(b)
            distance_list = []

            if len(missile_list) == 0:
                player.defense_laser.set_target(None)
            else:
                for m in missile_list:
                    distance_list.append(distance_between(player.get_center(), m.get_center()))
                min_distance = 1E6
                index_min = None
                for index, distance in enumerate(distance_list):
                    if distance < min_distance:
                        min_distance = distance
                        index_min = index
                if index_min is not None:
                    player.defense_laser.set_target(missile_list[index_min])
            player.defense_laser.update()



    def ouf_of_boarder_handler(self):
        for enemy in self.enemies:
            # 说明已经飞出屏幕
            if enemy.get_center()[1] > window_height + 100:
                self.enemies.remove(enemy)

        for b in self.hostile_bullets:
            if isinstance(b, Missile):
                if out_of_screen(b):
                    self.hostile_bullets.remove(b)
            elif out_of_screen(b):
                self.hostile_bullets.remove(b)

        for b in self.friendly_bullets:
            if out_of_screen(b):
                self.friendly_bullets.remove(b)

    def collision_detection(self):
        for p_id, player in self.players.items():
            player_mask = pygame.mask.from_surface(t.lib[player.texture_name])
            for h_bullet in self.hostile_bullets:
                bullet_mask = pygame.mask.from_surface(t.lib[h_bullet.texture_name])
                if self.collide(player, h_bullet, player_mask, bullet_mask):
                    self.get_hit(player, h_bullet.damage)
                    self.hostile_bullets.remove(h_bullet)

        for enemy in self.enemies:
            enemy_mask = pygame.mask.from_surface(t.lib[enemy.texture_name])
            for f_bullet in self.friendly_bullets:
                bullet_mask = pygame.mask.from_surface(t.lib[f_bullet.texture_name])
                if self.collide(enemy, f_bullet, enemy_mask, bullet_mask):
                    self.get_hit(enemy, f_bullet.damage)
                    self.friendly_bullets.remove(f_bullet)
        for p_id, player in self.players.items():
            player_mask = pygame.mask.from_surface(t.lib[player.texture_name])
            for enemy in self.enemies:
                enemy_mask = pygame.mask.from_surface(t.lib[enemy.texture_name])
                if self.collide(player, enemy,player_mask, enemy_mask):
                    self.instant_die(enemy)


    @staticmethod
    def collide(obj1, obj2, mask1, mask2):
        offset_x = obj2.x - obj1.x
        offset_y = obj2.y - obj1.y
        return mask1.overlap(mask2, (offset_x, offset_y)) != None

    @staticmethod
    def get_hit(plane_obj, amount):
        plane_obj.hit(amount)

    @staticmethod
    def instant_die(plane_obj):
        plane_obj.health = 0

    def hostile_bullets_move(self):
        for b in self.hostile_bullets:
            if isinstance(b, Missile):
                self.detect_missile_expire(b)
                if self.missile_die_detection(b):
                    self.hostile_bullets.remove(b)
            b.update()

    def friendly_bullets_move(self):
        for b in self.friendly_bullets:
            b.update()

    def enemy_die_detection(self):
        for enemy in self.enemies:
            if enemy.health <= 0:
                temp = Animation(enemy.get_center(), (0, 0), 'explosion1')
                self.animation['enemy_explosion'].append(temp)
                self.enemies.remove(enemy)

    def player_failed_detection(self):
        pass

    def update_animation(self):
        for key, animate_list in self.animation.items():
            for animate in animate_list:
                animate.update()

    def detect_animation_expire(self):
        for key, animate_list in self.animation.items():
            for animate in animate_list:
                if animate.counter >= animate.length:
                    self.animation[key].remove(animate)

    def detect_missile_expire(self, missile):
            if missile.life_time < 0:
                missile.fuel = False

    def missile_die_detection(self, missile):
        if missile.health <= 0:
            return True

    @staticmethod
    def obj_keep_in_screen(obj):
        for key, value in obj.items():
            if value.x < 0:
                obj[key].x = 0
                obj[key].vx = 0
            if value.x + value.width > window_width:
                obj[key].x = window_width - value.width
                obj[key].vx = 0
            if value.y < 0:
                obj[key].y = 0
                obj[key].vy = 0
            if value.y + value.height > window_height:
                obj[key].y = window_height - value.height
                obj[key].vy = 0

    def update(self):
        game_tick = self.update_timer()
        if game_tick < 1 / frame_rate:
            return
        self.timer['game_tick'] = 0
        self.obj_keep_in_screen(self.players)
        self.enemy_spawn()
        self.enemy_move()
        self.enemy_shoot()
        self.hostile_bullets_move()

        self.player_shoot()
        self.friendly_bullets_move()

        self.collision_detection()
        self.enemy_die_detection()

        self.update_animation()
        self.detect_animation_expire()

        self.player_self_defense()

        self.ouf_of_boarder_handler()

