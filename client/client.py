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
from base.config import window_height as height
from base.config import window_width as width
from base.config import ip, port, sensitivity

# width = 500
# height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

pygame.font.init()
pygame.mixer.init()

title_font = pygame.font.SysFont("黑体", 30)
selection_font = pygame.font.SysFont("黑体", 40)
pause_font = pygame.font.SysFont("arial", 70)
sub_pause_font = pygame.font.SysFont("arial", 40)

client_number = 0
client_texture_name = 'YELLOW_SPACE_SHIP'
client_nickname = ''
client_ip = 'localhost'
client_port = 11451

nickname_font = pygame.font.SysFont("calibri", 30)


def redraw(window, game):
    # draw_background(window)
    draw_players(window, game.players)
    draw_enemies(window, game.enemies)
    draw_hostile_bullets(window, game.hostile_bullets)
    draw_friendly_bullets(window, game.friendly_bullets)
    draw_global_animate(window, game.animation)
    draw_bosses(window, game.bosses)
    draw_props(window, game.props)

    pygame.display.update()


def draw_props(window, props):
    for prop in props:
        prop.init_texture(t.lib[prop.texture_name])
        prop.draw_self(window)


def draw_global_animate(window, animation):
    for key, value in animation.items():
        for animate in value:
            animate.draw_self(window)


def draw_hostile_bullets(window, bullets):
    for bullet in bullets:
        bullet.init_texture(t.lib[bullet.texture_name])
        bullet.draw_self(window)


def draw_enemies(window, enemies):
    for enemy in enemies:
        enemy.init_texture(t.lib[enemy.texture_name])
        enemy.draw_self(window)


def draw_bosses(window, bosses):
    for boss in bosses:
        boss.init_texture(t.lib[boss.texture_name])
        boss.draw_self(window)


def draw_players(window, players):
    for p_id, player in players.items():
        if player.state == 'dead':
            continue
        player.init_texture(t.lib[player.texture_name])
        player.draw_self(window)
        title_label = nickname_font.render(player.nickname, True, (255, 255, 255))
        window.blit(title_label, (player.get_center()[0] - title_label.get_width() / 2, player.y - 30))


def draw_pause_window(window):
    title_pause = pause_font.render("Paused", True, (255, 255, 255))
    window.blit(title_pause, (width / 2 - title_pause.get_width() / 2, 250))
    title_pause = sub_pause_font.render("Press ESC to resume", True, (255, 255, 255))
    window.blit(title_pause, (width / 2 - title_pause.get_width() / 2, 350))
    # pygame.display.update()


def draw_win_screen(window, score):
    # window.fill(255, 255, 255)
    title_pause = pause_font.render("You Win", True, (255, 255, 255))
    window.blit(title_pause, (width / 2 - title_pause.get_width() / 2, 250))
    hint = "Your score is: " + str(score)
    title_pause = sub_pause_font.render(hint, True, (255, 255, 255))
    window.blit(title_pause, (width / 2 - title_pause.get_width() / 2, 350))
    # pygame.display.update()


def draw_lose_screen(window, score):
    # window.fill(255, 255, 255)
    title_pause = pause_font.render("You Lose", True, (255, 255, 255))
    window.blit(title_pause, (width / 2 - title_pause.get_width() / 2, 250))
    hint = "Your score is: " + str(score)
    title_pause = sub_pause_font.render(hint, True, (255, 255, 255))
    window.blit(title_pause, (width / 2 - title_pause.get_width() / 2, 350))
    # pygame.display.update()


def draw_friendly_bullets(window, bullets):
    for bullet in bullets:
        rotated_img = pygame.transform.rotate(t.lib[bullet.texture_name], degrees(bullet.angle))
        bullet.init_texture(rotated_img)
        bullet.draw_self(window)


def keep_in_screen_client(player):
    if player.x < 0:
        player.x = 0
        player.vx = 0
    if player.x + player.width > width:
        player.x = width - player.width
        player.vx = 0
    if player.y < 0:
        player.y = 0
        player.vy = 0
    if player.y + player.height > height:
        player.y = height - player.height
        player.vy = 0


def draw_background(window):
    window.fill((60, 63, 65))


class MainMenu:
    def __init__(self, window):
        self.window = window
        self.nickname = client_nickname
        self.texture_name = 'YELLOW_SPACE_SHIP'
        self.mode = False
        self.menu = pygame_menu.Menu('Main Menu', width, height,
                                     theme=pygame_menu.themes.THEME_BLUE)
        self.nickname_input = self.menu.add.text_input('Name :', default=client_nickname,
                                                       onchange=self.__update_nickname)
        self.plane_preview = self.menu.add.image(
            image_path=t.menu[self.texture_name],
            padding=(25, 0, 0, 0)  # top, right, bottom, left
        )
        self.plane_selector = self.menu.add.selector('Type :', [('Yellow', 1), ('Blue', 2)],
                                                     onchange=self.__update_texture)
        self.ip_input = self.menu.add.text_input('IP address :', default=ip, onchange=self.__update_ip_address)
        self.ip_input = self.menu.add.text_input('port :', default=port, onchange=self.__update_port)
        self.play_button = self.menu.add.button('Play', main_game)
        self.quit_button = self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def __update_texture(self, selected, value):
        global client_texture_name
        if value == 1:
            self.texture_name = 'YELLOW_SPACE_SHIP'
            client_texture_name = 'YELLOW_SPACE_SHIP'
        elif value == 2:
            self.texture_name = 'BLUE_SPACE_SHIP'
            client_texture_name = 'BLUE_SPACE_SHIP'
        self.plane_preview.set_image(t.menu[self.texture_name])

    def __update_nickname(self, text):
        global client_nickname
        self.nickname = text
        client_nickname = text

    def __update_ip_address(self, text):
        # global ip
        # ip = text
        pass

    def __update_port(self, text):
        # global port
        # port = text
        pass

    # def __update_mode(self, mode):
    #     global host_or_join
    #     print(mode)
    #     self.mode = mode
    #     host_or_join = mode

    def mainloop(self):
        self.menu.mainloop(self.window)


def main_menu():
    pygame.init()
    m = MainMenu(win)
    m.mainloop()


def main_game():
    game_state = 'running'
    # 初始化网络连接
    n = Network(
        ip=ip,
        port=port,
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

    clock = pygame.time.Clock()
    run = True
    control_counter = 0
    while run:
        ck.R = False

        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                n.disconnect()
                pygame.quit()
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_RALT:
            #         ck.state_change('R_ALT')
            #     elif event.key == pygame.K_ESCAPE:
            #         ck.state_change('Escape')
            #     elif event.key == pygame.K_r:
            #         ck.state_change('R')
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RALT:
                    ck.toggle_state('R_ALT')
                    # ck.clear_counter('R_ALT')
                elif event.key == pygame.K_ESCAPE:
                    ck.toggle_state('Escape')
                    # ck.clear_counter('Escape')
                elif event.key == pygame.K_r:
                    ck.toggle_state('R')
                    # ck.clear_counter('R')

        # 由本地输入得到飞机移动的向量 和 飞机是否靠近鼠标位置
        control_report = get_input(p.get_center(), ck.R_ALT)
        # 在飞机的速度矢量上加上之前的移动矢量
        control_report['need_pause'] = ck.Escape

        if ck.R == True:
            ID, p = n.get_local_object()
            client_audio.restart_BGM()

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
        # 发送到服务器
        n.send(data)

        # 服务器返回在这一轮之后的战场情况
        # p.draw_self(window)
        reply = n.receive()
        # 将本时刻更新的音乐添加到音效中去
        if game_state != 'lose' or game_state != 'win':
            client_audio.add_sound_effect(reply.sound_list)

        old_state = game_state
        game_state = reply.state

        # 客户端根据更新的情况，对画面进行更新
        if game_state == 'running':
            if old_state != 'running':
                client_audio.unpause_BGM()
            draw_background(win)
            redraw(win, reply)
        if game_state == 'pause':
            if old_state != 'pause':
                client_audio.unpause_BGM()
            client_audio.pause_BGM()
            draw_background(win)
            draw_pause_window(win)
            redraw(win, reply)
        if game_state == 'win':

            client_audio.pause_BGM()

            draw_background(win)
            draw_win_screen(win, reply.players[ID].game_score)
            redraw(win, reply)
        if game_state == 'lose':

            client_audio.pause_BGM()

            draw_background(win)
            draw_lose_screen(win, reply.players[ID].game_score)
            redraw(win, reply)


if __name__ == '__main__':
    main_menu()
