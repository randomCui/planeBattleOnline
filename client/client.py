import pygame, os, sys
sys.path.append('../base')
sys.path.append('../server')

from input_handle import get_input
from texture import Texture
from config import window_height as height
from config import window_width as width
from network import Network

from base.player import Player

# width = 500
# height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0


def redraw_window(win,players):
    win.fill((255,255,255))
    for id, player in players.items():
        player.init_texture(t.lib[player.texture_name])
        player.draw_self(win)
    pygame.display.update()


if __name__ == '__main__':
    t = Texture()
    n = Network(
        ip='localhost',
        port=5559,
        size=(t.lib['YELLOW_SPACE_SHIP'].get_size()),
        max_speed=3,
        texture_name='YELLOW_SPACE_SHIP',
    )

    run = True
    id, p = n.get_local_object()
    p.init_texture(t.lib['YELLOW_SPACE_SHIP'])

    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        new_pos, need_dumper = get_input(p.get_center())
        p.change_pos(new_pos)
        if need_dumper:
            p.dumper_once()
        p.update()
        data = {
            'pos':p.get_pos()
        }
        n.send(data)
        reply = n.receive()
        redraw_window(win, reply.players)

