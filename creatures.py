import pygame, numpy, pickle, traceback
from vector import Vector

#Color globals
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)

class DeadBug:
    def __init__(self, x, y, color=GREEN):
        self.pos = Vector(x, y)
        self.color = color
        self.rect = pygame.Rect(x, y, 5, 5)

class BlockBug:
    def __init__(self, x, y, width, height, color=WHITE):
        self.pos = Vector(x, y)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

    def step(self):
        self.vel.addV(self.acc)
        self.pos.addV(self.vel)
