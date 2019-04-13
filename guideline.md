# Game AI trainer

## Overview
This document will explain the way we will proceed while creating our AI trainer.

To do this, we will have to use the following techniques:
- Reinforcement Learning
- Deep-Q Learning

At this point we are juste studying how any of this work, but there is some [examples](https://towardsdatascience.com/how-to-teach-an-ai-to-play-games-deep-reinforcement-learning-28f9b920440a) out there of how to do it.

We so will have to choose how we will weigth the reward system in order to create the best Q-table possible.

As for the snake game in the example, our agent will have 2 possible moves:
- Go to the left
- Go to the right
- Go front

Using this, we will have to determine a reward system, in order to incent the agent to do what we want him to do: Get the best score possible!

## Statistics

We will also have to generate and store data of how our agent has behaved during the training sessions.

It may help us to correlate training parameters with success of thoses training session and to weight each parameters influence on the whole process.

## BreakOut-Like Game

The game we want to use is based on the breakout game. Published in 1978, by Atari, it's the first game of this kind.

### Explanation

In this game, the user is represented by a bar which can move horizontally. The goal is to destroy all the bricks on the level using a little ball, we will have to make bounce against the player's bar.

Taking the Q-learning approach, it means that our player will always have 3 possible actions:
- Going left
- Staying still
- Going right

Each of this actions have to be determined by the passed action of the agent.

In the case of a Q-learning algorithm, we will have to determine a matrix will all the possible state of our environnement.



### Reward system

We can for example give it a positive reward when it gets under the ball to make it bounce back or a brick is destroyed. On the other hand, we may gave it a negative reward when it let the ball get out.
