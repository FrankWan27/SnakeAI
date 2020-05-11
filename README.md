# Snake AI
Uses an evolutionary approach to teach an AI how to play the classic game of Snake
## Example
![Example Snake](https://github.com/FrankWan27/SnakeAI/blob/master/img/examplesnake.gif?raw=true)

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Controls](#controls)
- [Neural Network Structure](#neural-network-structure)
- [Genetic Algorithm](#genetic-algorithm)
- [Authors](#authors)

## Overview
### Game Rules
Following a standard set of snake rules:
1. The snake must always be moving in a direction (Up, Down, Left, Right)
2. The snake dies if it runs into a wall or its tail
3. The snake grows by 1 for each fruit eaten, and a new fruit spawns in an unoccupied location

## Installation

### Clone

- Clone this repo to your local machine using `git clone https://github.com/FrankWan27/SnakeAI.git`

### Dependencies
- [Python 3 ](https://www.python.org/downloads/)
- [Pygame](https://www.pygame.org/)  - used to render graphics
  ```pip install pygame```
- [Matplotlib](https://matplotlib.org/) - used to draw graph to keep track of AI progress
  ```pip install matplotlib```
- [Numpy](https://numpy.org/) - used for matrix manipulation in numpy.ndarray
  ```pip install numpy```
### Usage
To start running the snake AI, simply run in the parent directory
 ```python main.py```
 To continue running the snake AI from a saved neural network state, add the textfile as an argument
 ```python main.py Best-5-11.txt```

## Controls
The game can be played by the AI (AI Mode) or by a human (Human Mode). By default, the game starts in AI mode.
### AI Mode
- Up/Down Arrow Key - Increase/Decrease the snake's movement speed (FPS) by 5 (Max 60, Min 5, Default 60)
- Space - Kill the current snake, assign a fitness score of -1 (won't reproduce), 


## Neural Network Structure



## Authors

* **Frank Wan** - [Github](https://github.com/FrankWan27)
