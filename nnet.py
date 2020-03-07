import numpy as np
import scipy.special
from defs import *
import copy 



class Nnet:

    #Input: Grid (10 x 20) + currentShape (4 x 4) + currentShape.x + currentShape.y + nextShape x 4 + heldShape = 223
    numInputs = 223

    #Hidden Layer: I don't really know what I'm doing here so putting arbitrary value
    numHidden = 20

    #Output: moveLeft, moveRight, rotateLeft, rotateRight, fastDrop, slowDrop, holdBlock, doNothing
    numOutputs = 8

    #Weights: 20 x 223 matrix
    wInputToHidden = []

    #Weights: 8 x 20 matrix
    wHiddenToOutput = []

    #Fitness:Calculated by score/time
    fitness = -1

    def __init__(self, species):
        self.numInputs = species.value[0]
        self.numHidden = species.value[1]
        self.numOutputs = species.value[2]

        self.initWeights()

    #Randomly generates a uniformly distributed weights matrix
    def initWeights(self, low = -0.5, high = 0.5):
        self.wInputToHidden = np.random.uniform(-0.5, 0.5, size=(self.numHidden, self.numInputs))
        self.wHiddenToOutput = np.random.uniform(-0.5, 0.5, size=(self.numOutputs, self.numHidden))

    #Return outputs given an input 
    def getOutputs(self, inputList):

        #inputsList = list[298]

        #inputs = ndarray[298x1]
        inputs = np.array(inputList, ndmin=2).T

        hiddenValues = scipy.special.expit(np.dot(self.wInputToHidden, inputs))
        outputs = scipy.special.expit(np.dot(self.wHiddenToOutput, hiddenValues))

        return outputs

    def getOptimalOutput(self, inputList):
        return np.argmax(self.getOutputs(inputList))

    def makeChild(self, mom, dad):
        self.wInputToHidden = mixArrays(mom.wInputToHidden, dad.wInputToHidden)
        self.wHiddenToOutput = mixArrays(mom.wHiddenToOutput, dad.wHiddenToOutput)

    def makeClone(self, mom):
        self.wInputToHidden = mutateArray(copy.deepcopy(mom.wInputToHidden), 0.2)
        self.wHiddenToOutput = mutateArray(copy.deepcopy(mom.wHiddenToOutput), 0.2)


class Nnets:
    #Constants
    popSize = 50
    numParents = 10

    #Global vars
    generation = 0
    nnets = []
    currentNnet = 0
    species = Species.TETRIS

    #Trackers
    highscore = -1
    highestScore = -1
    highestGen = -1
    genAvg = -1
    genTotal = 0
    deltaAvg = 0
    pastAvg = 0



    def __init__(self, species):
        self.species = species

    def createPop(self):
        for i in range(self.popSize):
            self.nnets.append(Nnet(self.species))

    def moveToNextNnet(self):
        self.currentNnet += 1
        if(self.currentNnet >= self.popSize):
            self.evolve()

    def getBestMove(self, inputList):
        return self.nnets[self.currentNnet].getOptimalOutput(inputList)
        
    def setFitness(self, score):
        self.nnets[self.currentNnet].fitness = score
        
        #update highscores
        if score > self.highscore:
            self.highscore = score
            if self.highscore > self.highestScore:
                self.highestScore = score
                self.highestGen = self.generation

        #update averages
        self.genTotal += score
        self.genAvg = self.genTotal / (self.currentNnet + 1) 
        self.deltaAvg = self.genAvg - self.pastAvg

    def evolve(self):
        #get top 10 performers
        bestNnets = []

        for i in range(self.numParents):
            bestNnets.append(self.popBestNnet())

        #randomly create a full population of children
        #newNnets = []
        #for i in range(self.popSize):
        #    mom = bestNnets[np.random.randint(self.numParents)]
        #    dad = bestNnets[np.random.randint(self.numParents)]
        #    newNnets.append(self.makeChild(mom, dad))

        #Rest of population will be modified versions of top 10
        for i in range(self.popSize - self.numParents):
            mom = bestNnets[np.random.randint(self.numParents)]
            bestNnets.append(self.makeClone(mom))

        self.generation += 1
        self.currentNnet = 0
        self.highscore = 0
        self.pastAvg = self.genAvg
        self.genTotal = 0
        self.nnets = bestNnets

    def makeChild(self, mom, dad):
        child = Nnet(self.species)
        child.makeChild(mom, dad)
        return child

    def makeClone(self, mom):
        child = Nnet(self.species)
        child.makeClone(mom)
        return child



    def popBestNnet(self):
        bestFit = -1
        bestIndex = 0
        for i in range(len(self.nnets)):
            if self.nnets[i].fitness > bestFit:
                bestIndex = i
                bestFit = self.nnets[i].fitness

        return self.nnets.pop(bestIndex)

