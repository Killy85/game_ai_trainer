from snake_ai.ple.games.snake import Snake
from snake_ai.ple import PLE
from snake_ai.agent import Trainer

game = Snake()
p = PLE(game, fps=30, display_screen=True)

agent = Trainer(allowed_actions=p.getActionSet())

p.init()
reward = 0.0
nb_frames = 100000

for i in range(nb_frames):
   if p.game_over():
           p.reset_game()

   observation = p.getGameState()
   action = agent.pickAction(reward, observation)
   reward = p.act(action)