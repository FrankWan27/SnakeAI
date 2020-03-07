from defs import *

class Snake:

    body = []
    direction = Dir.RIGHT
    length = 1
    lifetime = 0

    def __init__(self, xPos=0, yPos=0, direction=Dir.RIGHT):
        self.body = []
        self.lifetime = 0
        self.body.append((xPos, yPos))
        self.direction = direction

    def moveBody(self):

        head = self.getHead()
        #remove Tail
        self.body.pop(0)


        #add Head
        head = self.move(head, self.direction)

        if self.checkCollision(head):
            return False
        else:
            self.lifetime += 1
            self.body.append(head)
            return True

    def getHead(self):
        return self.body[self.getLength() - 1]


    def move(self, head, direction):
        return tuple(map(sum, zip(head, direction.value)))
    
    def checkCollision(self, head):

        #hard coded boundaries
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True

        for bodyPart in self.body:
            if head[0] == bodyPart[0] and head[1] == bodyPart[1]:
                return True

        return False

    def getLength(self):
        return len(self.body)
