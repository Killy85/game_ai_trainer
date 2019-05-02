from trainer import train as train_33, Trainer as Trainer33
from trainer_3state import train as train_3, Trainer as Trainer3
from game_adapted import Game_adapted
import matplotlib.pyplot as plt
import numpy as np


game = Game_adapted()
trainer = Trainer33()

results33 = train_33(400, trainer, game)

game = Game_adapted()
trainer = Trainer3()

results3 = train_3(400, trainer, game)

score33 = np.array(results33)
score33_c = np.convolve(score33, np.full((10,), 1/10), mode="same")
score3 = np.array(results3)
score3_c = np.convolve(score3, np.full((10,), 1/10), mode="same")


plt.subplot(211)
plt.plot(score33_c)
plt.subplot(212)
plt.plot(score3_c)
plt.show()

