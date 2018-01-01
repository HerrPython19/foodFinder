import pygame, creatures, random, pickle, time
from pygame.locals import *
from sys import argv
from numpy import concatenate

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
    clist = clist[:5]

    for i in range(5):
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

    #breeds 6 children from initial x parents
    while len(childlist) < 50:
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
        child_w1[0][0] = concatenate([parent1_w1[0][0][:pivot],parent2_w1[0][0][pivot:]])
        pivot = random.randint(0,4)
        child_w2[0][0] = concatenate([parent1_w2[0][0][:pivot],parent2_w2[0][0][pivot:]])
        pivot = random.randint(0,4)
        child_w3[0][0] = concatenate([parent1_w3[0][0][:pivot],parent2_w3[0][0][pivot:]])
        pivot = random.randint(0,4)
        child_w4[0][0] = concatenate([parent1_w4[0][0][:pivot],parent2_w4[0][0][pivot:]])

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
    pop_size = 50

    #determine if we're using saved population (-saved argument at cli)
    if len(argv) > 1:
        if argv[1] == "-saved":
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

    #Run x Epochs of Simulation
    print "Starting Generation", generation
    while epoch < max_epoch:
        if epoch % 10 == 0:
            print "Epoch: ", epoch
        updateCreatures(creature_list)        
        epoch += 1

    print "Finished Simulation"
    print "Average fitness: " + str(avgFitness(creature_list))

    print "Breeding..."
    #Breed new population, and mutate
    parents = selection(creature_list)
    print "Parents Selected"
    new_creatures = crossover(parents)
    print "Children Bred"
    mutate(new_creatures)
    print "Children Mutated"
            
    creature_list = new_creatures
    epoch = 0
    generation += 1
    
    save_nets(creature_list)
    print "Saved Weights of Neural Networks to Disk"
    save_gen(generation)
    print "Saved Generation to Disk"

main()
