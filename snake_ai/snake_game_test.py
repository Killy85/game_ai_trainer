from snake_game import Snake
import time
import random

snake = Snake(20, True)

debug = False

best_score = 0

while 1:
    time.sleep(0.03)

    if(debug):
        move = snake.do_move(0)
    else:
        move = snake.do_move(random.randint(0,4))
        print(move)

    if(move['reward'] < 0):
        snake.reset()


    elif(snake.get_score() > best_score):
    	best_score = snake.get_score() 