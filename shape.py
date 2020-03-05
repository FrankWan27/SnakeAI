import tetris as Tetris

class Shape:
	x = 0
	y = 0
	shape = []
	letter = ''

	def __init__(self, shapeLetter='S'):
		self.letter = shapeLetter
		self.shape = Tetris.shapes[shapeLetter]


