import pygame
import random
from defs import *

class Wall():

    width = 50
    height = 200
    speed = 1
    color = pygame.Color('red')

    def __init__(self, gameDisplay, x, y):
        self.gameDisplay = gameDisplay
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.visible = True


    def move(self, dx, dy):
        self.rect.centerx += dx
        self.rect.centery += dy

    def draw(self):
        pygame.draw.rect(self.gameDisplay, self.color, self.rect)

    def update(self, dt):
        self.move(-(self.speed * dt), 0)
        self.draw()
        
        if(self.rect.centerx < 0):
            self.visible = False

class Walls():

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.walls = []


    def addWall(self, x):

        y = random.randint(0, 800)

        self.walls.append(Wall(self.gameDisplay, x, y))

    def update(self, dt):

        for wall in self.walls:
            wall.update(dt)

        self.walls = [wall for wall in self.walls if wall.visible]


        if len(self.walls) == 0:
            self.addWall(DISPLAY_W)






