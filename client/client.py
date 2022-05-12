import pygame, os, sys
sys.path.append('../base')
from base.player import Player

from input_handle import get_input

from config import window_height as height
from config import window_width as width

# width = 500
# height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0


def redraw_window(win,player):
    win.fill((255,255,255))
    player.draw_self(win)
    pygame.display.update()


if __name__ == '__main__':
    YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("..", "assets", "pixel_ship_yellow.png"))
    run = True
    p = Player(0,0,YELLOW_SPACE_SHIP,
               max_speed=5)
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
        redraw_window(win, p)

