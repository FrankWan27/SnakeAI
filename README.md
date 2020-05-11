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
- [Training Example](#training-example)
- [Afterthoughts](#afterthoughts)
- [Authors](#authors)

## Overview

### Game Rules

Following a standard set of snake rules:
1. The snake must always be moving in a direction (Up, Down, Left, Right)
2. The snake dies if it runs into a wall or its tail
3. The snake grows by 1 for each fruit eaten, and a new fruit spawns in an unoccupied location
4. 
### Program Description

The program window is divided into three sections. The top left section shows the current game window, which includes the current game world, snake, and fruit information. The top right section shows the current snake's neural network. The bottom section shows a graph which contains the highest and average score history of all the previous generations.

![Overview](https://github.com/FrankWan27/SnakeAI/blob/master/img/overview.png?raw=true)

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
The game can be played by the AI (AI Mode) or by a human (Human Mode). By default, the game starts in AI mode. Upon closing the game by clicking the X button, the best performing snake's neural network will be written to the file "BestOnClose.txt"

### AI Mode

- Up/Down Arrow Key - Increase/Decrease the snake's movement speed (FPS) by 5 (Max 60, Min 5, Default 60)
- Space - Immediately kill the current snake and assign a fitness score of -1 (won't reproduce)
- W - Write best performing snake's neural network to the file "BestOnManual.txt"
- G - Switch to Human Mode

### Human Mode

- Up/Down/Left/Right Arrow Key - Change snake's direction to be up/down/left/right
- G - Switch to AI Mode

## Neural Network Structure

This neural network is 24x20x12x4, with one input layer, two hidden layers, and one output layer. Each input and output neuron can have a value between 0 and 1, and each weight can have a value between -1 and 1.

The neural network visualizer draws colors each neuron between black (no activation) and white (high activation). The weights are colored between red (inhibiting connection) and green (positive connection).

![Neural Net](https://github.com/FrankWan27/SnakeAI/blob/master/img/nnet.png?raw=true)


### Inputs
The snake can see in 8 directions, starting from the left, and every 45 degrees rotated clockwise. For each vision direction, it can calculate the distance from the wall, its tail, and the fruit. 
-  The distance from the wall and its tail is represented by $\frac{1}{distance}$. This makes the input much stronger when the snake is one tile away from the wall or its tail (immediate danger of dying), compared to when the snake is two or more tiles away. 
- The distance from fruits is represented by a 0 or 1. As long as the snake sees fruit in the vision direction, the input is given as a 1. I chose this because I wanted the motivation to go towards a fruit to be equally strong when the fruit is far away from the snake or when the fruit is close. 
![Neural Input](https://github.com/FrankWan27/SnakeAI/blob/master/img/inputs.png?raw=true)

### Hidden Layers

The hidden layers are activated by the ReLU activation function. 

### Output

The output layer contains the four moves the snake can make (Left, Right, Up, Down) and uses the sigmoid activation function to obtain a probability. The snake performs the move that has the highest calculated probability. 

## Genetic Algorithm

The snakes learn through a genetic algorithm that simulates the process of evolution. We start with a population of 50 snakes with randomized genes (weights). The snakes that perform the best are allowed to reproduce, which populates the next population through breeding and mutation. This process repeats until we are satisfied with state of the best snake and exit the program. 

### Selection

Of the population of 50 snakes, we select the top 10 performers to be the parents based on their fitness score. I found [Chrispresso](https://www.youtube.com/channel/UCFnNAjMoIgeTAj7N_zXC7uQ)'s method of evaluating fitness to be most effective: $$fitness = steps + (2^{fruit}+fruit^{2.1}*500)-[fruit^{1.2}*(0.25*steps)^{1.3}]$$ This equation attempts to reward early survival, eating fruit, and penalize wasted steps. We will allow the top performing snakes to continue onto the next generation. The remaining 40 snakes in the next population will be comprised of children of these top 10 performers. 

### Reproduction

For each of the 40 child snakes, we randomly select 2 parents from the pool of best performers weighted by their fitness score using the [Roulette Wheel Method](https://en.wikipedia.org/wiki/Fitness_proportionate_selection). Then we randomly copy the genes from either the mother or father snake with equal probability to the child snake. 

### Mutation

To ensure our population will continue to evolve, we will randomly mutate all 40 of the child snakes' genes. With a mutation rate of 5%, each mutated gene will be reset to a uniformly random value between -1 and 1. These 40 mutated child snakes and the 10 surviving snakes from the last generation will form the next population and repeat the entire process. 

## Training Example 
![training](https://github.com/FrankWan27/SnakeAI/blob/master/img/training.gif?raw=true)


## Afterthoughts

After finishing the project, I thought of a few improvements I could have made:
- Randomize the starting location of the snake
	- Because my grid size is 20x20, there is no center tile. Thus, the snakes are biased to move in the direction that has the most tiles before hitting the wall. (In our case, up and left).
	- We could randomize the starting location of each snake to be any of the four center tiles which would remove this bias.
- Have a color gene
	- I think it would be cool to see which parents each child snake has. An easy way to identify the parents of each child is to have a color gene that is also passed down through crossover.
- Have all snakes in the population run simultaneously 
	- One of the biggest limitations of this project is that I couldn't increase the population size to a large number such as 1000+, since each snake runs one at a time. If all snakes ran at the same time, we could greatly speed up the learning process and increase the population size.
- Save the random seed for each snake
	- If we save the random seed used to generate the food spawn locations, we could reproduce the exact path a specific snake took. This way, we can replay the lives of high scoring snakes.

Also, this project was originally intended to be a Tetris AI, but I got side tracked and made a Snake AI first.(I will continue the tetris project at a later date - stay tuned!


## Authors

* **Frank Wan** - [Github](https://github.com/FrankWan27)# Snake AI
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
