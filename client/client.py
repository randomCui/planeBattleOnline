import os
import sys
from math import degrees

import pygame
import pygame_menu

# 为了导入其他目录的模块，需要先将其他目录的路径加入环境变量中
sys.path.append('..')
sys.path.append('../base')
sys.path.append('../server')

from input_handle import get_input
from audio import Audio
from base.control_key_group import ControlKey
from network import Network
from base.shared_lib import t
from base.animate_lib import animate
from base.config import window_height as height
from base.config import window_width as width
from base.config import sensitivity

# 初始化显示屏幕等
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

# 初始化文字和音频组件
pygame.font.init()
pygame.mixer.init()

# 初始化需要使用到的字体
title_font = pygame.font.SysFont("黑体", 30)
score_font = pygame.font.SysFont("arial", 30)
pause_font = pygame.font.SysFont("arial", 70)
sub_pause_font = pygame.font.SysFont("arial", 40)
nickname_font = pygame.font.SysFont("calibri", 30)

# 初始化客户端信息
# client_number = 0
# 默认参数
# 默认选择的飞船类型
client_texture_name = 'YELLOW_SPACE_SHIP'
# 默认的游戏内名称
client_nickname = ''
# 默认连接的ip
client_ip = 'localhost'
# 默认连接端口
client_port = 11451


def redraw(window, game: 'base.Game'):
    """
    重绘游戏内所有物体

    :param window: 用于显示的pygame surface
    :param game: 存储当前游戏状态的Game对象
    :return:
    """
    draw_players(window, game.players)
    draw_enemies(window, game.enemies)
    draw_hostile_bullets(window, game.hostile_bullets)
    draw_friendly_bullets(window, game.friendly_bullets)
    draw_global_animate(window, game.animation)
    draw_bosses(window, game.bosses)
    draw_props(window, game.props)

    pygame.display.update()


def draw_props(window, props: list):
    """
    重绘游戏中的道具对象

    :param window: 用于绘图的pygame surface
    :param props: Game对象中的道具列表
    :return:
    """
    for prop in props:
        # 由于网络传输的游戏对象都只有元数据，没有带贴图，因此在这里先初始化贴图
        prop.init_texture(t.lib[prop.texture_name])
        # 调用自身方法向屏幕上绘制图形
        prop.draw_self(window)


def draw_global_animate(window, animation: dict):
    """
    绘制游戏中所有的动画对象

    :param window: 用于显示的pygame surface
    :param animation: Game对象中的动画字典
    :return:
    """
    for key, value in animation.items():
        for animate in value:
            animate.draw_self(window)


def draw_hostile_bullets(window, bullets: list):
    """
    绘制游戏中所有的敌方子弹对象

    :param window: 用于显示的pygame surface
    :param bullets: Game对象中的敌方子弹列表
    :return:
    """
    for bullet in bullets:
        # 由于网络传输的游戏对象都只有元数据，没有带贴图，因此在这里先初始化贴图
        bullet.init_texture(t.lib[bullet.texture_name])
        bullet.draw_self(window)


def draw_enemies(window, enemies):
    """
    绘制游戏中的所有普通敌机对象

    :param window: 用于显示的pygame surface
    :param enemies: Game对象中的普通敌机列表
    :return:
    """
    for enemy in enemies:
        enemy.init_texture(t.lib[enemy.texture_name])
        enemy.draw_self(window)


def draw_bosses(window, bosses: list):
    """
    绘制游戏中所有敌方Boss对象

    :param window: 用于显示的pygame surface
    :param bosses: Game对象中的Boss对象列表
    :return:
    """
    for boss in bosses:
        boss.init_texture(t.lib[boss.texture_name])
        boss.draw_self(window)


def draw_players(window, players: dict):
    """
    绘制游戏中所有玩家对象

    :param window: 用于显示的pygame surface
    :param players: Game对象中的玩家对象字典
    :return:
    """
    for p_id, player in players.items():
        if player.state == 'dead':
            continue
        player.init_texture(t.lib[player.texture_name])
        player.draw_self(window)
        title_label = nickname_font.render(player.nickname, True, (255, 255, 255))
        window.blit(title_label, (player.get_center()[0] - title_label.get_width() / 2, player.y - 30))


def draw_ui(window,score):
    """

    :param window: 用于显示的pygame surface
    :param score:
    :return:
    """
    score_text = 'Score: '+str(score)
    title_score = pause_font.render(score_text, True, (255, 255, 255))
    window.blit(title_score, (width - title_score.get_width(), 0))


def draw_pause_window(window):
    """

    :param window: 用于显示的pygame surface
    :return:
    """
    title_pause = pause_font.render("Paused", True, (255, 255, 255))
    window.blit(title_pause, (width / 2 - title_pause.get_width() / 2, 250))
    title_pause = sub_pause_font.render("Press ESC to resume", True, (255, 255, 255))
    window.blit(title_pause, (width / 2 - title_pause.get_width() / 2, 350))
    # pygame.display.update()


def draw_win_screen(window, score):
    """

    :param window: 用于显示的pygame surface
    :param score:
    :return:
    """
    # window.fill(255, 255, 255)
    title_pause = pause_font.render("You Win", True, (255, 255, 255))
    window.blit(title_pause, (width / 2 - title_pause.get_width() / 2, 250))
    hint = "Your score is: " + str(score)
    title_pause = sub_pause_font.render(hint, True, (255, 255, 255))
    window.blit(title_pause, (width / 2 - title_pause.get_width() / 2, 350))
    # pygame.display.update()


def draw_lose_screen(window, score):
    """

    :param window: 用于显示的pygame surface
    :param score:
    :return:
    """
    # window.fill(255, 255, 255)
    title_pause = pause_font.render("You Lose", True, (255, 255, 255))
    window.blit(title_pause, (width / 2 - title_pause.get_width() / 2, 250))
    hint = "Your score is: " + str(score)
    title_pause = sub_pause_font.render(hint, True, (255, 255, 255))
    window.blit(title_pause, (width / 2 - title_pause.get_width() / 2, 350))
    # pygame.display.update()


def draw_friendly_bullets(window, bullets):
    """

    :param window: 用于显示的pygame surface
    :param bullets:
    :return:
    """
    for bullet in bullets:
        rotated_img = pygame.transform.rotate(t.lib[bullet.texture_name], degrees(bullet.angle))
        bullet.init_texture(rotated_img)
        bullet.draw_self(window)


def draw_background(window, frame=0):
    """
    绘制游戏背景部分

    :param window: 用于绘制的pygame surface
    :param frame: 背景动画应该播放到的帧数
    :return:
    """
    window.blit(animate['background'][frame], (0, 0))
    # window.fill((60, 63, 65))


def keep_in_screen_client(player):
    """
    让传入的player对象坐标保持在屏幕内

    :param player: 玩家对象
    :return:
    """
    # 如果玩家的左侧超过屏幕的左侧
    if player.x < 0:
        # 就将左侧限制在屏幕最左边
        player.x = 0
        # 并且将水平运动速度清零
        player.vx = 0
    # 以下同理
    if player.x + player.width > width:
        player.x = width - player.width
        player.vx = 0
    if player.y < 0:
        player.y = 0
        player.vy = 0
    if player.y + player.height > height:
        player.y = height - player.height
        player.vy = 0


class MainMenu:
    """
    游戏的主菜单对象
    """
    def __init__(self, window):
        # 用于绘制的窗口
        self.window = window
        # 玩家的昵称
        self.nickname = client_nickname
        # 玩家所选的飞船
        self.texture_name = 'YELLOW_SPACE_SHIP'

        # 本来这里是选择host或是join模式的开关，但由于逻辑不合，暂时先不用到这个
        # self.mode = False

        # 初始化主菜单对象
        self.menu = pygame_menu.Menu('Main Menu', width, height,
                                     theme=pygame_menu.themes.THEME_BLUE)
        # 初始化昵称输入框
        self.nickname_input = self.menu.add.text_input('Name :', default=client_nickname,
                                                       onchange=self.__update_nickname)
        # 初始化飞机类型显示
        self.plane_preview = self.menu.add.image(
            image_path=t.menu[self.texture_name],
            padding=(25, 0, 0, 0)  # top, right, bottom, left
        )
        # 初始化飞机类型选择选项卡
        self.plane_selector = self.menu.add.selector('Type :', [('Yellow', 1), ('Blue', 2)],
                                                     onchange=self.__update_texture)
        # 初始化ip输入框
        self.ip_input = self.menu.add.text_input('IP address :', default=client_ip, onchange=self.__update_ip_address)
        # 初始化端口输入框
        self.port_input = self.menu.add.text_input('port :', default=client_port, onchange=self.__update_port)
        # 初始化开始游戏输入框
        self.play_button = self.menu.add.button('Play', main_game)
        # 初始化退出按钮输入框
        self.quit_button = self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def __update_texture(self, selected, value: int):
        """
        当飞机选择发生改变时，将对应的显示图案也改变

        :param selected: 表示选项的tuple
        :param value: 选项的Index
        :return:
        """
        # 由于还要和游戏主逻辑进行通信，因此在这里还需要修改全局变量
        global client_texture_name
        # 针对不同的选项填入不同的值
        if value == 1:
            self.texture_name = 'YELLOW_SPACE_SHIP'
            client_texture_name = 'YELLOW_SPACE_SHIP'
        elif value == 2:
            self.texture_name = 'BLUE_SPACE_SHIP'
            client_texture_name = 'BLUE_SPACE_SHIP'
        # 动态改变飞机预览图
        self.plane_preview.set_image(t.menu[self.texture_name])

    def __update_nickname(self, text: str):
        """
        跟游戏昵称输入框进行动态绑定

        :param text: 昵称
        :return:
        """
        # 为了修改全局变量，引入global
        global client_nickname
        self.nickname = text
        client_nickname = text

    def __update_ip_address(self, text: str):
        """
        跟ip地址输入框实现动态绑定

        :param text: 表示ip地址的字符串
        :return:
        """
        global client_ip
        client_ip = text
        pass

    def __update_port(self, text: int):
        """
        跟端口输入框实现动态绑定

        :param text: 表示端口的字符串
        :return:
        """
        global client_port
        client_port = int(text)
        pass

    # def __update_mode(self, mode):
    #     global host_or_join
    #     print(mode)
    #     self.mode = mode
    #     host_or_join = mode

    def mainloop(self):
        """
        pygame-menu包中为了实现主菜单一直显示，需要在初始化结束后调用mainloop让ui界面保持循环
        :return:
        """
        self.menu.mainloop(self.window)


def main_menu():
    # 进入游戏后首先显示主菜单
    pygame.init()
    m = MainMenu(win)
    m.mainloop()


def main_game():
    game_state = 'running'
    # 初始化网络连接
    n = Network(
        ip=client_ip,
        port=client_port,
    )
    # 向服务器发送本客户端的飞机信息
    n.init_player(
        basic_setting={
            'size': t.lib[client_texture_name].get_size(),
            'texture_name': client_texture_name
        },
        inertia_setting={
            'max_speed': 8,
        },
        plane_setting={
            'health': 10,
        },
        player_setting={
            'fire_cool_down_frame': 20,
            'nickname': client_nickname
        }
    )
    # 从服务器拿到本客户端的玩家ID和飞机对象
    ID, p = n.get_local_object()

    # 由于服务端不负责处理贴图，因此在客户端上需要将贴图贴上
    p.init_texture(t.lib[client_texture_name])

    # 初始化一个控制键对象，用于处理切换性按键的操作
    ck = ControlKey()

    # 初始化音频对象，用于播放音乐
    client_audio = Audio()
    client_audio.play_BGM()
    client_audio.pause_BGM()

    # 初始化游戏显示的相关参数
    clock = pygame.time.Clock()

    # 用于游戏采样分频器的计数
    control_counter = 0

    # 开始进入游戏的主循环
    run = True
    while run:
        clock.tick(120)
        for event in pygame.event.get():
            # 如果点击了关闭按钮，就让游戏退出
            if event.type == pygame.QUIT:
                run = False
                n.disconnect()
                pygame.quit()
            # 检测哪个按键被按下了，使用KEYDOWN事件可以避免pressed事件造成的重复触发
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RALT:
                    # 切换右ALT的激活状态，也就是切换鼠标/键盘控制
                    ck.toggle_state('R_ALT')
                elif event.key == pygame.K_ESCAPE:
                    # 切换Esc键的激活状态，也就是切换暂停与否的控制
                    ck.toggle_state('Escape')
                elif event.key == pygame.K_r:
                    # 切换R键的激活状态，也就是控制是否重开游戏
                    ck.toggle_state('R')

        # 由本地输入得到飞机移动的向量 和 飞机是否靠近鼠标位置
        control_report = get_input(p.get_center(), ck.R_ALT)
        # 在飞机的速度矢量上加上之前的移动矢量
        control_report['need_pause'] = ck.Escape
        # 获取飞机的移动状态
        p.change_pos(control_report['move_vector'])
        # 如果在鼠标控制模式下，接近光标位置，就开始增加阻尼，使飞机减速
        if control_report['is_damping']:
            p.damping()

        if control_counter == sensitivity:
            control_counter = 0
            # 结算并更新本地在这个时间点后的飞机位置
            if game_state == 'running':
                p.update()
        control_counter += 1

        # 让对象保持在屏幕中央
        keep_in_screen_client(p)

        # 组织好向服务器发送的数据
        data = {
            'pos': p.get_pos(),
            'bullet': control_report['is_shooting'],
            'pause': control_report['need_pause'],
            'restart': ck.R
        }
        # 如果要重新开始游戏，由于游戏开始默认暂停，因此首先重置Player对象，同时暂停BGM的播放
        if ck.R == True:
            ID, p = n.get_local_object()
            client_audio.restart_BGM()
        # 重新开始游戏只需要一次请求，不需要一直保持
        ck.clear_state('R')

        # 发送到服务器
        n.send(data)

        # 服务器返回在这一轮之后的战场情况
        reply = n.receive()
        # 将本时刻更新的音乐添加到音效中去
        if game_state != 'lose' or game_state != 'win':
            client_audio.add_sound_effect(reply.sound_list)

        old_state = game_state
        game_state = reply.state

        draw_background(win, reply.background_frame)
        # 客户端根据更新的情况，对画面进行更新
        if game_state == 'running':
            # 如果上次更新时不是运行状态，再切换BGM播放状态，防止BGM播放状态一直切换
            if old_state != 'running':
                client_audio.unpause_BGM()

            draw_ui(win, reply.players[ID].game_score)
            redraw(win, reply)
        elif game_state == 'pause':
            # 如果上次更新时不是暂停状态，再切换BGM播放状态，防止BGM播放状态一直切换
            if old_state != 'pause':
                client_audio.unpause_BGM()
            client_audio.pause_BGM()

            draw_pause_window(win)
            draw_ui(win, reply.players[ID].game_score)
            redraw(win, reply)
        elif game_state == 'win':
            # 如果本局游戏胜利
            # 暂停BGM播放
            client_audio.pause_BGM()

            # 显示游戏胜利覆盖层
            draw_win_screen(win, reply.players[ID].game_score)
            redraw(win, reply)
        if game_state == 'lose':
            # 如果本局游戏失败
            # 暂停BGM播放
            client_audio.pause_BGM()

            # 显示游戏失败覆盖层
            draw_lose_screen(win, reply.players[ID].game_score)
            redraw(win, reply)


if __name__ == '__main__':
    main_menu()
