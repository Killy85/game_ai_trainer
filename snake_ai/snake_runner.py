from snake_game import Snake
from agent import Trainer
import datetime
import time

flatten = lambda l: [item for sublist in l for item in sublist]

def get_state(grid_size, snake_location, state, alea=False):
    state = [snake_location[0], snake_location[1]]
    for key, value in enumerate(state_control):
        state.append(value)

    return state


nb_cases = 10
display = True

# Initialisation du jeu
snake = Snake(nb_cases, display)

grid_size = nb_cases + 2
agent = Trainer(allowed_actions=snake.get_actions_set(), name='SnakeV1', state_size=8)

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
        agent.save()

    if(reward < -1):
        snake.reset()

    iteration += 1

    observation = snake.get_observation()
    state_control = observation['state_control']
    snake_location = observation['snake_location']
    state = get_state(grid_size, snake_location, state_control)

    action = agent.pickAction(state, True)

    new_observation = snake.do_move(agent.getSelectedAction(action))
    reward = new_observation['reward']

    new_state_control = new_observation['state_control']
    new_snake_location = new_observation['snake_location']
    next_state = get_state(grid_size, new_snake_location, new_state_control)

    agent.train(state, action, reward, next_state, False)

print('Best Score : '+str(bestScore))
