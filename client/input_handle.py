import pygame,sys
sys.path.append('../base')

from base.config import window_width, window_height
from math import sqrt, pow

toggle_mouse_control = False
toggle_mouse_control_delay = 0


def get_input_vector_keyboard():
    global toggle_mouse_control
    global toggle_mouse_control_delay
    keys = pygame.key.get_pressed()
    x=0
    y=0
    if keys[pygame.K_LEFT]:
        x -= 0.1

    if keys[pygame.K_RIGHT]:
        x += 0.1

    if keys[pygame.K_UP]:
        y -= 0.1

    if keys[pygame.K_DOWN]:
        y += 0.1

    toggle_mouse_control_delay -= 1
    if toggle_mouse_control_delay < 0:
        if keys[pygame.K_RALT]:
            toggle_mouse_control_delay = 30
            if toggle_mouse_control:
                toggle_mouse_control = False
            else:
                toggle_mouse_control = True

    return x,y


def get_input_vector_mouse(plane_pos):
    approaching_threshold = 100
    is_approaching_mouse = False
    mouse_input = pygame.mouse.get_pos()
    move_vector = mouse_input[0]-plane_pos[0],mouse_input[1]-plane_pos[1]
    distance = sqrt(pow(move_vector[0],2)+pow(move_vector[1],2))
    if distance < approaching_threshold:
        is_approaching_mouse = True
    return mouse_move_vector_adjust(move_vector),is_approaching_mouse


def mouse_move_vector_adjust(vector):
    a_vector = (vector[0]/window_width),(vector[1]/window_height)
    return a_vector


# def dumper(vector):
#     dumper_activate_distance = 100
#     dumper_factor = 1.2
#     """
#     当飞船运动到接近鼠标的位置时会出现往复运动的情况，因此设置一个阻尼来消除简谐运动现象
#
#     :return: 经过阻尼的向量，以及通知飞机对象是否要停止的标志
#     """
#     distance = sqrt(pow(vector[0],2)+pow(vector[1],2))
#     if distance < dumper_activate_distance:
#         return (vector[0]*(distance/dumper_activate_distance)*dumper_factor*-1,
#                vector[1]*(distance/dumper_activate_distance)*dumper_factor*-1)
#     else:
#         return vector


def get_input(plane_pos):
    kb_input = get_input_vector_keyboard()
    mouse_input = get_input_vector_mouse(plane_pos)
    if not toggle_mouse_control:
        return kb_input,False
    else:
        return mouse_input

