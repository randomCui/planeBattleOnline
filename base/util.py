from math import sqrt, pow, atan


def distance_between(pos1,pos2):
    return sqrt(pow(pos1[0]-pos2[0],2)+pow(pos1[1]-pos2[1],2))


def vector_angle_from_y(vector):
    return atan(vector[0]/vector[1])
