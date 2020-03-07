from enum import Enum

shapes = {
    'I':[[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]],
    'J':[[2, 2, 0, 0], [0, 2, 0, 0], [0, 2 ,0, 0], [0, 0, 0, 0]],
    'L':[[0, 3, 0, 0], [0, 3, 0, 0], [3, 3, 0, 0], [0, 0, 0, 0]],
    'O':[[0, 0, 0, 0], [0, 4, 4, 0], [0, 4, 4, 0], [0, 0, 0, 0]],
    'S':[[0, 5, 0, 0], [5, 5, 0, 0], [5, 0, 0, 0], [0, 0, 0, 0]],
    'T':[[0, 6, 0, 0], [6, 6, 0, 0], [0, 6, 0, 0], [0, 0, 0, 0]],
    'Z':[[7, 0, 0, 0], [7, 7, 0, 0], [0, 7, 0, 0], [0, 0, 0, 0]],
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

class Dir(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)

#Stores input hidden and out nums
class Species(Enum):
	TETRIS = (223, 20, 8)
	SNAKE = (104, 20, 4)

#Converts a 2D Array to a 1D list
def arrayToList(arr, result):
    for x in range(len(arr)):
        for y in range(len(arr[0])):
            result.append(arr[x][y])
    return result

#Converts a 2D Array to a 1D list, and converts anything > 0 to 1
def arrayToOnes(arr, result):
    for x in range(len(arr)):
        for y in range(len(arr[0])):
            if arr[x][y] > 0:
                result.append(1)
            else:
                result.append(0)
    return result
