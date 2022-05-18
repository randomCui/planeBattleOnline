import pygame,os


animate = {
    'explosion1': [

    ]
}

for i in range(1, 9):
    filename = "bomb"+str(i)+".png"
    path = os.path.join("..", "assets", "animate", filename)
    animate['explosion1'].append(pygame.image.load(path))
