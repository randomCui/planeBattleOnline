from bullet import Bullet
from util import adjust_move_vector, vector_from_A_to_B, distance_between


class Missile(Bullet):
    def __init__(self, **properties):
        super().__init__(
            basic_setting=properties['basic_setting'],
            inertia_setting=properties['inertia_setting'],
            bullet_setting=properties['missile_setting'],
        )
        self.target_object = properties['missile_setting']['target_object']
        self.life_time = properties['missile_setting']['life_time']
        self.approach_threshold = 100
        self.dumper_factor = 0.99
        self.fuel = True

    def update(self):
        self.update_tracking()
        super().update()

    def update_tracking(self):
        if self.fuel:
            self.life_time -= 1
            move_vector = vector_from_A_to_B(self.get_center(), self.target_object.get_center())
            move_vector = adjust_move_vector(move_vector)
            self.change_pos(move_vector)
            if distance_between(self.get_center(), self.target_object.get_center()) < self.approach_threshold:
                self.damping()
