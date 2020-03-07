import numpy as np
import scipy.special
import defs



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
        self.fitness = -1

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
        self.wInputToHidden = Nnet.mixArrays(mom.wInputToHidden, dad.wInputToHidden)
        self.wHiddenToOutput = Nnet.mixArrays(mom.wHiddenToOutput, dad.wHiddenToOutput)


    #Simply picks a value between the two parents for every weight v
    def mixArrays(a1, a2):
        rows = a1.shape[0]
        cols = a1.shape[1]
        
        output = np.zeros((rows, cols))

        for x in range(rows):
            for y in range(cols):
                    if a1[x][y] < a2[x][y]:
                        output[x][y] = np.random.uniform(a1[x][y], a2[x][y])
                    else:
                        output[x][y] = np.random.uniform(a2[x][y], a1[x][y])

        return output


class Nnets:
    #Constants
    popSize = 50
    numParents = 10

    #Global vars
    generation = 0
    nnets = []
    currentNnet = 0
    species = defs.Species.TETRIS

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
        newNnets = []
        for i in range(self.popSize):
            mom = bestNnets[np.random.randint(self.numParents)]
            dad = bestNnets[np.random.randint(self.numParents)]
            newNnets.append(self.makeChild(mom, dad))

        self.generation += 1
        self.currentNnet = 0
        self.highscore = 0
        self.pastAvg = self.genAvg
        self.genTotal = 0
        self.nnets = newNnets

    def makeChild(self, mom, dad):
        child = Nnet(self.species)
        child.makeChild(mom, dad)
        return child


    def popBestNnet(self):
        bestFit = -1
        bestIndex = 0
        for i in range(len(self.nnets)):
            if self.nnets[i].fitness > bestFit:
                bestIndex = i
                bestFit = self.nnets[i].fitness

        return self.nnets.pop(bestIndex)

