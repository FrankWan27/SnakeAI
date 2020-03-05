
shapes = {
    'I':[[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]],
    'J':[[2, 2, 0], [0, 2, 0], [0, 2 ,0]],
    'L':[[0, 3, 0], [0, 3, 0], [3, 3, 0]],
    'O':[[4, 4], [4, 4]],
    'S':[[0, 5, 0], [5, 5, 0], [5, 0, 0]],
    'T':[[0, 6, 0], [6, 6, 0], [0, 6, 0]],
    'Z':[[7, 0, 0], [7, 7, 0], [0, 7, 0]]
}

import copy 
class Shape:
	x = 0
	y = 0
	shape = []
	letter = ''
	rotation = 0

	def __init__(self, shapeLetter='S'):
		self.letter = shapeLetter
		self.shape = copy.deepcopy(shapes[shapeLetter])



