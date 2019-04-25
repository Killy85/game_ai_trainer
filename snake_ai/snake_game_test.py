from snake_game import Snake
import time

snake = Snake(20, True)

while 1:
    time.sleep(0.5)
    move = snake.do_move(1)