from game_object import GameObject


class Shield(GameObject):
    """
    护盾类，游戏内目前还没有实现这个功能
    """
    def __init__(self, owner, **properties):
        super().__init__(basic_setting=properties['basic_setting'])

        self.texture = None
        self.is_deploying = False
        for key, value in properties['shield_setting']:
            setattr(self, key, value)
