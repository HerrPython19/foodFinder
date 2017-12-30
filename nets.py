import numpy, pickle, threading
from keras.models import Sequential, model_from_json
from keras.layers import Dense
from vector import Vector

numpy.random.seed(1)

class CreatureNet:
    def __init__(self, creature, food):
        self.creature = creature
        self.food = food
        self.xmodel = Sequential()
        self.ymodel = Sequential()
        self.xxdata = []
        self.xydata = []
        self.yxdata = []
        self.yydata = []

    def buildModels(self):
        self.xmodel.add(Dense(units=10, input_dim=4, activation='relu'))
        self.xmodel.add(Dense(units=1, activation='tanh'))
        self.ymodel.add(Dense(units=10, input_dim=4, activation='relu'))
        self.ymodel.add(Dense(units=1, activation='tanh'))

        self.xmodel.compile(loss='mean_squared_error',optimizer='adam',
                           metrics=['accuracy'])
        self.ymodel.compile(loss='mean_squared_error',optimizer='adam',
                           metrics=['accuracy'])

    def collectData(self):
        currxxdata = [self.creature.pos.x,
                    self.creature.vel.x,
                    self.creature.acc.x,
                    self.food.pos.x]

        currxydata =[self.creature.pos.y,
                     self.creature.vel.y,
                     self.creature.acc.y,
                     self.food.pos.y]

        newyxdata = self.xmodel.predict(numpy.array([currxxdata]))
        newyydata = self.ymodel.predict(numpy.array([currxydata]))

        togo = Vector(self.food.pos.x,self.food.pos.y)
        togo.x -= self.creature.pos.x
        togo.y -= self.creature.pos.y
        togo.normalize()
        #print newyxdata,newyydata

        self.xxdata.append(currxxdata)
        self.xydata.append(currxydata)
        self.yxdata.append(togo.x)
        self.yydata.append(togo.y)
        
        self.creature.vel.set(newyxdata[0]*2,newyydata[0]*2)
        self.creature.step()

    def play(self):
        currxxdata = [self.creature.pos.x,
                    self.creature.vel.x,
                    self.creature.acc.x,
                    self.food.pos.x]

        currxydata =[self.creature.pos.y,
                     self.creature.vel.y,
                     self.creature.acc.y,
                     self.food.pos.y]

        newyxdata = self.model.predict(numpy.array([currxxdata]))
        newyydata = self.model.predict(numpy.array([currxydata]))
        self.creature.vel.set(newyxdata[0]*2,newyydata[0]*2)
        self.creature.step()

    def saveData(self):
        xx = numpy.array(self.xxdata)
        xy = numpy.array(self.xydata)
        yx = numpy.array(self.yxdata)
        yy = numpy.array(self.yydata)

        f = open("xxdata.pickle","wb")
        pickle.dump(xx,f)
        f.close()

        f = open("xydata.pickle","wb")
        pickle.dump(xy,f)
        f.close()

        f = open("yxdata.pickle","wb")
        pickle.dump(yx,f)
        f.close()

        f = open("yydata.pickle","wb")
        pickle.dump(yy,f)
        f.close()

    def train(self):
        self.t1 = threading.Thread(target=self.model.fit,args=(
                        numpy.array(self.xdata),numpy.array(self.ydata))
                                   ,kwargs={'epochs':1000,'batch_size':100})
        self.t1.start()

    def dumbtrain(self):
        f = open("xxdata.pickle","rb")
        g = open("xydata.pickle","rb")
        h = open("yxdata.pickle","rb")
        j = open("yydata.pickle","rb")
        self.xxdata = pickle.load(f)
        self.xydata = pickle.load(g)
        self.yxdata = pickle.load(h)
        self.yydata = pickle.load(j)
        
        f.close()
        g.close()
        a = numpy.array(self.xxdata)
        b = numpy.array(self.yxdata)
        c = numpy.array(self.xydata)
        d = numpy.array(self.yydata)
        #print a,b
        self.xmodel.fit(a,b,epochs=1000,batch_size=20)
        self.ymodel.fit(c,d,epochs=1000,batch_size=20)
    
if __name__ == "__main__":
    a = CreatureNet(None, None)
    a.buildModels()
    a.dumbtrain()
