import pygame,sys
sys.path.append('../base')

from base.config import window_width, window_height
from math import sqrt, pow

toggle_mouse_control = False
toggle_mouse_control_delay = 0
toggle_pause = False
toggle_pause_delay = 0


def get_input_vector_keyboard(keys):
    global toggle_mouse_control
    global toggle_mouse_control_delay
    is_damping = True
    x = 0
    y = 0
    if keys[pygame.K_LEFT]:
        x -= 0.1
        is_damping = False

    if keys[pygame.K_RIGHT]:
        x += 0.1
        is_damping = False

    if keys[pygame.K_UP]:
        y -= 0.1
        is_damping = False

    if keys[pygame.K_DOWN]:
        y += 0.1
        is_damping = False

    toggle_mouse_control_delay -= 1
    if toggle_mouse_control_delay < 0:
        if keys[pygame.K_RALT]:
            toggle_mouse_control_delay = 30
            if toggle_mouse_control:
                toggle_mouse_control = False
            else:
                toggle_mouse_control = True

    return (x, y), is_damping


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


def detect_shooting(keys):
    # 说明玩家发射了子弹
    if keys[pygame.K_SPACE]:
        return True


def detect_pause(keys):
    global toggle_pause, toggle_pause_delay
    toggle_pause_delay -= 1
    if toggle_pause_delay < 0:
        toggle_pause_delay = 30
        if keys[pygame.K_ESCAPE]:
            if toggle_pause:
                toggle_pause = False
            else:
                toggle_pause = True


def get_input(plane_pos):
    # 提供一个规范的报文格式
    control_report = {
        'move_vector': None,
        'is_controlling': None,
        'is_shooting': None,
    }

    kb_state = pygame.key.get_pressed()

    kb_input = get_input_vector_keyboard(kb_state)
    mouse_input = get_input_vector_mouse(plane_pos)

    is_shooting = detect_shooting(kb_state)

    detect_pause(kb_state)

    if not toggle_mouse_control:
        move_vector, is_damping = kb_input
        # return kb_input,False
    else:
        move_vector, is_damping = mouse_input
        # return mouse_input

    control_report['move_vector'] = move_vector
    control_report['is_damping'] = is_damping
    control_report['is_shooting'] = is_shooting
    control_report['need_pause'] = toggle_pause

    return control_report


