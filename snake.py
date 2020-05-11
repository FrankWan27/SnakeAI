from defs import *
import random

class Snake:

    body = []
    direction = Dir.RIGHT
    length = 1
    fitness = 0
    health = MAXHP
    fruit = (9, 9)

    def __init__(self, xPos=int(HEIGHT/2), yPos=int(WIDTH/2), direction=Dir.RIGHT):
        self.body = []
        self.fitness = 0
        self.body.append((xPos, yPos))
        self.body.append((xPos, yPos))
        self.direction = direction
        self.spawnFruit()

    def moveBody(self):

        preDist = self.distToFruit()
        head = self.getHead()
        #remove Tail
        self.body.pop(0)


        #add Head
        head = self.move(head, self.direction)

        if self.checkCollision(head):
            self.body.append(head)
            return False
        else:
            self.body.append(head)
            postDist = self.distToFruit()
            self.fitness += 1
            self.health -= 1
            return True

    def getHead(self):
        return self.body[self.getLength() - 1]


    def move(self, head, direction):
        return tuple(map(sum, zip(head, direction.value)))
    
    def checkCollision(self, head):
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True

        for bodyPart in self.body:
            if head[0] == bodyPart[0] and head[1] == bodyPart[1]:
                return True

        return False

    def getLength(self):
        return len(self.body)

    def spawnFruit(self):
        indexes = []
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if (x, y) not in self.body:
                    indexes.append((x, y))

        choice = random.choice(indexes)
        
        self.fruit = choice

    def checkEat(self):
        if self.getHead() == self.fruit:
            self.body.append(self.fruit)
            self.health = MAXHP
            self.spawnFruit()

    def distToFruit(self):
        return abs(self.fruit[0] - self.getHead()[0]) + abs(self.fruit[1] - self.getHead()[1])

    def calculateFitness(self):
        food = (self.getLength() - 2)
        tempFit = self.fitness + (2**food + food**2.1*500) - (food**1.2*(0.25*self.fitness)**1.3)
        if(tempFit < 0):
            tempFit = 0

        return tempFit
        