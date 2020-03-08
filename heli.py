import pygame
import random
from defs import *
from nnet import Nnets
import numpy as np

class Heli():

    color = pygame.Color('blue')

    def __init__(self, gameDisplay, nnet):
        self.gameDisplay = gameDisplay
        self.alive = True
        self.fitness = 0
        self.lifespan = 0
        self.nnet = nnet
        self.rect = pygame.Rect(50, DISPLAY_H/2, 20, 20)

    def reset(self):
        self.alive = True
        self.fitness = 0
        self.lifespan = 0
        self.rect = pygame.Rect(50, DISPLAY_H/2, 20, 20)

    def moveDown(self, dt):
        self.rect.centery += dt * 0.2
        if self.rect.bottom > DISPLAY_H:          
            self.alive = False

    def moveUp(self, dt):
        self.rect.centery -= dt * 0.2
        if self.rect.top < 0:
            self.alive = False

    def draw(self):
        pygame.draw.rect(self.gameDisplay, self.color, self.rect)

    def setFitness(self, wall):
        self.fitness = self.lifespan - (abs(self.rect.centery - wall.rect.centery))

    def checkCollision(self, walls):
        for wall in walls:
            if wall.rect.colliderect(self.rect):
                self.alive = False
                self.setFitness(wall)
                self.nnet.fitness = self.fitness
                break

    def update(self, dt, walls):
        if self.alive:
            move = self.nnet.getOptimalOutput(self.getInputs(walls))
            if move == 0:
                self.moveUp(dt)
            else:
                self.moveDown(dt)
            self.lifespan += dt
            self.fitness = self.lifespan
            self.draw()
            self.checkCollision(walls)


    def getInputs(self, walls):

        hDist = walls[0].rect.centerx - self.rect.centerx
        vDist = walls[0].rect.centery - self.rect.centery

        inputs = [hDist / DISPLAY_W, vDist / DISPLAY_H]

        return inputs



class Helis():

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.helis = []
        self.nnets = Nnets(species=Species.HELI)
        self.nnets.createPop()
        self.createGeneration()

    def update(self, dt, walls):
        numAlive = 0
        for i in range(len(self.helis)):
            heli = self.helis[i]
            heli.update(dt, walls)
            if heli.alive:
                self.nnets.setFitnessIndex(i, heli.fitness)
                numAlive += 1
        return numAlive

    def createGeneration(self):
        self.helis = []
        for i in range(POP_SIZE):
            self.helis.append(Heli(self.gameDisplay, self.nnets.nnets[i]))

    def evolve(self):
        self.nnets.evolve()
        self.helis = []

        for i in range(POP_SIZE):
            self.helis.append(Heli(self.gameDisplay, self.nnets.nnets[i]))
