import numpy, pickle
from keras.models import Sequential, model_from_json
from keras.layers import Dense
from vector import Vector

#numpy.random.seed(1)

class CreatureNet:
    def __init__(self):
        self.xmodel = Sequential()
        self.ymodel = Sequential()
        self.buildNet()

    def buildNet(self):
        self.xmodel.add(Dense(units=8, input_dim=2, activation='relu'))
        self.xmodel.add(Dense(units=4, activation='relu'))
        self.xmodel.add(Dense(units=1, activation='tanh'))

        self.ymodel.add(Dense(units=8, input_dim=2, activation='relu'))
        self.ymodel.add(Dense(units=4, activation='relu'))
        self.ymodel.add(Dense(units=1, activation='tanh'))

        self.xmodel.compile(loss='binary_crossentropy',optimizer='adam',
                            metrics=['accuracy'])
        self.ymodel.compile(loss='binary_crossentropy',optimizer='adam',
                            metrics=['accuracy'])

    def randomizeWeights(self):
        #use only after the net has been built
        pass

    def predict(self, bugx, bugy, foodx, foody):
        inx = numpy.array([[bugx, foodx]])
        iny = numpy.array([[bugy, foody]])
        predictx = self.xmodel.predict(inx)
        predicty = self.ymodel.predict(iny)

        return predictx, predicty
