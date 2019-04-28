from snake_game import Snake
from agent import Trainer
import datetime
import time

flatten = lambda l: [item for sublist in l for item in sublist]

def get_state(grid_size, snake_location, food_location, alea=False):
    return flatten(get_grille(grid_size, snake_location, food_location))

def get_grille(grid_size, snake_location, food_location):
    s_x, s_y = snake_location
    f_x, f_x = food_location
    grille = [
        [0] * int(grid_size) for i in range(int(grid_size))
    ]
    grille[s_x][s_y] += 1
    grille[f_x][f_x] += 1
    return grille

nb_cases = 20
display = True

# Initialisation du jeu
snake = Snake(nb_cases, display)

grid_size = nb_cases + 2
agent = Trainer(allowed_actions=snake.get_actions_set(), height=grid_size, width=grid_size)

reward = 0
bestScore = 0
iteration = 0

while 1:
    # Définition de l'action à 30 Action Par secondes
    time.sleep(0.033)
    score = int(snake.get_score())

    if(score > bestScore):
        bestScore = score
        print('New Best Score : '+str(bestScore) + ' a ' + str(datetime.datetime.now()))

    if(reward < -1):
        snake.reset()

    iteration += 1

    observation = snake.get_observation()
    food_location = observation['food_location']
    snake_location = observation['snake_location']
    state = get_state(grid_size, snake_location, food_location)

    action = agent.pickAction(state, True)

    new_observation = snake.do_move(agent.getSelectedAction(action))
    reward = new_observation['reward']

    new_food_location = new_observation['food_location']
    new_snake_location = new_observation['snake_location']
    next_state = get_state(grid_size, new_snake_location, new_food_location)

    agent.train(state, action, reward, next_state, False)

print('Best Score : '+str(bestScore))
