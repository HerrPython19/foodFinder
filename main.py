import pygame, sys, creatures, random, numpy
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
def updateCreatures(clist):
    for bug in clist:
        bug.step()

def createCreatures(amt, food):
    clist = []
    for i in range(amt):
        mybug = creatures.BlockBug(20,20,10,10, food)
        mybug.setBoundsPos(0,0,WINDOWWIDTH-10,WINDOWHEIGHT-10)
        mybug.setBoundsVel(2,2)
        mybug.setBoundsAcc(1,1)

        clist.append(mybug)

    return clist

def selection(clist):
    #sorts creatures by fitness and selects top 4
    clist = sorted(clist, key = lambda x: x.fitness())
    clist = clist[:4]
    
    return clist

def crossover(parents):
    clist = []
    for c in parents:
        clist.append(c)

    while len(clist) < 10:
        parent1 = random.choice(clist)
        parent2 = random.choice(clist)

        child = createCreatures(1, parent1.food)[0]
        #pull current weights from the child (for editing)
        child_w1 = child.net.xmodel.get_layer(index=1).get_weights()
        child_w2 = child.net.xmodel.get_layer(index=2).get_weights()
        child_w3 = child.net.ymodel.get_layer(index=1).get_weights()
        child_w4 = child.net.ymodel.get_layer(index=2).get_weights()

        #get weights from parent 1
        parent1_w1 = parent1.net.xmodel.get_layer(index=1).get_weights()
        parent1_w2 = parent1.net.xmodel.get_layer(index=2).get_weights()
        parent1_w3 = parent1.net.ymodel.get_layer(index=1).get_weights()
        parent1_w4 = parent1.net.ymodel.get_layer(index=2).get_weights()

        #get weights from parent 2
        parent2_w1 = parent1.net.xmodel.get_layer(index=1).get_weights()
        parent2_w2 = parent1.net.xmodel.get_layer(index=2).get_weights()
        parent2_w3 = parent1.net.ymodel.get_layer(index=1).get_weights()
        parent2_w4 = parent1.net.ymodel.get_layer(index=2).get_weights()

        #do crossover
        pivot = random.randint(1,3)
        child_w1[0][0] = numpy.concatenate([parent1_w1[0][0][:pivot],parent2_w1[0][0][pivot:]])
        pivot = random.randint(0,4)
        child_w2[0][0] = numpy.concatenate([parent1_w2[0][0][:pivot],parent2_w2[0][0][pivot:]])
        pivot = random.randint(0,4)
        child_w3[0][0] = numpy.concatenate([parent1_w3[0][0][:pivot],parent2_w3[0][0][pivot:]])
        pivot = random.randint(0,4)
        child_w4[0][0] = numpy.concatenate([parent1_w4[0][0][:pivot],parent2_w4[0][0][pivot:]])

        #set child's weights to new weights
        child.net.xmodel.get_layer(index=1).set_weights(child_w1)
        child.net.xmodel.get_layer(index=2).set_weights(child_w2)
        child.net.ymodel.get_layer(index=1).set_weights(child_w3)
        child.net.ymodel.get_layer(index=2).set_weights(child_w4)
        
        clist.append(child)

    return clist


def mutate(clist):
    for creature in clist:
        w1 = creature.net.xmodel.get_layer(index=1).get_weights()
        w2 = creature.net.xmodel.get_layer(index=1).get_weights()
        w3 = creature.net.xmodel.get_layer(index=1).get_weights()
        w4 = creature.net.xmodel.get_layer(index=1).get_weights()
        
#Main function
def main():
    global WINDOWSURF, DRAWSURF

    generation = 0
    epoch = 0
    max_epoch = 500
    pop_size = 10
    #create creatures and food
    myfood = creatures.DeadBug(200,150)
    creature_list = createCreatures(pop_size, myfood)

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

        updateCreatures(creature_list)
        
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
            parents = selection(creature_list)
            new_creatures = crossover(parents)
            mutate(new_creatures)
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    main()
