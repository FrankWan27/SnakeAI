import numpy as np
import pygame
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
    def initWeights(self, low = -5, high = 5):
        self.wInputToHidden = np.random.uniform(low, high, size=(self.numHidden, self.numInputs))
        self.wHiddenToOutput = np.random.uniform(low, high, size=(self.numOutputs, self.numHidden))
        #self.wInputToHidden = np.array([
        #    [0.4, 0, 0, 0, -5, 0, 0, 0, 5, 0, 0, 0], 
        #    [0, 0.3, 0, 0, 0, -5, 0, 0, 0, 5, 0, 0], 
         #   [0, 0, 0.1, 0, 0, 0, -5, 0, 0, 0, 5, 0], 
        #    [0, 0, -0.2, 0.5, 0, 0, 0, -5, 0, 0, 0, 5]
         #   ])


    #Return outputs given an input 
    def getOutputs(self, inputList):

        inputs = np.array(inputList, ndmin=2).T


        hiddenValues = sigmoid(np.dot(self.wInputToHidden, inputs))
        np.set_printoptions(suppress=True)
        #print(inputs)
        #print(self.wInputToHidden)

        outputs = sigmoid(np.dot(self.wHiddenToOutput, hiddenValues))
        #print(outputs)
        
        return outputs

    def getHidden(self, inputList):
        inputs = np.array(inputList, ndmin=2).T
        hiddenValues = sigmoid(np.dot(self.wInputToHidden, inputs))
        return hiddenValues

        
    def getOptimalOutput(self, inputList):
        output = self.getOutputs(inputList)
        return np.random.choice(np.flatnonzero(np.isclose(output, output.max())))


    def makeChild(self, mom, dad):
        self.wInputToHidden = mutateArray(mixArrays(mom.wInputToHidden, dad.wInputToHidden), MUTATION_RATE)
        self.wHiddenToOutput = mutateArray(mixArrays(mom.wHiddenToOutput, dad.wHiddenToOutput), MUTATION_RATE)


    def makeClone(self, mom):
        self.wInputToHidden = mutateArray(copy.deepcopy(mom.wInputToHidden), MUTATION_RATE)
        self.wHiddenToOutput = mutateArray(copy.deepcopy(mom.wHiddenToOutput), MUTATION_RATE)


class Nnets:
    #Constants
    popSize = POP_SIZE
    numParents = 10

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
        self.nnets = []
        self.currentNnet = 0
        self.generation = 0

    def createPop(self):
        for i in range(self.popSize):
            self.nnets.append(Nnet(self.species))

    def moveToNextNnet(self):
        self.currentNnet += 1
        if(self.currentNnet >= self.popSize):
            self.evolve()

    def getBestMove(self, inputList):
        return self.nnets[self.currentNnet].getOptimalOutput(inputList)

    def setFitnessIndex(self, index, score):
        self.nnets[index].fitness = score
        #print(self.nnets[self.currentNnet].wInputToHidden)
        #print(self.nnets[self.currentNnet].wHiddenToOutput)

        
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
        
    def setFitness(self, score):
        self.setFitnessIndex(self.currentNnet, score)

        

    def evolve(self):
        #get top 10 performers
        bestNnets = []

        for i in range(self.numParents):
            bestNnets.append(self.popBestNnet())

        #Rest of population will be children of top 10
        for i in range(self.popSize - self.numParents):
            mom = bestNnets[np.random.randint(self.numParents)]
            dad = bestNnets[np.random.randint(self.numParents)]
            bestNnets.append(self.makeChild(mom, dad))

        #Rest of population will be modified versions of top 10
        #for i in range(self.popSize - self.numParents):
        #    mom = bestNnets[np.random.randint(self.numParents)]
        #    bestNnets.append(self.makeClone(mom))

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
