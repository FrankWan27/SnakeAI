import tetris as Tetris
import copy 
class Shape:
	x = 0
	y = 0
	shape = []
	letter = ''

	def __init__(self, shapeLetter='S'):
		self.letter = shapeLetter
		self.shape = copy.deepcopy(Tetris.shapes[shapeLetter])



