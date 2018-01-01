import pygame, sys, creatures, random, numpy, pickle, time, traceback
from pygame.locals import *

#updates internal game state
def updateCreatures(clist):
    for bug in clist:
        bug.step()

def createCreatures(amt, food):
    clist = []
    for i in range(amt):
        mybug = creatures.BlockBug(20,20,10,10, food)
        mybug.setBoundsPos(0,0,190,190)
        mybug.setBoundsVel(2,2)
        mybug.setBoundsAcc(1,1)

        clist.append(mybug)

    return clist

def selection(clist):
    #sorts creatures by fitness and selects top 4
    clist = sorted(clist, key = lambda x: x.fitness())
    clist = clist[:4]

    for i in range(4):
        clist[i].pos.set(10,10)
        clist[i].vel.set(0,0)
        clist[i].acc.set(0,0)
        clist[i].rect.top = 10
        clist[i].rect.left = 10
    
    return clist

def crossover(parents):
    #need to keep clist to avoid editing original list of parents
    clist = []
    childlist = []
    for c in parents:
        clist.append(c)

    #breeds 6 children from initial 4 parents
    while len(childlist) < 10:
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
        pivot = random.randint(0,4)
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
        
        childlist.append(child)

    return childlist


def mutate(clist):
    for creature in clist:
        w1 = creature.net.xmodel.get_layer(index=1).get_weights()
        w2 = creature.net.xmodel.get_layer(index=2).get_weights()
        w3 = creature.net.ymodel.get_layer(index=1).get_weights()
        w4 = creature.net.ymodel.get_layer(index=2).get_weights()

        chance = 6
        choice = random.randint(1,chance)
        if choice == chance:
            mutate_index = random.randint(0,3)
            w1[0][0][mutate_index] = (random.random()*2)-1
            mutate_index = random.randint(0,3)
            w2[0][mutate_index][0] = (random.random()*2)-1
            mutate_index = random.randint(0,3)
            w3[0][0][mutate_index] = (random.random()*2)-1
            mutate_index = random.randint(0,3)
            w4[0][mutate_index][0] = (random.random()*2)-1

        creature.net.xmodel.get_layer(index=1).set_weights(w1)
        creature.net.xmodel.get_layer(index=2).set_weights(w2)
        creature.net.ymodel.get_layer(index=1).set_weights(w3)
        creature.net.ymodel.get_layer(index=2).set_weights(w4)

def avgFitness(clist):
    total = 0
    divisor = 0
    for i in clist:
        total += i.fitness()
        divisor += 1

    return float(total)/divisor

def getWeights(net):
    weights = []
    weights.append(net.xmodel.get_layer(index=1).get_weights())
    weights.append(net.xmodel.get_layer(index=2).get_weights())
    weights.append(net.ymodel.get_layer(index=1).get_weights())
    weights.append(net.ymodel.get_layer(index=2).get_weights())

    return weights

def setWeights(net, weights):
    net.xmodel.get_layer(index=1).set_weights(weights[0])
    net.xmodel.get_layer(index=2).set_weights(weights[1])
    net.ymodel.get_layer(index=1).set_weights(weights[2])
    net.ymodel.get_layer(index=2).set_weights(weights[3])
    
def save_nets(clist):
    #store weights of current creatures
    weight_list = []
    food = clist[0].food
    amt = len(clist)
    for c in clist:
        weight_list.append(getWeights(c.net))

    f = open("pop.ulation","wb")
    pickle.dump(weight_list,f)
    f.close()

def save_gen(gen):
    f = open("gen.eration", "wb")
    pickle.dump(gen,f)
    f.close()

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
        
#Main function
def main():
    #set initial variables
    generation = 0
    epoch = 0
    max_epoch = 500
    pop_size = 10

    #determine if we're using saved population (-saved argument at cli)
    if len(sys.argv) > 1:
        if sys.argv[1] == "-saved":
            saved = "y"
            print "Using saved population."
        else:
            saved = "n"
            print "Using new population."
    else:
        saved = "n"
        print "Using new population."

    #create creatures and food
    myfood = creatures.DeadBug(200,200)
    if saved == "y":
        weights = load_nets()
        generation = load_gen()
        creature_list = createCreatures(pop_size, myfood)
        for i in range(len(creature_list)):
            creature_list[i].food = myfood
            setWeights(creature_list[i].net, weights[i])

    else:
        creature_list = createCreatures(pop_size, myfood)

    print "Starting new generation"
    start_time = time.time()
    while epoch < max_epoch:
        updateCreatures(creature_list)        
        epoch += 1

    end_time = time.time()
    print "Time: " + str(end_time-start_time)
    print "Average fitness: " + str(avgFitness(creature_list))
    
    parents = selection(creature_list)
    new_creatures = crossover(parents)
    mutate(new_creatures)
    save_nets(new_creatures)
            
    creature_list = new_creatures
    epoch = 0
    generation += 1
    save_gen(generation)
    start_time = time.time()
    
    save_nets(creature_list)
    save_gen(generation)

print "CURRENT BUG: Program gets slower every generation. May have to do with breeding."
print "Narrowed bug down to issue with keras. Online results suggest keras.backend.clear_session()",
print "will clear memory. However, this throws an exception on my machine."
main()
