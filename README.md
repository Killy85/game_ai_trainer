# game_ai_trainer
This repository is home of a Machine Learning project aiming at training an agent to play a game using Reinforcement learning

## Retro-Planning

### 11/04/2019

2 personnes pour :

Créer un jeu simple (casse-brick) qui communique avec un script python. (Kevin and Matthieu)

2 personnes pour :

Etudier un cas existant d'apprentissage par renforcement (Nicolas and Benjamin)


### 19/04/2019

POC

And ... we didn't push it further! I mean the planning !

Then it was about updating the model to fit our game.

## Breakout game

So, for the breakout-game, we had two different representations :

The first one was an array of three boolean which help giving the ball position.
The results with this were quite mediocre and we agreed on a change. 

So we decided to do as in the article we were starting from. We send the whole screen shot of the game to our network. Maybe not exactly the screenshot, but a reduced version of it.
By doing so, we may have a lot of the informations a real player has.

That's what you can find in the `game` folder.

We adapted a game to our convienence and used it to train on it. the `q_learning` script mais train and test 2 differents games: our breakout adn the gym[atari] breakout

To launch the script, here is a little guide:

`python q_learning.py [game] [action] (--model path_to_the_model_to_restore)`

game : Required. The game you want to launch. It have twos valid values for the moment : `atari`, `homemade`

action : Required. What we want to do with the game. Also twos valid values : `train` and `test`

path_to_the_model_to_restore : Required for testing, optional for training. Path to the model we want to restore in our network

## What about the snake?

Well, the snake game was the first example we found on the net of a working q-learning algorithm. 

It was kind of a side quest for us. Turns out to be more difficult than accounted for but here we are.

You will find more detailled informations on how to use it in [this document](snake_ai/README.md)