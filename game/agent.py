from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import random
import numpy as np
import pandas as pd
from operator import add


class BreakoutAgent(object):

    def __init__(self):
        """Initialize the value of the agent
        """

        self.reward = 0
        self.gamma = 0.9
        self.dataframe = pd.DataFrame()
        self.short_memory = np.array([])
        self.agent_target = 1
        self.agent_predict = 0
        self.learning_rate = 0.0005
        self.model = self.network()
        #self.model = self.network("weights.hdf5")
        self.epsilon = 0
        self.actual = []
        self.memory = []

    def get_state(self, game, player):
        """Return the state of the environnement

        Arguments:
            game {Game} -- Object describing all items in the game
            player {Player} -- Object describing the attributes of the player

        Returns:
            npArray -- This different boolean state of the player
        """

        state = [
            game.ball.x < (player.x - 1/2 *(player.width)), 
            #Ball is left
            game.ball.x > (player.x + 1/2 *(player.width)), 
            #Ball is right
            player.x - 1/2 *(player.width) < game.ball.x < player.x + 1/2 *(player.width),
            #Ball is up
        ]

        return np.asarray(state)

    def set_reward(self, ball, brick_destroyed):
        """Compute the reward for the last agent action

        Arguments:
            ball {Object} -- Object describing if the ball is lost or has bounced
            brick_destroyed {Array} -- Id of bricks that has been destroyed since last call

        Returns:
            integer -- The reward for the last agent action
        """

        self.reward = 0
        if ball.loosed:
            self.reward = -100
            return self.reward
        if ball.bounce:
            self.reward += 5
        #if brick_destroyed:
        #    self.reward += 1 * len(brick_destroyed)
        # This is a possible devellopement for the training
        return self.reward

    def network(self, weights=None):
        """Create a models based on a neural network

        Keyword Arguments:
            weights  -- Weight to load on the model(default: {None})

        Returns:
            Sequential -- the model we will use during our game
        """

        model = Sequential()
        model.add(Dense(output_dim=120, activation='relu', input_dim=11))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=3, activation='softmax'))
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)

        if weights:
            model.load_weights(weights)
        return model

    def remember(self, state, action, reward, next_state, done):
        """Store into the agent last part of the learning

        Arguments:
            state {Array} -- [description]
            action {Integer} -- [description]
            reward {Integer} -- [description]
            next_state {Array} -- [description]
            done {function} -- [description]
        """

        self.memory.append((state, action, reward, next_state, done))

    def replay_new(self, memory):
        """[summary]

        Arguments:
            memory {[type]} -- [description]
        """

        if len(memory) > 1000:
            minibatch = random.sample(memory, 1000)
        else:
            minibatch = memory
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(
                    self.model.predict(np.array([next_state]))[0])
            target_f = self.model.predict(np.array([state]))
            target_f[0][np.argmax(action)] = target
            self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

    def train_short_memory(self, state, action, reward, next_state, done):
        """[summary]

        Arguments:
            state {[type]} -- [description]
            action {[type]} -- [description]
            reward {[type]} -- [description]
            next_state {[type]} -- [description]
            done {function} -- [description]
        """

        target = reward
        if not done:
            target = reward + self.gamma * np.amax(
                self.model.predict(next_state.reshape((1, 11)))[0])
        target_f = self.model.predict(state.reshape((1, 11)))
        target_f[0][np.argmax(action)] = target
        self.model.fit(state.reshape((1, 11)),
                target_f, epochs=1, verbose=0)