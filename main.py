import pygame, sys, creatures
from pygame.locals import *
#from nets import CreatureNet

#Global variables representing window dimensions
WINDOWWIDTH = 400
WINDOWHEIGHT = 300

#Global variable for top-level surface
WINDOWSURF = None
DRAWSURF = None

#Color globals
BLACK = (0,0,0)
WHITE = (255,255,255)

#Define our desired FPS
FPS = 60

#Draws any creature
def drawCreature(creature):
    pygame.draw.rect(DRAWSURF,creature.color,creature.rect)

#updates internal game state
def updateCreatures():
    pass
    
#Main function
def main():
    global WINDOWSURF, DRAWSURF

    #create creatures and food
    mybug = creatures.BlockBug(20,20,10,10)
    mybug.setBoundsPos(0,0,WINDOWWIDTH-10,WINDOWHEIGHT-10)
    mybug.setBoundsVel(2,2)
    mybug.setBoundsAcc(.25,.25)
    myfood = creatures.DeadBug(200,100)

    pygame.init()
    WINDOWSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    DRAWSURF = pygame.Surface((WINDOWWIDTH,WINDOWHEIGHT))
    DRAWSURF.fill(BLACK)
    pygame.display.set_caption("Food Finder")
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        updateCreatures()
        
        DRAWSURF.fill(BLACK)
        drawCreature(mybug)
        drawCreature(myfood)
        WINDOWSURF.blit(DRAWSURF,(0,0))
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
