import pygame
import sys

sys.path.append('../base')

from base.config import window_width, window_height
from math import sqrt, pow


def get_input_vector_keyboard(keys):
    # 键盘输入默认需要阻尼
    is_damping = True
    x = 0
    y = 0
    # 将键盘每次的按键都抽象成0.1的偏移量
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

    return (x, y), is_damping


def get_input_vector_mouse(plane_pos):
    # 设置飞机移动到鼠标位置100像素以内时进行阻尼平滑减速
    approaching_threshold = 100
    is_approaching_mouse = False
    mouse_input = pygame.mouse.get_pos()
    # 得到飞机相对于鼠标的向量
    move_vector = mouse_input[0] - plane_pos[0], mouse_input[1] - plane_pos[1]
    # 计算距离
    distance = sqrt(pow(move_vector[0], 2) + pow(move_vector[1], 2))
    # 如果靠近到了鼠标
    if distance < approaching_threshold:
        # 就进行阻尼
        is_approaching_mouse = True
    # 返回前进向量值和是否需要阻尼
    return mouse_move_vector_adjust(move_vector), is_approaching_mouse


def mouse_move_vector_adjust(vector):
    # 为了适应不同大小的窗口，将移动的绝对值转换为屏幕大小的相对值
    a_vector = (vector[0] / window_width), (vector[1] / window_height)
    return a_vector


def detect_shooting(keys):
    # 说明玩家发射了子弹
    if keys[pygame.K_SPACE]:
        return True


def get_input(plane_pos, is_mouse_control):
    # 提供一个规范的报文格式
    control_report = {
        'move_vector': None,
        'is_controlling': None,
        'is_shooting': None,
    }
    # 获得键盘按下的状态
    kb_state = pygame.key.get_pressed()

    # 获得键盘和鼠标各自的操作输入值
    kb_input = get_input_vector_keyboard(kb_state)
    mouse_input = get_input_vector_mouse(plane_pos)

    # 得到是否要发射子弹的输入
    is_shooting = detect_shooting(kb_state)

    # 决定是鼠标操作还是键盘操作
    if not is_mouse_control:
        move_vector, is_damping = kb_input
    else:
        move_vector, is_damping = mouse_input

    control_report['move_vector'] = move_vector
    control_report['is_damping'] = is_damping
    control_report['is_shooting'] = is_shooting

    return control_report
