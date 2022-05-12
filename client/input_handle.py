import pygame
from config import sensitivity,window_width,window_height,toggle_mouse_control,toggle_mouse_control_delay


def get_input_vector_keyboard():
    global toggle_mouse_control
    global toggle_mouse_control_delay
    keys = pygame.key.get_pressed()
    x=0
    y=0
    if keys[pygame.K_LEFT]:
        x -= 0.05

    if keys[pygame.K_RIGHT]:
        x += 0.05

    if keys[pygame.K_UP]:
        y -= 0.05

    if keys[pygame.K_DOWN]:
        y += 0.05

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
    mouse_input = pygame.mouse.get_pos()
    move_vector = mouse_input[0]-plane_pos[0],mouse_input[1]-plane_pos[1]
    return mouse_move_vector_adjust(move_vector)


def mouse_move_vector_adjust(vector):
    a_vector = (vector[0]/window_width),(vector[1]/window_height)
    return a_vector


def get_input(plane_pos):
    kb_input = get_input_vector_keyboard()
    mouse_input = get_input_vector_mouse(plane_pos)
    if not toggle_mouse_control:
        return kb_input
    else:
        return mouse_input

