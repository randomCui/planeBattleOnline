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


class Game:
    def __init__(self, game_id, difficulty='easy'):
        # 游戏运行状态
        self.state = 'running'
        # 本局游戏对应的游戏id
        self.game_id = game_id
        # 游戏中普通敌人列表
        self.enemies = []
        # 游戏中玩家字典
        self.players = {}
        # 游戏中敌方子弹的子弹
        self.hostile_bullets = []
        # 游戏中导弹对象的列表(好像也没用到)
        self.missile = []
        # 己方子弹的列表
        self.friendly_bullets = []
        # 游戏中道具列表
        self.props = []
        # 游戏中Boss列表
        self.bosses = []
        # 游戏中声效列表
        self.sound_list = []
        # 保存游戏中动画对象的字典
        self.animation = {
            'hostile_bullet_explosion': [],
            'friendly_bullet_explosion': [],
            'enemy_catch_fire': [],
            'enemy_explosion': [],
        }

        # 提出暂停请求的玩家id
        self.pause_owner = ''

        # 游戏难度
        self.difficult_lock = False
        self.difficult = difficulty

        # 游戏开始时间，用于游戏中计时器的操作
        self.start_time = time.time()

        # 当前时间，用于游戏中计时器的更新
        self.current_time = self.start_time
        # 暂停时间点，用于从暂停中恢复的相关操作
        self.pause_time_point = self.current_time
        # 本次更新是否是从暂停中更新的
        self.recover_from_pause = False

        # 游戏中的定时器
        self.timer = {
            'game_tick': 0,
            'enemy_spawn': 0,
            'boss_spawn': 0,
            'prop_spawn': 0,
        }

        # 敌人数量计数器，用于控制敌人生成
        self.item_counter = {
            'enemy': 30,
            'boss': 1
        }
        self.item_left_counter = {
            'enemy': 30,
            'boss': 1,
        }

        # 每局游戏对应的背景应该播放到的帧数
        self.background_frame = 0
        # 计算帧率的分频器
        self.background_frame_counter = 0
        # 是否将背景动画倒着播放
        self.reverse = False

        # 每局游戏对应的随机数生成器
        self.random = random.Random()
        self.random.seed(self.current_time)

    def enemy_spawn(self, pos=(0, 0)):
        # 随机生成一个敌机种类
        # 如果没有指定生成位置，就随机生成一个
        if pos == (0, 0):
            pos = self.random.randint(0, window_width - 100), 30
        # 如果生成敌机的间隔已经达到，并且还有剩余的敌机要生成
        if self.timer['enemy_spawn'] > setting[self.difficult]['enemy_spawn_time'] and self.item_counter['enemy'] != 0:
            # 将生成间隔定时器清零
            self.timer['enemy_spawn'] = 0
            # 将应该生成的敌人数量-1
            self.item_counter['enemy'] -= 1
            # 随机从两种类型的敌机中选择一种
            ch = random.randint(1, 2)
            temp = None
            if ch == 1:
                # 根据参数生成一个敌机对象
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
                # 初始化敌机的移动方式
                temp.init_move((0, 2))
            elif ch == 2:
                # 根据参数生成一个敌机对象
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
                # 初始化敌机的移动方式
                temp.init_move((0, 2))
            # 将新生成的敌机添加到游戏中保存敌机的列表中去
            self.enemies.append(temp)

    def boss_spawn(self, pos=(0, 0)):
        # 具体的生成逻辑和上面生成敌机的基本相同，这里不再赘述
        if pos == (0, 0):
            # 随机生成在屏幕的上1/3部分
            pos = self.random.randint(0, window_width - 100), 30
        if (self.timer['boss_spawn'] > setting[self.difficult]['boss_spawn_time'] or self.item_counter['enemy'] < 6)\
                and self.item_counter['boss'] != 0:
            self.timer['boss_spawn'] = 0
            self.item_counter['boss'] -= 1
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
                        'max_speed': 2
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

    def prop_spawn(self, pos=(0, 0)):
        # 基本的生成逻辑和生成敌机类似，不再赘述
        if pos == (0, 0):
            pos = self.random.randint(0, window_width - 100), self.random.randint(window_height / 3,
                                                                                  window_height * 2 / 3)
        if self.timer['prop_spawn'] > setting[self.difficult]['prop_spawn_time']:
            self.timer['prop_spawn'] = 0
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

    def update_timer(self):
        """
        推算自从上次update以来经过的时间，并更新所有定时器的值
        :return: 自从上次update之后经过的时间，决定是否要对游戏进行一次更新
        """
        # 计算经过的时间
        time_past = time.time() - self.current_time
        # 设置当前时间
        self.current_time = time.time()
        # 如果本次更新是从暂停中恢复的话
        if self.recover_from_pause:
            self.recover_from_pause = False
            # 就假装中间没有经过任何时间
            time_past = 0
            for key, value in self.timer.items():
                self.timer[key] += time_past
        else:
            for key, value in self.timer.items():
                self.timer[key] += time_past
        return self.timer['game_tick']

    def enemy_move(self):
        # 更新游戏中所有普通敌机对象的位置状态
        for enemy in self.enemies:
            enemy.update()

    def boss_move(self):
        # 更新游戏中所有Boss对象的位置状态
        for boss in self.bosses:
            boss.update()

    def prop_move(self):
        # 更新游戏中所有道具对象的位置状态
        for prop in self.props:
            prop.update()

    def hostile_bullets_move(self):
        # 更新游戏中所有敌方子弹对象的位置状态
        for b in self.hostile_bullets:
            # 如果这个对象是导弹对象
            if isinstance(b, Missile):
                # 检查导弹的动力段是否已经结束，如果结束，就让其切换到无动力滑行状态
                self.detect_missile_expire(b)
            b.update()

    def friendly_bullets_move(self):
        # 更新游戏中所有道具对象的位置状态
        for b in self.friendly_bullets:
            b.update()

    def enemy_shoot(self):
        # 尝试让普通敌人对象射击
        for enemy in self.enemies:
            # 如果flag为True，说明成功生成出了一个子弹
            flag, b = enemy.shoot(self.players)
            # 如果成功发射了子弹
            if flag:
                # 如果是单个子弹，将子弹添加到子弹列表中，如果返回的是一个列表，就逐个添加
                if isinstance(b, list):
                    for bullet in b:
                        self.hostile_bullets.append(bullet)
                else:
                    self.hostile_bullets.append(b)

    def boss_shoot(self):
        # 尝试让Boss对象射击
        for boss in self.bosses:
            # 如果flag为True，说明成功生成出了一个子弹
            flag, b = boss.shoot(self.players)
            # 如果成功发射了子弹
            if flag:
                # 将子弹添加到子弹列表中
                self.hostile_bullets.append(b)

    def player_shoot(self):
        # 尝试让玩家射击
        for key, value in self.players.items():
            # 如果flag为True，说明成功生成出了一个子弹
            flag, b = value.shoot()
            # 如果成功发射了子弹
            if flag:
                # 如果是单个子弹，将子弹添加到子弹列表中，如果返回的是一个列表，就逐个添加
                if isinstance(b, list):
                    for bullet in b:
                        self.friendly_bullets.append(bullet)
                else:
                    self.friendly_bullets.append(b)
                # 增加音效
                self.sound_list.append('player_shoot')

    def player_self_defense(self):
        """
        更新每个玩家的激光防卫系统的状态

        :return:
        """
        # 对于每个玩家
        for key, player in self.players.items():
            # 如果玩家死了，就不更新他的状态
            if player.state == 'dead':
                continue
            # 找到hostile_bullets中所有的导弹对象
            missile_list = []
            for b in self.hostile_bullets:
                if isinstance(b, Missile):
                    missile_list.append(b)

            # 记录导弹离飞机距离
            distance_list = []

            # 如果没有导弹，就将防卫系统的防卫对象设为空
            if len(missile_list) == 0:
                player.set_target(None)
            else:
                # 找出距离最近的导弹
                for m in missile_list:
                    distance_list.append(distance_between(player.get_center(), m.get_center()))
                min_distance = 1E6
                index_min = None
                for index, distance in enumerate(distance_list):
                    if distance < min_distance:
                        min_distance = distance
                        index_min = index
                if index_min is not None:
                    # 将最近的导弹设置为激光射击的目标
                    player.set_target(missile_list[index_min])

            player.update()

    @staticmethod
    # 更新某个游戏内部对象的状态
    def obj_move(obj):
        obj.update()

    def ouf_of_boarder_handler(self):
        """
        处理游戏中出界的对象

        :return:
        """
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
            # 如果玩家已经死了，就忽略它的碰撞检测
            if player.state == 'dead':
                continue
            # 使用mask对象，实现像素级精确的碰撞检测
            player_mask = pygame.mask.from_surface(t.lib[player.texture_name])
            for h_bullet in self.hostile_bullets:
                bullet_mask = pygame.mask.from_surface(t.lib[h_bullet.texture_name])
                # 使用两个mask对象来判断二者是否碰撞
                if self.collide(player, h_bullet, player_mask, bullet_mask):
                    # 如果碰撞，玩家扣血，子弹被摧毁
                    self.get_hit(player, h_bullet.damage)
                    self.hostile_bullets.remove(h_bullet)

        # 敌方飞机被己方子弹击中的计算逻辑，跟上面的逻辑基本上一一致
        for enemy in self.enemies:
            enemy_mask = pygame.mask.from_surface(t.lib[enemy.texture_name])
            for f_bullet in self.friendly_bullets:
                bullet_mask = pygame.mask.from_surface(t.lib[f_bullet.texture_name])
                if self.collide(enemy, f_bullet, enemy_mask, bullet_mask):
                    self.get_hit(enemy, f_bullet.damage)
                    if enemy.health == 0:
                        # 判断这发子弹是哪个玩家射出的
                        assert f_bullet.belonging is not None
                        # 给得到人头的玩家加分
                        f_bullet.belonging.game_score += enemy.score
                    # 子弹被摧毁
                    self.friendly_bullets.remove(f_bullet)

        # 己方子弹击中敌方Boss的结算逻辑，跟上面的计算逻辑一致
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

        # 敌方飞机和我方飞机相撞检测，跟上面的结算逻辑一致
        for p_id, player in self.players.items():
            if player.state == 'dead':
                continue
            player_mask = pygame.mask.from_surface(t.lib[player.texture_name])
            for enemy in self.enemies:
                enemy_mask = pygame.mask.from_surface(t.lib[enemy.texture_name])
                if self.collide(player, enemy, player_mask, enemy_mask):
                    # 如果相撞，普通敌人对象就直接死亡
                    self.instant_die(enemy)

        # 敌方boss和我方飞机相撞检测，跟上面的检测逻辑一致
        for p_id, player in self.players.items():
            if player.state == 'dead':
                continue
            player_mask = pygame.mask.from_surface(t.lib[player.texture_name])
            for boss in self.bosses:
                boss_mask = pygame.mask.from_surface(t.lib[boss.texture_name])
                if self.collide(player, boss, player_mask, boss_mask):
                    self.instant_die(boss)

        # 我方飞机捡起道具的检测
        for p_id, player in self.players.items():
            # 死亡的玩家不能拾取道具
            if player.state == 'dead':
                continue
            player_mask = pygame.mask.from_surface(t.lib[player.texture_name])
            for prop in self.props:
                prop_mask = pygame.mask.from_surface(t.lib[prop.texture_name])
                # 如果捡到了道具
                if self.collide(player, prop, player_mask, prop_mask):
                    # 让子弹给玩家起作用
                    self.prop_make_effect(prop, player)
                    # 添加音效
                    self.sound_list.append('get_prop')
                    # 将道具对象移除
                    self.props.remove(prop)

    @staticmethod
    # 根据不同的道具对象给玩家起到不同的作用
    def prop_make_effect(prop, player):
        if prop.type == PropType.HEALTH_UP:
            player.hit(-1)
        if prop.type == PropType.BULLET_UP:
            player.shooting_pattern = 'shotgun'
        if prop.type == PropType.SHOOTING_SPEED_UP:
            player.fire_cool_down_frame *= 0.8

    @staticmethod
    # 通过两个mask对象判断两个物体是否相撞
    def collide(obj1, obj2, mask1, mask2):
        offset_x = obj2.x - obj1.x
        offset_y = obj2.y - obj1.y
        return mask1.overlap(mask2, (offset_x, offset_y)) != None

    @staticmethod
    # 被击中的物体扣血
    def get_hit(plane_obj, amount):
        plane_obj.hit(amount)

    @staticmethod
    # 被撞击到的敌机直接死亡
    def instant_die(plane_obj):
        plane_obj.health = 0


    def enemy_die_detection(self):
        # 判断游戏中的对象是否死亡
        for enemy in self.enemies:
            if enemy.health <= 0:
                # 如果死亡，就添加死亡动画
                temp = Animation(enemy.get_center(), (0, 0), 'explosion1')
                self.animation['enemy_explosion'].append(temp)

                # 给生成敌人数-1
                self.item_left_counter['enemy'] -= 1
                # 添加音效
                self.sound_list.append('death')

                # 将死亡的敌人移除
                self.enemies.remove(enemy)

    def boss_die_detection(self):
        for boss in self.bosses:
            if boss.health <= 0:
                # 如果死亡，就添加死亡动画
                temp = Animation(boss.get_center(), (0, 0), 'explosion1')
                # 给生成敌人数-1
                self.item_left_counter['boss'] -= 1
                # 添加音效
                self.animation['enemy_explosion'].append(temp)

                self.bosses.remove(boss)

    def player_failed_detection(self):
        # 检测玩家是否死亡
        for p_id, player in self.players.items():
            if player.health <= 0:
                # 如果生命值<=0，就将玩家状态设置为dead
                player.state = 'dead'

    def update_animation(self):
        # 更新哟西中所有动画的状态
        for key, animate_list in self.animation.items():
            for animate in animate_list:
                animate.update()

    def detect_animation_expire(self):
        # 检查是否右动画效果已经播放完毕
        for key, animate_list in self.animation.items():
            for animate in animate_list:
                if animate.counter >= animate.length:
                    # 如果播放完毕，就移除
                    self.animation[key].remove(animate)

    def detect_prop_expire(self):
        # 检查是否右道具对象已经过了出现时间
        for prop in self.props:
            if prop.keep_time > prop.designate_keep_time:
                # 如果已经超过了存活时间，就删除这个道具
                self.props.remove(prop)

    @staticmethod
    def obj_keep_in_screen(obj):
        # 检测其是否在屏幕中
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

    @staticmethod
    def detect_missile_expire(missile):
        # 检查导弹是否还处于动力段，如果不在动力段，那么就改为进入滑行段
        if missile.life_time < 0:
            missile.fuel = False

    def missile_die_detection(self):
        # 检查所有导弹中是否有被摧毁的
        for m in self.hostile_bullets:
            # 如果这个对象是Missile的实例
            if isinstance(m, Missile):
                # 如果health低于0
                if m.health <= 0:
                    # 就将这个导弹移除
                    self.hostile_bullets.remove(m)

    def refresh_sound_list(self):
        # 将音效信息清除
        self.sound_list = []

    def global_state_update(self):
        # 检测场上是否还有玩家存活
        alive_num = 0
        for p_id, player in self.players.items():
            if player.state == 'alive':
                alive_num += 1
        # 如果没有人存活，那么说明这一句游戏已经失败了
        if alive_num == 0:
            self.state = 'lose'

        # 检测是否所有敌人都被消灭
        enemy_left = False
        for key, value in self.item_counter.items():
            if value != 0:
                enemy_left = True
                break
        if len(self.enemies) > 0:
            enemy_left = True
        if len(self.bosses) > 0:
            enemy_left = True

        # 如果所有敌人都被消灭，那么说明本局游戏胜利
        if not enemy_left:
            self.state = 'win'

    def update_background_frame(self):
        # 更新游戏背景的帧数变化
        # 给分频器+1
        self.background_frame_counter += 1
        # 如果到了分频比
        if self.background_frame_counter == 5:
            # 分频器清零
            self.background_frame_counter = 0
            # 根据正向播放还是反向播放来更新帧数
            if not self.reverse:
                self.background_frame+=1
            else:
                self.background_frame-=1
            # 如果帧数要越界
            if self.background_frame<=0 or self.background_frame >= 42:
                # 将播放方向反相
                if self.reverse:
                    self.reverse = False
                else:
                    self.reverse = True

    def update(self):
        # 检查本次更新和上次更新的时间距离
        game_tick = self.update_timer()
        # 如果不足帧率对应的帧时间，就不进行更新
        if game_tick < 1 / frame_rate:
            return
        # 如果更新了，那么将两次更新的间隔置为0
        self.timer['game_tick'] = 0

        self.refresh_sound_list()
        self.obj_keep_in_screen(self.players)

        self.enemy_spawn()
        self.boss_spawn()
        self.prop_spawn()

        self.enemy_move()
        self.enemy_shoot()

        self.boss_move()
        self.boss_shoot()

        self.player_shoot()

        self.prop_move()
        self.detect_prop_expire()

        self.hostile_bullets_move()
        self.friendly_bullets_move()

        self.collision_detection()
        self.enemy_die_detection()
        self.boss_die_detection()
        self.missile_die_detection()

        self.update_animation()
        self.detect_animation_expire()

        self.player_self_defense()

        self.ouf_of_boarder_handler()

        self.player_failed_detection()

        self.global_state_update()
        self.update_background_frame()
