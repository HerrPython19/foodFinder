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
def updateCreatures(clist, food):
    for bug in clist:
        bug.step(food.pos.x,food.pos.y)

def createCreatures(amt):
    clist = []
    for i in range(amt):
        mybug = creatures.BlockBug(20,20,10,10)
        mybug.setBoundsPos(0,0,WINDOWWIDTH-10,WINDOWHEIGHT-10)
        mybug.setBoundsVel(2,2)
        mybug.setBoundsAcc(1,1)

        clist.append(mybug)

    return clist
        
#Main function
def main():
    global WINDOWSURF, DRAWSURF

    generation = 0
    epoch = 0
    max_epoch = 500
    pop_size = 10
    #create creatures and food
    creature_list = createCreatures(pop_size)
    myfood = creatures.DeadBug(200,150)

    pygame.init()
    WINDOWSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    DRAWSURF = pygame.Surface((WINDOWWIDTH,WINDOWHEIGHT))
    DRAWSURF.fill(BLACK)
    pygame.display.set_caption("Food Finder")

    basicfont = pygame.font.SysFont(None, 20)
    text = basicfont.render("Generation: " + str(generation) + "   Epoch: "+ str(epoch),
                            True, (255,255,255), (0,0,0))
    textrect = pygame.Rect(150,0,150,20)
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYUP:
                if event.key == K_SPACE:
                    creature_list = createCreatures(pop_size)

        updateCreatures(creature_list, myfood)
        
        DRAWSURF.fill(BLACK)
        epoch += 1
        text = basicfont.render("Generation: " + str(generation) + "   Epoch: "+ str(epoch),
                            True, (255,255,255), (0,0,0))
        DRAWSURF.blit(text,textrect)
        
        for bug in creature_list:
            drawCreature(bug)
        drawCreature(myfood)
        
        WINDOWSURF.blit(DRAWSURF,(0,0))
        pygame.display.update()
        clock.tick(FPS)

        if epoch >= max_epoch:
            for bug in creature_list:
                print bug.fitness(myfood.pos.x,myfood.pos.y)
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    main()
