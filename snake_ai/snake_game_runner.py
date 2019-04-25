from snake_game import Snake
from agent import Trainer
import datetime

flatten = lambda l: [item for sublist in l for item in sublist]

def get_state(game, snake_location, food_location, alea=False):
    x, y = snake_location
    if alea:
        return [get_grille(game, x, y) for (x, y) in
                [snake_location, food_location]]
    return flatten(get_grille(game, x, y))

def get_grille(game, x, y):
    grille = [
        [0] * int(game.width/10) for i in range(int(game.height/10))
    ]
    grille[x][y] = 1
    return grille


# NE PAS CHANGER CETTE VARIABLE
case_size = 20
size = 10

# Initialisation du jeu
game = Snake(height=case_size*size,width=case_size*size)

agent = Trainer(allowed_actions=p.getActionSet(), height=game.height, width=game.width)

p.init()
reward = 0.0
nb_steps = 10000000000000000
bestScore = 0

for i in range(nb_frames):

    if(p.score() > bestScore):
        bestScore = int(p.score())
        print('New Best Score : '+str(bestScore) + ' a ' + str(datetime.datetime.now()))

    if p.game_over():
        p.reset_game()

    observation = p.getGameState()
    food_location = [int(observation.get('food_x')/10), int(observation.get('food_y')/10)]
    snake_location = [int(observation.get('snake_head_x')/10), int(observation.get('snake_head_y')/10)]
    state = get_state(game, snake_location, food_location)
    action = agent.pickAction(state, True)
    reward = p.act(agent.getSelectedAction(action))

    # Fixing Reward by punishing more the player when he is not doing the right thing.
    if(reward == -1): # If he loose (By touching himself or the border)
        reward = -100
    elif(reward == 1): # If he get the food
        reward = 200
    
    observation = p.getGameState()
    food_location = [int(observation.get('food_x')/10), int(observation.get('food_y')/10)]
    snake_location = [int(observation.get('snake_head_x')/10), int(observation.get('snake_head_y')/10)]
    next_state = get_state(game, snake_location, food_location)

    agent.train(state, action, reward, next_state, False)

print('Best Score : '+str(bestScore))
