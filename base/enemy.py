from plane import Plane


class EnemyType1(Plane):
    def __init__(self, **properties):
        super().__init__(basic_setting=properties['basic_setting'],
                         inertia_setting=properties['inertia_setting'],
                         plane_setting=properties['plane_setting'],
                         )
        for key, value in properties['enemy_setting']:
            setattr(self, key, value)

    def update(self):
        super(EnemyType1, self).update()

    def hit(self, amount=1):
        super(EnemyType1, self).hit()

    def init_move(self, speed_vector):
        super(EnemyType1, self).init_move(speed_vector)



class EnemyType2(Plane):
    pass
