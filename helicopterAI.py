#import necessary libraries
#pip install pygame
import pygame
import numpy as np
import random
import sys
import os
from nnet import Nnets
from defs import *
from wall import Walls
from heli import Helis

# PyInstaller adds this attribute
if getattr(sys, 'frozen', False):
    # Running in a bundle
    CurrentPath = sys._MEIPASS
else:
    # Running in normal Python environment
    CurrentPath = os.path.dirname(__file__)

#setup constants
player = False

#setup global vars
gameDisplay = ''
inputs = []
walls = ''
helis = ''
#Core game loop
def startGame():
    global gameDisplay
    global walls
    global helis
    pygame.init()
    gameDisplay = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
    pygame.display.set_caption('Helicopter AI')
    runloop = True
    clock = pygame.time.Clock()
    
    walls = Walls(gameDisplay)
    helis = Helis(gameDisplay)

    dt = 0
    gameTime = 0

    while runloop:        

        gameDisplay.fill(pygame.Color('gray'))

        #Break loop if we quit
        runloop = handleInput()
        #Get AI's best move

        #if not player:
        #    doBestMove(getNeuralInput(snakePlayer), snakePlayer)

        dt = clock.tick(FPS)
        gameTime += dt

        walls.update(dt)
        numAlive = helis.update(dt, walls.walls)

        if numAlive <= 0:
            walls = Walls(gameDisplay)
            helis.evolve()
            gameTime = 0


        #showGrid()
        showDebug(dt, gameTime, numAlive)
        #showNnet(snek)

        pygame.display.update()

    pygame.display.quit()
    pygame.quit()

def showLabel(data, text, x, y):
    font = pygame.font.Font(os.path.join(CurrentPath, 'fonts/abel.ttf'), 20)
    label = font.render('{} {}'.format(text, data), 1, (40,40,250))
    gameDisplay.blit(label, (x, y))
    return y + 20

def showDebug(dt, gameTime, numAlive):
    xOffset = 10
    yOffset = 2
    yOffset = showLabel(round(1000/dt, 2), 'FPS: ', xOffset, yOffset)
    yOffset = showLabel(round(gameTime/1000, 2),'Game Time: ', xOffset, yOffset)
    yOffset = showLabel(helis.nnets.generation, 'Current Generation: ', xOffset, yOffset)
    yOffset = showLabel(numAlive, 'Current Alive: ', xOffset, yOffset)
    yOffset = showLabel(helis.nnets.highestGen, 'Best Gen So Far: ', xOffset, yOffset)

    yOffset = 700
    yOffset = showLabel(int(helis.nnets.genAvg), 'Current Gen Average: ', xOffset, yOffset)
    yOffset = showLabel(int(helis.nnets.deltaAvg), 'Change From Last Gen: ', xOffset, yOffset)
    yOffset = showLabel(helis.nnets.highscore, 'Highscore (This Gen): ', xOffset, yOffset)
    yOffset = showLabel(helis.nnets.highestScore, 'Highest Score So Far: ', xOffset, yOffset)

def showNnet(nnets):
    global inputs
    xOffset = 600
    yOffset = 0
    
    pygame.draw.rect(gameDisplay, (60, 60, 60), (xOffset, yOffset, 600, 600))

    yOffset = 50

    nnet = nnets.nnets[nnets.currentNnet]
    outputs = nnet.getOutputs(inputs)

    #Draw lines
    for i in range(len(inputs)):
        for j in range(len(outputs)):
            color = (nnet.wInputToHidden[j][i] + 5) / 10
            drawColor = ((int)(255 - color * 255), (int)(color * 255), 0)
            pygame.draw.line(gameDisplay, drawColor, (xOffset + 100, yOffset + (int)(i / len(inputs) * 550)),(xOffset + 400, yOffset + (int)(j / len(outputs) * 550)))

    #Draw inputs
    for i in range(len(inputs)):
        color = inputs[i]
        drawColor = ((int)(color * 255), (int)(color * 255), (int) (color * 255))
        #pygame.draw.circle(gameDisplay, pygame.Color('white'), (xOffset + 100, yOffset + (int)(i / len(inputs) * 550)), 20, 1)
        pygame.draw.circle(gameDisplay, drawColor, (xOffset + 100, yOffset + (int)(i / len(inputs) * 550)), 19)


    #Draw output
    dirs = ['Left', 'Right', 'Up', 'Down']
    for i in range(len(outputs)):
        color = outputs[i]
        drawColor = ((int)(color * 255), (int)(color * 255), (int) (color * 255))
        #pygame.draw.circle(gameDisplay, pygame.Color('white'), (xOffset + 400, yOffset + (int)(i / len(outputs) * 550)), 20, 1)
        pygame.draw.circle(gameDisplay, drawColor, (xOffset + 400, yOffset + (int)(i / len(outputs) * 550)), 19)

        showLabel(dirs[i], 'Move', xOffset + 450, yOffset + (int)(i / len(outputs) * 550))

            


    #wInputsToHidden = nnet.wInputToHidden

#Handle keyboard input
def handleInput():
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and player:
                if event.key == pygame.K_LEFT:
                    moveLeft(snakePlayer)
                if event.key == pygame.K_RIGHT:
                    moveRight(snakePlayer)
                if event.key == pygame.K_UP:
                    moveUp(snakePlayer)
                if event.key == pygame.K_DOWN:
                    moveDown(snakePlayer)
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    #Manual Kill Current NNet
                    snek.setFitness(-1)
                    snek.moveToNextNnet()
                    resetGame()
    return True

#Current player or Nnet lost
def handleLoss():    
    #update fitness of current Nnet
    snek.setFitness(snakePlayer.calculateFitness())
    snek.moveToNextNnet()
    resetGame()
    
def moveUp(s):
    if s.direction != Dir.DOWN:
        s.direction = Dir.UP

    
def moveDown(s):
    if s.direction != Dir.UP:
        s.direction = Dir.DOWN

def getNeuralInput(snakePlayer):
    global grid
    global inputs
    inputs = []

    return inputs


def doBestMove(inputs, snakePlayer):
    # 0 : moveLeft
    # 1 : moveRight
    # 2 : moveUp
    # 3 : moveDown

    bestMove = snek.getBestMove(inputs)


    if bestMove == 0:
        #print('Move Left')
        moveLeft(snakePlayer)
    elif bestMove == 1:
        #print('Move Right')
        moveRight(snakePlayer)
    elif bestMove == 2:
        moveUp(snakePlayer)
    else:
        moveDown(snakePlayer)