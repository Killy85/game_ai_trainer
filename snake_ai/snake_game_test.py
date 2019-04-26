from snake_game import Snake
import time
import random

snake = Snake(20, True)

debug = True

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

best_score = 0

while 1:
    time.sleep(0.5)

    if(debug):
        move = snake.do_move(0)
    else:
        move = snake.do_move(random.randint(0,4))

    if(move['reward'] < 0):
        snake.reset()

    elif(move['reward'] > best_score):
    	best_score = move['reward']