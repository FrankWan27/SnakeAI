#import necessary libraries
#pip install pygame
import pygame
import numpy as np
import random
import sys
import os
from nnet import Nnets
import defs
from snake import Snake

# PyInstaller adds this attribute
if getattr(sys, 'frozen', False):
    # Running in a bundle
    CurrentPath = sys._MEIPASS
else:
    # Running in normal Python environment
    CurrentPath = os.path.dirname(__file__)

#setup constants
player = False
WIDTH = 10
HEIGHT = 10

#setup global vars
gameDisplay = ''
grid = np.zeros((WIDTH, HEIGHT))
fruit = [(9, 9)]

snakePlayer = Snake()

snek = Nnets(defs.Species.SNAKE)

#Core game loop
def startGame():
    global gameDisplay
    global snakePlayer
    pygame.init()
    gameDisplay = pygame.display.set_mode((600, 600))
    pygame.display.set_caption('Snake AI')
    resetGame()
    spawnFruit()

    runloop = True
    clock = pygame.time.Clock()
    
    dt = 0
    gameTime = 0

    snek.createPop()

    while runloop:        
        #Break loop if we quit
        runloop = handleInput()
        #Get AI's best move
        if not player:
            doBestMove(getNeuralInput(snakePlayer), snakePlayer)

        dt = clock.tick(400)
        gameTime += dt

        if snakePlayer.moveBody():
            clearGrid()
            updateGrid(snakePlayer.body, 1)
        else:
            handleLoss()

        checkEat(snakePlayer)
        updateGrid(fruit, 2)


        #Draw everything to screen
        gameDisplay.fill(pygame.Color('gray'))
        showDebug(dt, gameTime)
        showScore()
        showGrid()

        pygame.display.update()

    pygame.display.quit()
    pygame.quit()

def resetGame():
    global grid
    global score
    global snakePlayer
    grid = np.zeros((WIDTH, HEIGHT))
    score = 0
    snakePlayer = Snake()

def showLabel(data, text, x, y):
    font = pygame.font.Font(os.path.join(CurrentPath, 'fonts/abel.ttf'), 20)
    label = font.render('{} {}'.format(text, data), 1, (40,40,250))
    gameDisplay.blit(label, (x, y))
    return y + 20

def showDebug(dt, gameTime):
    xOffset = 10
    yOffset = 2
    yOffset = showLabel(round(1000/dt, 2), 'FPS: ', xOffset, yOffset)
    yOffset = showLabel(round(gameTime/1000, 2),'Game Time: ', xOffset, yOffset)
    yOffset = showLabel(snek.generation, 'Current Generation: ', xOffset, yOffset)
    yOffset = showLabel(snek.currentNnet, 'Current Nnet: ', xOffset, yOffset)
    yOffset = showLabel(snek.highestGen, 'Best Gen So Far: ', xOffset, yOffset)

    yOffset += 408
    yOffset = showLabel(int(snek.genAvg), 'Current Gen Average: ', xOffset, yOffset)
    yOffset = showLabel(int(snek.deltaAvg), 'Change From Last Gen: ', xOffset, yOffset)
    yOffset = showLabel(snek.highscore, 'Highscore (This Gen): ', xOffset, yOffset)
    yOffset = showLabel(snek.highestScore, 'Highest Score So Far: ', xOffset, yOffset)

def showScore():
    font = pygame.font.Font(os.path.join(CurrentPath, 'fonts/abel.ttf'), 80)
    label = font.render('{}'.format(score), 1, (0, 0, 0))
    offset = font.size('{}'.format(score))
    gameDisplay.blit(label, (390 - offset[0], 707))

def showGrid():
    xOffset = 150
    yOffset = 150
    pygame.draw.rect(gameDisplay, pygame.Color('black'), (xOffset - 10, yOffset - 10, 320, 320))

    for x in range(WIDTH):
        for y in range(HEIGHT):
            if(grid[x][y] == 1):
                pygame.draw.rect(gameDisplay, pygame.Color('white'), (xOffset + x * 30, yOffset + y * 30, 29, 29))
            if(grid[x][y] == 2):
                pygame.draw.rect(gameDisplay, pygame.Color('purple'), (xOffset + x * 30, yOffset + y * 30, 29, 29))

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

    return True

#Current player or Nnet lost
def handleLoss():    
    #update fitness of current Nnet
    snek.setFitness(snakePlayer.getLength() * 1000 + snakePlayer.lifetime)
    snek.moveToNextNnet()
    resetGame()

def moveLeft(s):
    if s.direction is not defs.Dir.RIGHT:
        s.direction = defs.Dir.LEFT

    
def moveRight(s):
    if s.direction is not defs.Dir.LEFT:
        s.direction = defs.Dir.RIGHT

    
def moveUp(s):
    if s.direction is not defs.Dir.DOWN:
        s.direction = defs.Dir.UP

    
def moveDown(s):
    if s.direction is not defs.Dir.UP:
        s.direction = defs.Dir.DOWN

def clearGrid():
    global grid
    grid = np.zeros((WIDTH, HEIGHT))

def updateGrid(toDraw, num):
    global grid
    for dot in toDraw:
        grid[dot[0]][dot[1]] = num

def spawnFruit():
    global grid
    global fruit
    indexes = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if grid[x][y] == 0:
                indexes.append(x * HEIGHT + y)

    choice = random.choice(indexes)

    y = choice % HEIGHT
    x = int(choice / HEIGHT)

    fruit = [(x, y)]

def checkEat(snakePlayer):
    if snakePlayer.getHead() == fruit[0]:
        snakePlayer.body.append(fruit[0])
        spawnFruit()


def getNeuralInput(snakePlayer):
    global grid
    inputs = []
    #Add grid
    defs.arrayToList(grid, inputs)

    #Add current x and y and direction
    head = snakePlayer.getHead()
    inputs.append(head[0])
    inputs.append(head[1])
    inputs.append(snakePlayer.direction.value[0])
    inputs.append(snakePlayer.direction.value[1])

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
        #print('Move Up')
        moveUp(snakePlayer)
    elif bestMove == 3:
        #print('Move Down')
        moveDown(snakePlayer)
    else:
        return
        #print('Doing Nothing')
