#import necessary libraries
#pip install pygame
import pygame
import numpy as np
import math
import random
import sys
import os
from nnet import Nnets
from defs import *
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


#setup global vars
gameDisplay = ''
grid = np.zeros((WIDTH, HEIGHT))
inputs = []

snakePlayer = Snake()

snek = Nnets(Species.SNAKE)

#Core game loop
def startGame():
    global gameDisplay
    global snakePlayer
    pygame.init()
    gameDisplay = pygame.display.set_mode((1200, 600))
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

        clearGrid()
        updateGrid(snakePlayer.body, 1)

        snakePlayer.checkEat()
        updateGrid([snakePlayer.fruit], 2)

        if(snakePlayer.health < 0):
            handleLoss()


        if not player:
            doBestMove(getNeuralInput(snakePlayer), snakePlayer)

        dt = clock.tick(FPS)
        gameTime += dt

        if not snakePlayer.moveBody():
            handleLoss()

        clearGrid()
        updateGrid(snakePlayer.body, 1)

        snakePlayer.checkEat()
        updateGrid([snakePlayer.fruit], 2)


        #Draw everything to screen
        gameDisplay.fill(pygame.Color('gray'))
        showGrid()
        showDebug(dt, gameTime)
        showNnet(snek)

        pygame.display.update()

    pygame.display.quit()
    pygame.quit()

def resetGame():
    global grid
    global score
    global snakePlayer
    #random.seed(1)
    grid = np.zeros((WIDTH, HEIGHT))
    spawnFruit()
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
    yOffset = showLabel(snakePlayer.calculateFitness(), 'Current Fitness ', xOffset, yOffset)

    yOffset = 500
    yOffset = showLabel(int(snek.genAvg), 'Current Gen Average: ', xOffset, yOffset)
    yOffset = showLabel(int(snek.deltaAvg), 'Change From Last Gen: ', xOffset, yOffset)
    yOffset = showLabel(snek.highscore, 'Highscore (This Gen): ', xOffset, yOffset)
    yOffset = showLabel(snek.highestScore, 'Highest Score So Far: ', xOffset, yOffset)

def showNnet(nnets):
    global inputs
    xOffset = 600
    yOffset = 0
    
    pygame.draw.rect(gameDisplay, (60, 60, 60), (xOffset, yOffset, 600, 600))

    yOffset = 50

    nnet = nnets.nnets[nnets.currentNnet]
    hidden = nnet.getHidden(inputs)
    hidden2 = nnet.getHidden2(inputs)
    outputs = nnet.getOutputs(inputs)

    inputX = 100
    hiddenX = 233
    hidden2X = 366
    outputX = 500



    #Draw lines
    for i in range(len(inputs)):
        for j in range(len(hidden)):
            color = (nnet.wInputToHidden[j][i] + 1) / 2
            drawColor = ((int)(255 - color * 255), (int)(color * 255), 0)
            pygame.draw.line(gameDisplay, drawColor, (xOffset + inputX, yOffset + (int)(i / len(inputs) * 550)),(xOffset + hiddenX, yOffset + (int)(j / len(hidden) * 550)))
    
    for i in range(len(hidden)):
        for j in range(len(hidden2)):
            color = (nnet.wHiddenToHidden[j][i] + 1) / 2
            drawColor = ((int)(255 - color * 255), (int)(color * 255), 0)
            pygame.draw.line(gameDisplay, drawColor, (xOffset + hiddenX, yOffset + (int)(i / len(hidden) * 550)),(xOffset + hidden2X, yOffset + (int)(j / len(hidden2) * 550)))

    for i in range(len(hidden2)):
        for j in range(len(outputs)):
            color = (nnet.wHiddenToOutput[j][i] + 1) / 2
            drawColor = ((int)(255 - color * 255), (int)(color * 255), 0)
            pygame.draw.line(gameDisplay, drawColor, (xOffset + hidden2X, yOffset + (int)(i / len(hidden2) * 550)),(xOffset + outputX, yOffset + 40 + (int)(j / len(outputs) * 550)))


    #Draw inputs
    for i in range(len(inputs)):
        color = inputs[i]
        drawColor = ((int)(color * 255), (int)(color * 255), (int) (color * 255))
        #pygame.draw.circle(gameDisplay, pygame.Color('white'), (xOffset + 100, yOffset + (int)(i / len(inputs) * 550)), 20, 1)
        pygame.draw.circle(gameDisplay, drawColor, (xOffset + inputX, yOffset + (int)(i / len(inputs) * 550)), 19)

    #Draw hidden
    for i in range(len(hidden)):
        color = hidden[i]
        drawColor = ((int)(color * 255), (int)(color * 255), (int) (color * 255))
        #pygame.draw.circle(gameDisplay, pygame.Color('white'), (xOffset + 100, yOffset + (int)(i / len(inputs) * 550)), 20, 1)
        pygame.draw.circle(gameDisplay, drawColor, (xOffset + hiddenX, yOffset + (int)(i / len(hidden) * 550)), 19)
    
    #Draw hidden
    for i in range(len(hidden2)):
        color = hidden2[i]
        drawColor = ((int)(color * 255), (int)(color * 255), (int) (color * 255))
        #pygame.draw.circle(gameDisplay, pygame.Color('white'), (xOffset + 100, yOffset + (int)(i / len(inputs) * 550)), 20, 1)
        pygame.draw.circle(gameDisplay, drawColor, (xOffset + hidden2X, yOffset + (int)(i / len(hidden2) * 550)), 19)



    #Draw output
    dirs = ['Left', 'Right', 'Up', 'Down']
    for i in range(len(outputs)):
        color = outputs[i]
        drawColor = ((int)(color * 255), (int)(color * 255), (int) (color * 255))
        #pygame.draw.circle(gameDisplay, pygame.Color('white'), (xOffset + 400, yOffset + (int)(i / len(outputs) * 550)), 20, 1)
        pygame.draw.circle(gameDisplay, drawColor, (xOffset + outputX, 40 + yOffset + (int)(i / len(outputs) * 550)), 19)

        showLabel(dirs[i], '', xOffset + 530, yOffset + (int)(i / len(outputs) * 550))

            


    #wInputsToHidden = nnet.wInputToHidden




def showGrid():
    xOffset = 0
    yOffset = 0
    xSize = 600 / WIDTH
    ySize = 600 / HEIGHT
    #pygame.draw.rect(gameDisplay, pygame.Color('black'), (xOffset - 10, yOffset - 10, 320, 320))

    for x in range(WIDTH):
        for y in range(HEIGHT):
            if(grid[x][y] == 1):
                pygame.draw.rect(gameDisplay, pygame.Color('white'), (xOffset + x * xSize, yOffset + y * ySize, xSize - 1, ySize - 1))
            if(grid[x][y] == 2):
                pygame.draw.rect(gameDisplay, pygame.Color('purple'), (xOffset + x * xSize, yOffset + y * ySize, xSize - 1, ySize - 1))

#Handle keyboard input
def handleInput():
    global FPS
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
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_SPACE:
                        #Manual Kill Current NNet
                        snek.setFitness(-1)
                        snek.moveToNextNnet()
                        resetGame()
                    if event.key == pygame.K_UP:
                        FPS += 5
                    if event.key == pygame.K_DOWN:
                        FPS -= 5
                    
    return True

#Current player or Nnet lost
def handleLoss():    
    #update fitness of current Nnet
    snek.setFitness(snakePlayer.calculateFitness())
    snek.moveToNextNnet()
    resetGame()

def moveLeft(s):
    if s.direction != Dir.RIGHT:
        s.direction = Dir.LEFT

    
def moveRight(s):
    if s.direction != Dir.LEFT:
        s.direction = Dir.RIGHT

    
def moveUp(s):
    if s.direction != Dir.DOWN:
        s.direction = Dir.UP

    
def moveDown(s):
    if s.direction != Dir.UP:
        s.direction = Dir.DOWN

def turnLeft(s):
    if s.direction == Dir.UP:
        s.direction = Dir.LEFT
    if s.direction == Dir.LEFT:
        s.direction = Dir.DOWN
    if s.direction == Dir.DOWN:
        s.direction = Dir.RIGHT
    if s.direction == Dir.RIGHT:
        s.direction = Dir.UP

def turnRight(s):
    if s.direction == Dir.UP:
        s.direction = Dir.RIGHT
    if s.direction == Dir.RIGHT:
        s.direction = Dir.DOWN
    if s.direction == Dir.DOWN:
        s.direction = Dir.LEFT
    if s.direction == Dir.LEFT:
        s.direction = Dir.UP

def clearGrid():
    global grid
    grid = np.zeros((WIDTH, HEIGHT))

def updateGrid(toDraw, num):
    global grid
    for dot in toDraw:
        grid[dot[0]][dot[1]] = num

#NOT USED (Moved to Snake Class)
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

#NOT USED (Moved to Snake Class)
def checkEat(snakePlayer):
    if snakePlayer.getHead() == fruit[0]:
        snakePlayer.body.append(fruit[0])
        snakePlayer.health = MAXHP
        spawnFruit()


def getNeuralInput(snakePlayer):
    global grid
    global inputs
    inputs = []
    head = snakePlayer.getHead()

    #get distance to walls left (normalized)
    inputs.append(head[0] / (WIDTH - 1)) 
    #right
    inputs.append((WIDTH - head[0] - 1) / (WIDTH - 1))
    #up
    inputs.append(head[1] / (HEIGHT - 1))
    #down
    inputs.append((WIDTH - head[1] - 1) / (HEIGHT - 1))

    #get distance to self
    distToSelf = getDistanceToObj(head, 1)

    #if head[0] > 0 and distToSelf[0] > 1:
    #    inputs.append(1)
    #else:
    #    inputs.append(0)

    #if head[0] < WIDTH - 1 and distToSelf[1] > 1:
    #    inputs.append(1)
    #else:
    #    inputs.append(0)

    #if head[1] > 0 and distToSelf[2] > 1:
    #    inputs.append(1)
    #else:
    #    inputs.append(0)

    #if head[1] < HEIGHT - 1 and distToSelf[3] > 1:
    #    inputs.append(1)
    #else:
    #    inputs.append(0)


    inputs.append(1 - distToSelf[0] / (WIDTH - 1))
    inputs.append(1 - distToSelf[1] / (WIDTH - 1))
    inputs.append(1 - distToSelf[2] / (HEIGHT - 1))
    inputs.append(1 - distToSelf[3] / (HEIGHT - 1))

    #get distance to fruit
    distToFruit = getDistanceToObj(head, 2)

    #if distToFruit[0] == 1:
    #    inputs.append(1)
    #else:
    #    inputs.append(0)

    #if distToFruit[1] == 1:
    #    inputs.append(1)
    #else:
    #    inputs.append(0)

    #if distToFruit[2] == 1:
    #    inputs.append(1)
    #else:
    #    inputs.append(0)    

    #if distToFruit[3] == 1:
    #    inputs.append(1)
    #else:
    #    inputs.append(0)
    inputs.append(math.ceil(1 - distToFruit[0] / (WIDTH - 1)))
    inputs.append(math.ceil(1 - distToFruit[1] / (WIDTH - 1)))
    inputs.append(math.ceil(1 - distToFruit[2] / (HEIGHT - 1)))
    inputs.append(math.ceil(1 - distToFruit[3] / (HEIGHT - 1)))


    #inputs.append(snakePlayer.direction.value[0])
    #inputs.append(snakePlayer.direction.value[1])
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

def getDistanceToObj(head, num):
    left = WIDTH - 1
    right = WIDTH - 1
    up = HEIGHT - 1
    down = HEIGHT - 1

    count = 1
    i = head[0] - 1
    while i >= 0:
        if grid[i][head[1]] == num:
            left = count
            break
        else:
            count += 1
        i -= 1
    
    count = 1
    i = head[0] + 1
    while i < WIDTH:
        if grid[i][head[1]] == num:
            right = count
            break
        else:
            count += 1
        i += 1
    
    count = 1
    i = head[1] - 1
    while i >= 0:
        if grid[head[0]][i] == num:
            up = count
            break
        else:
            count += 1
        i -= 1
    
    count = 1
    i = head[1] + 1
    while i < HEIGHT:
        if grid[head[0]][i] == num:
            down = count
            break
        else:
            count += 1
        i += 1

    return (left, right, up, down)
    