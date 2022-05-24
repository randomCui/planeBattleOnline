from math import sqrt, pow, atan, degrees, hypot, acos

from config import window_height as height
from config import window_width as width


def distance_between(pos1, pos2):
    """
    计算两个坐标之间的距离

    :param pos1: 坐标1
    :param pos2: 坐标2
    :return: 两坐标之间的距离
    """
    return sqrt(pow(pos1[0] - pos2[0], 2) + pow(pos1[1] - pos2[1], 2))


def vector_angle_from_y(vector):
    """
    计算向量跟y轴的夹角

    :param vector: 需要计算的向量
    :return: 跟y轴的夹角
    """
    return degrees(atan(vector[0] / vector[1]))


def adjust_move_vector(vector):
    """
    将绝对移动向量转换为跟屏幕大小的相对移动距离

    :param vector: 移动的向量
    :return: 标准换之后的向量
    """
    a_vector = (vector[0] / width), (vector[1] / height)
    return a_vector


def vector_from_A_to_B(a_pos, b_pos):
    """
    计算坐标A指向坐标B的向量

    :param a_pos: 坐标A
    :param b_pos: 坐标B
    :return: 计算出的向量
    """
    return b_pos[0] - a_pos[0], b_pos[1] - a_pos[1]


def out_of_screen(obj):
    """
    目标是否完全在屏幕外

    :param obj: 被检测的对象
    :return: 是否在屏幕之外
    """
    if obj.x + obj.width < 0:
        return True
    if obj.x > width:
        return True
    if obj.y + obj.height < 0:
        return True
    if obj.y > height:
        return True
    return False


def angle(vector1, vector2):
    """
    计算两向量之家的夹角

    :param vector1: 向量1
    :param vector2: 向量2
    :return: 夹角
    """
    x1, y1 = vector1
    x2, y2 = vector2
    inner_product = x1 * x2 + y1 * y2
    len1 = hypot(x1, y1)
    len2 = hypot(x2, y2)
    print(acos(inner_product / (len1 * len2)))
    return acos(inner_product / (len1 * len2))


def calculate_end_point(shoot_vector, length):
    """
    计算指向某个方向的向量，在特定长度下，末端的坐标

    :param shoot_vector: 方向向量
    :param length: 向量长度
    :return: 终点坐标
    """
    total_distance = (shoot_vector[0] ** 2 + shoot_vector[1] ** 2) ** 0.5
    if total_distance != 0:
        percentage = length / total_distance
        return shoot_vector[0] * percentage, shoot_vector[1] * percentage
    else:
        return shoot_vector
