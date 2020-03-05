#import necessary libraries
#pip install pygame
import pygame
import numpy as np
import random
from shape import Shape
#setup global vars
gameDisplay = ''
grid = np.zeros((10, 20))

#official shape and orientation
#https://tetris.wiki/Super_Rotation_System
#changed to be row based
shapes = {
    'I':[[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]],
    'J':[[2, 2, 0], [0, 2, 0], [0, 2 ,0]],
    'L':[[0, 3, 0], [0, 3, 0], [3, 3, 0]],
    'O':[[4, 4], [4, 4]],
    'S':[[0, 5, 0], [5, 5, 0], [5, 0, 0]],
    'T':[[0, 6, 0], [6, 6, 0], [0, 6, 0]],
    'Z':[[7, 0, 0], [7, 7, 0], [0, 7, 0]]
}

colors = {
    1:'cyan',
    'I':'cyan',
    2:'blue',
    'J':'blue',
    3:'orange',
    'L':'orange',
    4:'yellow',
    'O':'yellow',
    5:'green',
    'S':'green',
    6:'purple',
    'T':'purple',
    7:'red',
    'Z':'red'
}

speeds = [500, 100, 1, 0]
speedSetting = speeds[0]
hold = ''
currentShape = Shape()
upcoming = []

score = 0

#Core game loop
def startGame():
    global gameDisplay
    pygame.init()
    gameDisplay = pygame.display.set_mode((600, 800))
    pygame.display.set_caption('Tetris AI')
    bg = pygame.image.load('img/BG.png')
    resetGame()

    currentShape = getNextShape()
    addShape()

    runloop = True
    clock = pygame.time.Clock()
    
    dt = 0
    gameTime = 0
    ticker = 0
    
    while runloop:        
        #Break loop if we quit
        runLoop = handleInput()

        dt = clock.tick(60)
        gameTime += dt
        ticker += dt
        if(ticker >= speedSetting):
            moveDown()
            ticker = 0

        #Draw everything to screen
        gameDisplay.blit(bg, (0, 0))
        showFPS(dt, gameTime)
        showScore()
        showNext()
        showGrid()
        
        pygame.display.update()



def resetGame():
    global grid
    global hold
    global upcoming
    global score

    grid = np.zeros((10, 20))
    hold = ''
    upcoming = generateUpcoming()
    score = 0

def showLabel(data, text, x, y):
    font = pygame.font.SysFont("monospace", 20)
    label = font.render('{} {}'.format(text, data), 1, (40,40,250))
    gameDisplay.blit(label, (x, y))

def showFPS(dt, gameTime):
    showLabel(round(1000/dt, 2), 'FPS: ', 10, 10, )
    showLabel(round(gameTime/1000, 2),'Game Time: ', 10, 30)

def showScore():
    font = pygame.font.SysFont("Sans Serif", 80)
    label = font.render('{}'.format(score), 1, (0, 0, 0))
    offset = font.size('{}'.format(score))
    gameDisplay.blit(label, (390 - offset[0], 732))

def showGrid():
    xOffset = 150
    yOffset = 99
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if(grid[x][y] != 0):
                pygame.draw.rect(gameDisplay, pygame.Color('white'), (xOffset + x * 30, yOffset + y * 30, 30, 30))
                pygame.draw.rect(gameDisplay, pygame.Color(colors[grid[x][y]]), (1 + xOffset + x * 30, 1 + yOffset + y * 30, 28, 28))


def showNext():
    nextShape = createShape(upcoming[0])
    #pygame.draw.rect(gameDisplay, pygame.Color('red'), nextShape[0])
    
def createShape(shape):
    rectList = []
    if(shape == 'S'):
        rectList.append(pygame.Rect(30, 0, 31, 31))
        rectList.append(pygame.Rect(0, 0, 31, 31))
        rectList.append(pygame.Rect(0, 0, 31, 31))
        rectList.append(pygame.Rect(0, 0, 31, 31))

    return rectList

#Handle keyboard input
def handleInput():
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moveLeft()
                if event.key == pygame.K_RIGHT:
                    moveRight()
                if event.key == pygame.K_DOWN:
                    moveDown()
                if event.key == pygame.K_UP:
                    fastDrop()
                

#Adds currentShape to the grid
def addShape():
    for x in range(len(currentShape.shape)):
        for y in range(len(currentShape.shape[0])):
            if currentShape.shape[x][y] != 0:
                grid[currentShape.x + x][currentShape.y + y] = currentShape.shape[x][y];

#Removes currentShape from the grid
def removeShape():
    for x in range(len(currentShape.shape)):
        for y in range(len(currentShape.shape[0])):
            if currentShape.shape[x][y] != 0:
                grid[currentShape.x + x][currentShape.y + y] = 0;


#Move currentShape left 1 tile
def moveLeft():
    removeShape()
    currentShape.x -= 1
    if checkCollision(currentShape):
        currentShape.x += 1
    addShape()

#Move currentShape right 1 tile
def moveRight():
    removeShape()
    currentShape.x += 1
    if checkCollision(currentShape):
        currentShape.x -= 1
    addShape()

#Move currentShape right 1 tile
def moveDown():
    global currentShape
    global score
    removeShape()
    currentShape.y += 1
    if checkCollision(currentShape):
        currentShape.y -= 1
        addShape()
        clearRows()
        currentShape = getNextShape()
        #check if we lost
        if checkCollision(currentShape):
            print('U Lost')
            resetGame()

    score += 1
    addShape()

#Move currentShape to the bottom
def fastDrop():
    global currentShape
    global score
    removeShape()
    while not checkCollision(currentShape):
        currentShape.y += 1
        score += 2

    
    currentShape.y -= 1
    score -= 2
    addShape()
    clearRows()
    currentShape = getNextShape()
    #check if we lost
    if checkCollision(currentShape):
        print('U Lost')
        resetGame()

    addShape()

#Checks if currentShape collides with boundary or other blocks
def checkCollision(currentShape):
    for x in range(len(currentShape.shape)):
        for y in range(len(currentShape.shape[0])):
            if currentShape.shape[x][y] != 0:
                #check bounds
                if currentShape.x + x < 0 or currentShape.y + y < 0 or currentShape.x + x >= len(grid) or currentShape.y + y >= len(grid[0]):
                    return True
                if grid[currentShape.x + x][currentShape.y + y] != 0:
                    return True

#Returns next upcoming shape
def getNextShape():
    tempShape = Shape(upcoming[0])
    upcoming[0] = upcoming[1]
    upcoming[1] = upcoming[2]
    upcoming[2] = upcoming[3]
    upcoming[3] = randomShape()

    #move shape to center of grid
    tempShape.x = (int)(len(grid) / 2 - len(tempShape.shape) / 2)
    return tempShape

#Pick a random shape
def randomShape():
    return random.choice(list(shapes.keys()))

#Generate 4 upcoming blocks
def generateUpcoming():
    tempArr = []
    for i in range(4):
        tempArr.append(randomShape())
    return tempArr

#Clear rows that are matched
def clearRows():
    global grid
    global score
    #List of rows that are full
    rows = []
    for y in reversed(range(len(grid[0]))):
        full = True
        for x in range(len(grid)):
            if grid[x][y] == 0:
                full = False
        if full:
            rows.append(y)

    #https://tetris.wiki/Scoring
    #TODO: implement T-spin and back to back difficult and combo

    multiplier = 0
    #Single
    if len(rows) == 1:
        multiplier = 100
    #Double
    elif len(rows) == 2:
        multiplier = 200
    #Triple
    elif len(rows) == 3:
        multiplier = 500
    #Tetris
    elif len(rows) == 4:
        multiplier = 800

    score += multiplier

    #delete rows to clear
    for row in rows:
        np.delete(grid, row, 1)

    #add missing rows 
    tempRows = np.zeros((10, len(rows)))
    grid = np.hstack((tempRows, grid))






