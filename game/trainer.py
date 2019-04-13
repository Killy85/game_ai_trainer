import numpy as np
from keras.models import Sequential, load_model
from keras.layers.core import Dense, Activation
from keras.optimizers import Adam, sgd
import random
import time
import os

STATES = {
        1: (0, 0),
        2: (0, 1),
        3: (0, 2),
        4: (1, 0),
        5: (1, 1),
        6: (1, 2),
        7: (2, 0),
        8: (2, 1),
        9: (2, 2),
        10: (3, 0),
        11: (3, 1),
        12: (3, 2),
        13: (4, 0),
        14: (4, 1),
        15: (4, 2),
        16: (5, 0),
        17: (5, 1),
        18: (5, 2),
        19: (6, 0),
        20: (6, 1),
        21: (6, 2),
        22: (7, 0),
        23: (7, 1),
        24: (7, 2),
        25: (8, 0),
        26: (8, 1),
        27: (8, 2),
        28: (9, 0),
        29: (9, 1),
        30: (9, 2),
        31: (10, 0),
        32: (10, 1),
        33: (10, 2)
    }

class Trainer:
    def __init__(self, name=None, learning_rate=0.01, epsilon_decay=0.9999):
        column_number = 11
        self.state_size = 3 * column_number
        self.action_size = 3
        self.gamma = 0.9
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate

        self.name = name

        if name is not None and os.path.isfile("model-" + name):
            model = load_model("model-" + name)
        else:
            model = Sequential()
            model.add(Dense(24, input_shape=(self.state_size,), activation='relu'))
            model.add(Dense(24, activation="relu"))
            model.add(Dense(self.action_size, activation='linear'))
            model.compile(loss='mse', optimizer=sgd(lr=self.learning_rate))

        self.model = model       

    def get_best_action(self, state, rand=True):

        self.epsilon *= self.epsilon_decay

        if rand and np.random.rand() <= self.epsilon:
            # The agent acts randomly
            return random.randrange(self.action_size)

        # Predict the reward value based on the given state
        act_values = self.model.predict(np.array([state]))

        # Pick the action based on the predicted reward
        action =  np.argmax(act_values[0])  
        return action

    def train(self, state, action, reward, next_state, done):
        target = self.model.predict(np.array([state]))[0]
        if done:
            target[action] = reward
        else:
            target[action] = reward + self.gamma * np.max(
                self.model.predict(np.array([next_state])))

        inputs = np.array([state])
        outputs = np.array([target])

        return self.model.fit(inputs, outputs, epochs=1, verbose=0, batch_size=1)

    def save(self):
        if self.name:
            self.model.save("model-" + self.name, overwrite=True)
        else:
            self.model.save("model-" + str(time.time()))


def train(episodes, trainer, game):
    scores = []
    losses = [0]
    for e in range(episodes):
        state = game.reset()
        
        score = 0  # score in current game
        done = False
        steps = 0  # steps in current game
        while not done:
            steps += 1
            action = trainer.get_best_action(state)
            next_state, reward, done, _ = game.move(action)
            score += reward
            trainer.train(state, action, reward, next_state, done)
            #print(state.index(1), Game.ACTION_NAMES[action], reward, 
            # next_state.index(1), "DONE" if done else "")
            state = next_state
            if done:
                scores.append(score)
                break
            if steps > 200:
                trainer.train(state, action, -10, state, True) # we end the game
                scores.append(score)
                break
        if e % 100 == 0: # print log every 100 episode
            print(f"episode: {e}/{episodes}, moves: {steps}, score: {score}")
            print(f"epsilon : {trainer.epsilon}")
    #trainer.save()
    return scores

