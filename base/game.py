import pygame
import random
import sys
import time

sys.path.append('../base')

from base.config import setting, window_height, window_width, frame_rate
from base.enemy import EnemyType1, EnemyType2, EnemyType3
from base.missile import Missile
from base.boss import BossType1
from base.prop import Prop, PropType
from base.animation import Animation
from base.shared_lib import t
from base.score import add_score
from util import out_of_screen, distance_between


def detect_missile_expire(missile):
    if missile.life_time < 0:
        missile.fuel = False


def missile_die_detection(missile):
    if missile.health <= 0:
        return True


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
        self.bosses = []
        self.sound_list = []

        self.running_state = False
        self.pause_owner = ''

        self.difficult = difficulty
        self.start_time = time.time()

        self.current_time = self.start_time
        self.pause_time_point = self.current_time
        self.recover_from_pause = False
        self.timer = {
            'game_tick': 0,
            'enemy_spawn': 0,
            'boss_spawn': 100,
            'prop_spawn': 10,
        }
        self.item_counter = {
            'enemy': 30,
            'boss': 1
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
        if self.timer['enemy_spawn'] > setting[self.difficult]['enemy_spawn_time'] and self.item_counter['enemy'] != 0:
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
                        'last_fire': 40,
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
                        'last_fire': 80
                    },
                )
                temp.init_move((0, 2))
            self.enemies.append(temp)
            self.timer['enemy_spawn'] = 0

    def boss_spawn(self, pos=(0, 0)):
        if pos == (0, 0):
            pos = self.random.randint(0, window_width - 100), 30
        if self.timer['boss_spawn'] > setting[self.difficult]['boss_spawn_time'] and self.item_counter['boss'] != 0:
            ch = random.randint(1, 1)
            temp = None
            if ch == 1:
                temp = BossType1(
                    basic_setting={
                        'x': pos[0],
                        'y': pos[1],
                        'size': t.lib['BOSS_1'].get_size(),
                        'texture_name': 'BOSS_1'
                    },
                    inertia_setting={
                        'max_speed': 0.5
                    },
                    plane_setting={
                        'health': setting[self.difficult]['boss_health']['boss_1']
                    },
                    boss_setting={
                        'fire_cool_down_frame': 45,
                        'last_fire': 0,
                    },
                )
            self.bosses.append(temp)
            self.timer['boss_spawn'] = 0

    def prop_spawn(self, pos=(0, 0)):
        if pos == (0, 0):
            pos = self.random.randint(0, window_width - 100), self.random.randint(window_height / 3,
                                                                                  window_height * 2 / 3)
        if self.timer['prop_spawn'] > setting[self.difficult]['prop_spawn_time']:
            ch = random.randint(1, 3)
            temp = Prop(
                basic_setting={
                    'x': pos[0],
                    'y': pos[1],
                    'size': t.lib[PropType(ch).name].get_size(),
                    'texture_name': PropType(ch).name
                },
                prop_setting={
                    'type': PropType(ch),
                    'designate_keep_time': 180,
                },
            )
            init_move_vector = self.random.random(), self.random.random()
            temp.init_move(init_move_vector)
            self.props.append(temp)
            self.timer['prop_spawn'] = 0

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

    def boss_move(self):
        for boss in self.bosses:
            boss.update()

    def prop_move(self):
        for prop in self.props:
            prop.update()

    def enemy_shoot(self):
        for enemy in self.enemies:
            flag, b = enemy.shoot(self.players)
            if flag:
                self.hostile_bullets.append(b)

    def boss_shoot(self):
        for boss in self.bosses:
            flag, b = boss.shoot(self.players)
            if flag:
                self.hostile_bullets.append(b)

    def player_shoot(self):
        for key, value in self.players.items():
            flag, b = value.shoot()
            if flag:
                self.friendly_bullets.append(b)
                self.sound_list.append('player_shoot')

    def player_self_defense(self):
        for key, player in self.players.items():
            if player.state == 'dead':
                continue
            missile_list = []
            for b in self.hostile_bullets:
                if isinstance(b, Missile):
                    missile_list.append(b)
            distance_list = []

            if len(missile_list) == 0:
                player.set_target(None)
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
                    player.set_target(missile_list[index_min])
            player.update()

    @staticmethod
    def obj_move(obj):
        obj.update()

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

        for prop in self.props:
            if out_of_screen(prop):
                self.props.remove(prop)

    def collision_detection(self):
        # 己方飞机被敌方子弹击中的结算逻辑
        for p_id, player in self.players.items():
            if player.state == 'dead':
                continue
            player_mask = pygame.mask.from_surface(t.lib[player.texture_name])
            for h_bullet in self.hostile_bullets:
                bullet_mask = pygame.mask.from_surface(t.lib[h_bullet.texture_name])
                if self.collide(player, h_bullet, player_mask, bullet_mask):
                    self.get_hit(player, h_bullet.damage)
                    self.hostile_bullets.remove(h_bullet)

        # 敌方飞机被己方子弹击中的计算逻辑
        for enemy in self.enemies:
            enemy_mask = pygame.mask.from_surface(t.lib[enemy.texture_name])
            for f_bullet in self.friendly_bullets:
                bullet_mask = pygame.mask.from_surface(t.lib[f_bullet.texture_name])
                if self.collide(enemy, f_bullet, enemy_mask, bullet_mask):
                    self.get_hit(enemy, f_bullet.damage)
                    if enemy.health == 0:
                        assert f_bullet.belonging is not None
                        f_bullet.belonging.game_score += enemy.score
                    self.friendly_bullets.remove(f_bullet)

        # 己方子弹击中敌方Boss的结算逻辑
        for boss in self.bosses:
            boss_mask = pygame.mask.from_surface(t.lib[boss.texture_name])
            for f_bullet in self.friendly_bullets:
                bullet_mask = pygame.mask.from_surface(t.lib[f_bullet.texture_name])
                if self.collide(boss, f_bullet, boss_mask, bullet_mask):
                    self.get_hit(boss, f_bullet.damage)
                    if boss.health == 0:
                        assert f_bullet.belonging is not None
                        f_bullet.belonging.game_score += boss.score
                    self.friendly_bullets.remove(f_bullet)

        # 敌方飞机和我方飞机相撞检测
        for p_id, player in self.players.items():
            if player.state == 'dead':
                continue
            player_mask = pygame.mask.from_surface(t.lib[player.texture_name])
            for enemy in self.enemies:
                enemy_mask = pygame.mask.from_surface(t.lib[enemy.texture_name])
                if self.collide(player, enemy, player_mask, enemy_mask):
                    self.instant_die(enemy)

        # 敌方boss和我方飞机相撞检测
        for p_id, player in self.players.items():
            if player.state == 'dead':
                continue
            player_mask = pygame.mask.from_surface(t.lib[player.texture_name])
            for boss in self.enemies:
                boss_mask = pygame.mask.from_surface(t.lib[boss.texture_name])
                if self.collide(player, boss, player_mask, boss_mask):
                    self.instant_die(boss)

        # 我方飞机捡起道具的检测
        for p_id, player in self.players.items():
            if player.state == 'dead':
                continue
            player_mask = pygame.mask.from_surface(t.lib[player.texture_name])
            for prop in self.props:
                prop_mask = pygame.mask.from_surface(t.lib[prop.texture_name])
                if self.collide(player, prop, player_mask, prop_mask):
                    self.prop_make_effect(prop, player)
                    self.sound_list.append('get_prop')
                    self.props.remove(prop)

    @staticmethod
    def prop_make_effect(prop, player):
        if prop.type == PropType.HEALTH_UP:
            player.hit(-1)
        if prop.type == PropType.DAMAGE_UP:
            player.damage_factor *= 1.2
        if prop.type == PropType.SHOOTING_SPEED_UP:
            player.fire_cool_down_frame *= 0.8

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
                detect_missile_expire(b)
                if missile_die_detection(b):
                    self.hostile_bullets.remove(b)
            b.update()

    def friendly_bullets_move(self):
        for b in self.friendly_bullets:
            b.update()

    def enemy_die_detection(self):
        for enemy in self.enemies:
            if enemy.health <= 0:
                temp = Animation(enemy.get_center(), (0, 0), 'explosion1')
                self.item_counter['enemy'] -= 1
                self.sound_list.append('death')
                self.animation['enemy_explosion'].append(temp)
                self.enemies.remove(enemy)

    def boss_die_detection(self):
        for boss in self.bosses:
            if boss.health <= 0:
                temp = Animation(boss.get_center(), (0, 0), 'explosion1')
                self.item_counter['boss'] -= 1
                self.animation['enemy_explosion'].append(temp)
                self.bosses.remove(boss)

    def player_failed_detection(self):
        for p_id, player in self.players.items():
            if player.health <= 0:
                player.state = 'dead'

    def update_animation(self):
        for key, animate_list in self.animation.items():
            for animate in animate_list:
                animate.update()

    def detect_animation_expire(self):
        for key, animate_list in self.animation.items():
            for animate in animate_list:
                if animate.counter >= animate.length:
                    self.animation[key].remove(animate)

    def detect_prop_expire(self):
        for prop in self.props:
            if prop.keep_time > prop.designate_keep_time:
                self.props.remove(prop)

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

    def refresh_sound_list(self):
        self.sound_list = []

    def global_state_update(self):
        # 检测场上是否还有玩家存活
        alive_num = 0
        for p_id, player in self.players.items():
            if player.state == 'alive':
                alive_num += 1
        if alive_num == 0:
            self.state = 'lose'

        # 检测是否所有敌人都被消灭
        enemy_left = False
        for key, value in self.item_counter.items():
            if value != 0:
                enemy_left = True
                break

        if not enemy_left:
            self.state = 'win'

    def update(self):
        game_tick = self.update_timer()
        if game_tick < 1 / frame_rate:
            return
        self.timer['game_tick'] = 0
        self.refresh_sound_list()
        self.obj_keep_in_screen(self.players)
        self.enemy_spawn()
        self.boss_spawn()

        self.enemy_move()
        self.enemy_shoot()

        self.boss_move()
        self.boss_shoot()

        self.prop_spawn()
        self.prop_move()
        self.detect_prop_expire()

        self.hostile_bullets_move()

        self.player_shoot()
        self.friendly_bullets_move()

        self.collision_detection()
        self.enemy_die_detection()
        self.boss_die_detection()

        self.update_animation()
        self.detect_animation_expire()

        self.player_self_defense()

        self.ouf_of_boarder_handler()

        self.player_failed_detection()

        self.global_state_update()
