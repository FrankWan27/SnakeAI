import random
import snakeAI as SnakeAI
import sys

random.seed(0)

if len(sys.argv) > 1:
	SnakeAI.startGame(sys.argv[1])
else:
	SnakeAI.startGame()
