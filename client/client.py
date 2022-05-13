import pygame
import sys

# 为了导入其他目录的模块，需要先将其他目录的路径加入环境变量中
sys.path.append('../base')
sys.path.append('../server')

from input_handle import get_input
from texture import Texture
from config import window_height as height
from config import window_width as width
from network import Network

# width = 500
# height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0


def redraw_window(window, players):
    window.fill((255, 255, 255))
    for p_id, player in players.items():
        player.init_texture(t.lib[player.texture_name])
        player.draw_self(window)
    pygame.display.update()


if __name__ == '__main__':
    t = Texture()
    # 初始化网络连接
    n = Network(
        ip='localhost',
        port=44013,
    )

    # 向服务器发送本客户端的飞机信息
    n.init_player(
        basic_setting={
            'size': (t.lib['YELLOW_SPACE_SHIP'].get_size()),
            'texture_name': 'YELLOW_SPACE_SHIP'
        },
        inertia_setting={
            'max_speed':3,
        },
        plane_setting={

        },
    )

    # 从服务器拿到本客户端的玩家ID和飞机对象
    ID, p = n.get_local_object()
    # 由于服务端不负责处理贴图，因此在客户端上需要将贴图贴上
    p.init_texture(t.lib['YELLOW_SPACE_SHIP'])

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        # 由本地输入得到飞机移动的向量 和 飞机是否靠近鼠标位置
        target_position, is_damping_activate = get_input(p.get_center())
        # 在飞机的速度矢量上加上之前的移动矢量
        p.change_pos(target_position)
        # 如果在鼠标控制模式下，接近光标位置，就开始增加阻尼，使飞机减速
        if is_damping_activate:
            p.damping()

        # 结算并更新本地在这个时间点后的飞机位置
        p.update()

        # 组织好向服务器发送的数据
        data = {
            'pos': p.get_pos()
        }
        # 发送到服务器
        n.send(data)

        # 服务器返回在这一轮之后的战场情况
        reply = n.receive()

        # 客户端根据更新的情况，对画面进行更新
        redraw_window(win, reply.players)
