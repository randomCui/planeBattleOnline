import pygame,os
from base.config import window_height as height
from base.config import window_width as width

# 保存动画图片序列的字典
animate = {
    'explosion1': [

    ],
    'background': [

    ]
}

# 加载爆炸效果动画
for i in range(1, 9):
    filename = "bomb"+str(i)+".png"
    path = os.path.join("..", "assets", "animate", filename)
    animate['explosion1'].append(pygame.image.load(path))

# 加载背景动画序列
for i in range(0, 43):
    filename = 'bg'+str(i)+'.jpg'
    path = os.path.join("..", "assets", "background", filename)
    temp_img = pygame.image.load(path)

    pygame.transform.scale(temp_img,(width,height))
    animate['background'].append(temp_img)

