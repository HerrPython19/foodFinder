import pygame, numpy, pickle, traceback
from vector import Vector

#Color globals
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)

class Bug:
    def __init__(self, x, y, width, height, color):
        self.pos = Vector(x, y)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

class DeadBug(Bug):
    def __init__(self, x, y):
        Bug.__init__(self, x, y, 5, 5, GREEN)

class BlockBug(Bug):
    def __init__(self, x, y, width, height, color=WHITE):
        Bug.__init__(self, x, y, width, height, color)
        
    def setBoundsPos(self, minx, miny, maxx, maxy):
        self.pos.lBound(minx,miny)
        self.pos.uBound(maxx,maxy)

    def setBoundsVel(self, x, y):
        self.vel.bound(x,y)

    def setBoundsAcc(self, x, y):
        self.acc.bound(x,y)

    def step(self):
        self.vel.addV(self.acc)
        self.pos.addV(self.vel)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
