import pygame


class GameObject:
    def __init__(self, **properties):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        # 设置生命值，移动速度等等内容
        self.width = 0
        self.height = 0
        self.angle = 0
        self.size = None
        self.texture = None
        self.mask = None
        for key, value in properties['basic_setting'].items():
            setattr(self, key, value)

        assert self.size is not None
        self.width = self.size[0]
        self.height = self.size[1]

    def init_texture(self, texture):
        if texture is not None:
            self.texture = texture
            self.height = texture.get_height()
            self.width = texture.get_width()
        else:
            raise ValueError("Texture cannot be None")

    def get_center(self):
        return self.x + self.width / 2, self.y + self.height / 2

    def draw_self(self, window):
        """
        将游戏中的飞行物体直接画在对应的窗口中

        :param window: 需要显示到的窗口
        :return:
        """
        # 假设在显示图形之前图像已经被初始化完成
        assert self.texture is not None
        self.rotate_around_pivot(window)

    def rotate_around_pivot(self, window):
        # offset from pivot to center
        image_rect = self.texture.get_rect(topleft=(self.x, self.y))
        offset_center_to_pivot = pygame.math.Vector2((self.x, self.y)) - image_rect.center

        # rotated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(-self.angle)

        # rotated image center
        rotated_image_center = (self.x - rotated_offset.x, self.y - rotated_offset.y)

        # get a rotated image
        rotated_image = pygame.transform.rotate(self.texture, self.angle)
        rotated_image_rect = rotated_image.get_rect(topleft=(self.x,self.y),center=rotated_image_center)

        # rotate and blit the image
        window.blit(rotated_image, rotated_image_rect)

        # draw rectangle around the image
        pygame.draw.rect(window, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()), 2)

    def __str__(self):
        """
        将游戏对象状态转为字符串，便于调试

        :return: 游戏对象的字符串
        """
        return format("Pos:(%.2f)(%2.f),Vector:(%.2f)(%.2f)" % (self.x, self.y, self.vx, self.vy))
