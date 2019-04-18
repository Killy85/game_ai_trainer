import numpy as np
from keras.models import Sequential, load_model
from keras.layers.core import Dense, Activation
from keras.optimizers import Adam, sgd
import os

class Trainer:
    def __init__(self, allowed_actions, name=None, learning_rate=0.01, epsilon_decay=0.9999):
        self.action_size = len(allowed_actions)
        self.actions = allowed_actions
        self.gamma = 0.9
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate

        if name is not None and os.path.isfile("model-" + name):
            model = load_model("model-" + name)
        else:
            model = Sequential()
            model.add(Dense(24, input_shape=(self.state_size,), activation='relu'))
            model.add(Dense(24, activation="relu"))
            model.add(Dense(self.action_size, activation='linear'))
            model.compile(loss='mse', optimizer=sgd(lr=self.learning_rate))

        self.model = model

    def pickAction(self, reward, observation):

        return self.actions[0]