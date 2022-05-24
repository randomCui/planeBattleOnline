import pygame,os


animate = {
    'explosion1': [

    ],
    'background': [

    ]
}

for i in range(1, 9):
    filename = "bomb"+str(i)+".png"
    path = os.path.join("..", "assets", "animate", filename)
    animate['explosion1'].append(pygame.image.load(path))

for i in range(0, 43):
    filename = 'bg'+str(i)+'.jpg'
    path = os.path.join("..", "assets", "background", filename)
    animate['background'].append(pygame.image.load(path))

