import pygame

#Color globals
BLACK = (0,0,0)
WHITE = (255,255,255)

class BlockBug:
    def __init__(self, x, y, width, height, color=WHITE):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
