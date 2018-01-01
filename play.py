import pygame, sys, creatures, random, pickle, time
from pygame.locals import *

#Global variables representing window dimensions
WINDOWWIDTH = 600
WINDOWHEIGHT = 600

#Global variable for top-level surface
WINDOWSURF = None
DRAWSURF = None

#Color globals
BLACK = (0,0,0)
WHITE = (255,255,255)

#Define our desired FPS
FPS = 60

#Updates internal game state
def updateCreatures(clist):
    for bug in clist:
        bug.step()
        
#Draws any creature
def drawCreature(creature):
    pygame.draw.rect(DRAWSURF,creature.color,creature.rect)

def createCreatures(amt, food):
    clist = []
    for i in range(amt):
        mybug = creatures.BlockBug(20,20,10,10, food)
        mybug.setBoundsPos(0,0,WINDOWWIDTH-10,WINDOWHEIGHT-10)
        mybug.setBoundsVel(2,2)
        mybug.setBoundsAcc(1,1)

        clist.append(mybug)

    return clist

def setWeights(net, weights):
    net.xmodel.get_layer(index=1).set_weights(weights[0])
    net.xmodel.get_layer(index=2).set_weights(weights[1])
    net.ymodel.get_layer(index=1).set_weights(weights[2])
    net.ymodel.get_layer(index=2).set_weights(weights[3])

def load_nets():
    f = open("pop.ulation","rb")
    weights = pickle.load(f)
    f.close()

    return weights

def load_gen():
    f = open("gen.eration","rb")
    gen = pickle.load(f)
    f.close()

    return gen

def main():
    global WINDOWSURF, DRAWSURF

    pop_size = 10

    #create creatures and food (explicitly uses saved population)
    myfood = creatures.DeadBug(200,200)
    weights = load_nets()
    generation = load_gen()
    creature_list = createCreatures(pop_size, myfood)
    for i in range(len(creature_list)):
        creature_list[i].food = myfood
        setWeights(creature_list[i].net, weights[i])

    pygame.init()
    WINDOWSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    DRAWSURF = pygame.Surface((WINDOWWIDTH,WINDOWHEIGHT))
    DRAWSURF.fill(BLACK)
    pygame.display.set_caption("Food Finder")

    basicfont = pygame.font.SysFont(None, 20)
    #text = basicfont.render("Generation: " + str(generation) + "   Epoch: "+ str(epoch),True, (255,255,255), (0,0,0))
    #textrect = pygame.Rect(210,0,150,20)
    
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                myfood = creatures.DeadBug(x, y)
                for i in creature_list:
                    i.food = myfood

        updateCreatures(creature_list) 
        DRAWSURF.fill(BLACK)
        #text = basicfont.render("Generation: " + str(generation) + "   Epoch: "+ str(epoch),True, (255,255,255), (0,0,0))
        #DRAWSURF.blit(text,textrect)
        
        for bug in creature_list:
            drawCreature(bug)
        drawCreature(myfood)
        
        WINDOWSURF.blit(DRAWSURF,(0,0))
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
