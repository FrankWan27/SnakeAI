#import necessary libraries
#pip install pygame
import pygame
import numpy as np
import scipy
import random


random.seed(a = 'Suisei')

#setup global vars
gameDisplay = ''
grid = np.zeros((20, 10))

#official shape and orientation
#https://tetris.wiki/Super_Rotation_System
shapes = {
    'I':[[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
    'J':[[2, 0, 0], [2, 2, 2], [0, 0 ,0]],
    'L':[[0, 0, 3], [3, 3, 3], [0, 0, 0]],
    'O':[[4, 4], [4, 4]],
    'S':[[0, 5, 5], [5, 5, 0], [0, 0, 0]],
    'T':[[0, 6, 0], [6, 6, 6], [0, 0, 0]],
    'Z':[[7, 7, 0], [0, 7, 7], [0, 0, 0]]
}

colors = {
    'I':'cyan',
    'J':'blue',
    'L':'orange',
    'O':'yellow',
    'S':'green',
    'T':'purple',
    'Z':'red'
}

hold = ''
upcoming = []



score = 0

def generateUpcoming():
    tempArr = []
    for i in range(5):
        tempArr.append(random.choice(list(shapes.keys())))
    return tempArr

def resetGame():
    global grid
    global hold
    global upcoming

    grid = np.zeros((20, 10))
    hold = ''
    upcoming = generateUpcoming()

def showLabel(data, text, x, y):
    font = pygame.font.SysFont("monospace", 20)
    label = font.render('{} {}'.format(text, data), 1, (40,40,250))
    gameDisplay.blit(label, (x, y))

def showFPS(dt, gameTime):
    showLabel(round(1000/dt, 2), 'FPS: ', 10, 10, )
    showLabel(round(gameTime/1000, 2),'Game Time: ', 10, 30)

def showNext():
    print('s')
    

def initGame():
    global gameDisplay
    pygame.init()
    gameDisplay = pygame.display.set_mode((600, 800))
    pygame.display.set_caption('Tetris AI')
    bg = pygame.image.load('img/BG.png')
    resetGame()

    print(upcoming)
    
    runloop = True
    clock = pygame.time.Clock()
    
    dt = 0
    gameTime = 0
    
    while runloop:
        
        dt = clock.tick(60)
        gameTime += dt
        
        gameDisplay.blit(bg, (0, 0))
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runLoop = False
                pygame.display.quit()
                pygame.quit()
                
            elif event.type == pygame.KEYDOWN:
                print('keypress')
                
        showFPS(dt, gameTime)
        showNext()
        pygame.display.update()

   
initGame()
