from math import sqrt, pow, atan, degrees
from config import window_height as height
from config import window_width as width


def distance_between(pos1, pos2):
    return sqrt(pow(pos1[0] - pos2[0], 2) + pow(pos1[1] - pos2[1], 2))


def vector_angle_from_y(vector):
    return degrees(atan(vector[0] / vector[1]))


def adjust_move_vector(vector):
    a_vector = (vector[0] / width), (vector[1] / height)
    return a_vector


def vector_from_A_to_B(a_pos, b_pos):
    return b_pos[0] - a_pos[0], b_pos[1] - a_pos[1]


def out_of_screen(obj):
    if obj.x + obj.width < 0:
        return True
    if obj.x > width:
        return True
    if obj.y + obj.height < 0:
        return True
    if obj.y > height:
        return True
    return False

