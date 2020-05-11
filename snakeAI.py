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
def startGame(filename = None):
    global gameDisplay
    global snakePlayer
    pygame.init()
    gameDisplay = pygame.display.set_mode((1200, 900))
    pygame.display.set_caption('Snake AI')
    resetGame()

    runloop = True
    clock = pygame.time.Clock()
    
    dt = 0
    gameTime = 0

    snek.createPop(filename)

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
        if(snek.graph is not None):
            
            gameDisplay.blit(snek.graph, (0, 600))
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
    yOffset = showLabel(snakePlayer.calculateFitness(), 'Current Fitness ', xOffset, yOffset)

    yOffset = 520
    yOffset = showLabel(int(snek.genAvg), 'Current Gen Average: ', xOffset, yOffset)
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
        pygame.draw.circle(gameDisplay, drawColor, (xOffset + inputX, yOffset + (int)(i / len(inputs) * 550)), 11)

    #Draw hidden
    for i in range(len(hidden)):
        color = hidden[i]
        drawColor = ((int)(color * 255), (int)(color * 255), (int) (color * 255))
        #pygame.draw.circle(gameDisplay, pygame.Color('white'), (xOffset + 100, yOffset + (int)(i / len(inputs) * 550)), 20, 1)
        pygame.draw.circle(gameDisplay, drawColor, (xOffset + hiddenX, yOffset + (int)(i / len(hidden) * 550)), 11)
    
    #Draw hidden
    for i in range(len(hidden2)):
        color = hidden2[i]
        drawColor = ((int)(color * 255), (int)(color * 255), (int) (color * 255))
        #pygame.draw.circle(gameDisplay, pygame.Color('white'), (xOffset + 100, yOffset + (int)(i / len(inputs) * 550)), 20, 1)
        pygame.draw.circle(gameDisplay, drawColor, (xOffset + hidden2X, yOffset + (int)(i / len(hidden2) * 550)), 11)



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
    global player
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                snek.writeBest("BestOnClose.txt")
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
                if event.key == pygame.K_g:
                    player = False
            else:
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_SPACE:
                        #Manual Kill Current NNet
                        snek.setFitness(-1)
                        snek.moveToNextNnet()
                        resetGame()
                    if event.key == pygame.K_UP:
                        if(FPS < 55):
                            FPS += 5
                    if event.key == pygame.K_DOWN:
                        if(FPS > 5):
                            FPS -= 5
                    if event.key == pygame.K_w:
                        snek.writeBest("BestOnManual.txt")
                    if event.key == pygame.K_g:
                        player = True

                    
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

def getNeuralInput(snakePlayer):
    global grid
    global inputs
    inputs = [0] * 24
    head = snakePlayer.getHead()

    #L, UL, U, UR, R, DR, D, DL
    directions = [[-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1]]

    #8 total directions
    for i in range(8): 
        tempVec = lookInDir(head, directions[i][0], directions[i][1])
        inputs[i] = tempVec[0]
        inputs[i + 8] = tempVec[1]
        inputs[i + 16] = tempVec[2]

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

def lookInDir(head, xDir, yDir):
    wallDist = 0
    foodFound = 0
    tailDist = 0

    tailFound = False
    increment = np.sqrt(xDir * xDir + yDir * yDir)


    #move once in direction
    distance = increment
    x = head[0] + xDir
    y = head[1] + yDir

    normalize = increment * np.abs(xDir * WIDTH) + increment * np.abs(yDir * HEIGHT)
    #1 - (distance / normalize)

    while x >= 0 and x < WIDTH and y >= 0 and y < HEIGHT:
        if foodFound == 0 and grid[x][y] == 2:
            foodFound = 1

        if not tailFound and grid[x][y] == 1:
            tailFound = True
            tailDist = 1/distance

        x += xDir
        y += yDir
        distance += increment

    wallDist = 1/distance

    return (wallDist, tailDist, foodFound)