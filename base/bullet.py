from inertia_object import InertiaObject
from util import distance_between,vector_angle_from_y
from math import atan


class Bullet(InertiaObject):
    def __init__(self, **properties):
        super().__init__(basic_setting=properties['basic_setting'],
                         inertia_setting=properties['inertia_setting'],
                         )
        self.damage = None
        self.animation_list = []
        self.not_destroyed = True

        for key, value in properties['bullet_setting'].items():
            setattr(self, key, value)

    def get_damage(self):
        if self.not_destroyed:
            return self.damage

    def init_shoot_move(self, speed_vector):
        self.vx = speed_vector[0]
        self.vy = speed_vector[1]

    def update(self):
        super(Bullet, self).update()


class BulletSimple(Bullet):
    pass


class BulletAiming(Bullet):
    def __init__(self, **properties):
        self.target = None
        self.angle_from_y = None

        super(BulletAiming, self).__init__(basic_setting=properties['basic_setting'],
                                           inertia_setting=properties['inertia_setting'],
                                           bullet_setting=properties['bullet_setting']
                                           )

        assert self.target is not None
        target_vector = self.target[0]-self.get_center()[0], self.target[1]-self.get_center()[1]
        distance = distance_between(self.target, self.get_center())
        self.vx = self.max_speed*(target_vector[0]/distance)
        self.vy = self.max_speed * (target_vector[1] / distance)
        self.angle_from_y = vector_angle_from_y(target_vector)
        print(self.angle_from_y*180/3.14)
