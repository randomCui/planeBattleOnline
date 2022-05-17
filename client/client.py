import sys
from math import degrees

import pygame

# 为了导入其他目录的模块，需要先将其他目录的路径加入环境变量中
sys.path.append('..')
sys.path.append('../base')

from input_handle import get_input
from base.shared_lib import t
from base.config import window_height as height
from base.config import window_width as width
from network import Network
from base.config import ip, port, sensitivity

# width = 500
# height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0


def redraw(window, game):
    draw_background(window)
    draw_players(window, game.players)
    draw_enemies(window, game.enemies)
    draw_hostile_bullets(window, game.hostile_bullets)
    draw_friendly_bullets(window, game.friendly_bullets)

    pygame.display.update()


def draw_hostile_bullets(window, bullets):
    for bullet in bullets:
        rotate_around_pivot(window,
                            t.lib[bullet.texture_name],
                            (bullet.x + bullet.width / 2, bullet.y + bullet.height / 2),
                            (bullet.width / 2, bullet.height / 2),
                            degrees(bullet.angle_from_y)
                            )


def draw_enemies(window, enemies):
    for enemy in enemies:
        enemy.init_texture(t.lib[enemy.texture_name])
        enemy.draw_self(window)


def draw_players(window, players):
    for p_id, player in players.items():
        player.init_texture(t.lib[player.texture_name])
        player.draw_self(window)


def rotate_around_pivot(window, image, pos, pivot_pos, angle):
    # offset from pivot to center
    image_rect = image.get_rect(topleft=(pos[0] - pivot_pos[0], pos[1] - pivot_pos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    # rotate and blit the image
    window.blit(rotated_image, rotated_image_rect)

    # draw rectangle around the image
    # pygame.draw.rect(window, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()), 2)
    return rotated_image


def draw_friendly_bullets(window, bullets):
    for bullet in bullets:
        rotated_img = pygame.transform.rotate(t.lib[bullet.texture_name], degrees(bullet.angle_from_y))
        bullet.init_texture(rotated_img)
        bullet.draw_self(window)


def keep_in_screen_client(player):
    if p.x < 0:
        p.x = 0
        p.vx = 0
    if p.x + p.width > width:
        p.x = width - p.width
        p.vx = 0
    if p.y<0:
        p.y = 0
        p.vy = 0
    if p.y+p.height>height:
        p.y = height - p.height
        p.vy = 0


def draw_background(window):
    window.fill((60, 63, 65))


if __name__ == '__main__':
    # 初始化网络连接
    n = Network(
        ip=ip,
        port=port,
    )

    # 向服务器发送本客户端的飞机信息
    n.init_player(
        basic_setting={
            'size': (t.lib['YELLOW_SPACE_SHIP'].get_size()),
            'texture_name': 'YELLOW_SPACE_SHIP'
        },
        inertia_setting={
            'max_speed': 8,
        },
        plane_setting={
            'health': 10,
        },
        player_setting={
            'fire_cool_down_frame': 20,
        }
    )

    # 从服务器拿到本客户端的玩家ID和飞机对象
    ID, p = n.get_local_object()
    # 由于服务端不负责处理贴图，因此在客户端上需要将贴图贴上
    p.init_texture(t.lib['YELLOW_SPACE_SHIP'])

    clock = pygame.time.Clock()
    run = True

    control_counter = 0

    while run:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                n.disconnect()
                pygame.quit()
        # 由本地输入得到飞机移动的向量 和 飞机是否靠近鼠标位置
        control_report = get_input(p.get_center())
        # 在飞机的速度矢量上加上之前的移动矢量

        p.change_pos(control_report['move_vector'])
        # 如果在鼠标控制模式下，接近光标位置，就开始增加阻尼，使飞机减速
        if control_report['is_damping']:
            p.damping()

        if control_counter == sensitivity:
            control_counter = 0
            # 结算并更新本地在这个时间点后的飞机位置
            p.update()
        control_counter += 1

        # 让对象保持在屏幕中央
        keep_in_screen_client(p)
        # 组织好向服务器发送的数据
        data = {
            'pos': p.get_pos(),
            'bullet': control_report['is_shooting'],
        }
        # 发送到服务器
        n.send(data)

        # 服务器返回在这一轮之后的战场情况
        reply = n.receive()
        # 客户端根据更新的情况，对画面进行更新
        redraw(win, reply)
