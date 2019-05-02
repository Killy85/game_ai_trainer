# -*- coding: utf-8 -*-
import os.path
import time
import random
import argparse
from collections import deque
from datetime import datetime
from game_adapted import Game_adapted

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from keras import layers
from skimage.color import rgb2gray
from skimage.transform import resize
from keras.models import Model
import gym
from keras.optimizers import RMSprop
from keras import backend as K
from keras.models import load_model
from keras.models import clone_model
from keras.callbacks import TensorBoard

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_integer('num_episode', 40000,
                            """number of epochs of the optimization loop.""")
# tf.app.flags.DEFINE_integer('observe_step_num', 5000,
tf.app.flags.DEFINE_integer('observe_step_num', 10000,
                            """Timesteps to observe before training.""")
# tf.app.flags.DEFINE_integer('epsilon_step_num', 50000,
tf.app.flags.DEFINE_integer('epsilon_step_num', 1000000,
                            """frames over which to anneal epsilon.""")
tf.app.flags.DEFINE_integer('refresh_target_model_num', 10000,  # update the target Q model every refresh_target_model_num
                            """frames over which to anneal epsilon.""")
tf.app.flags.DEFINE_integer('replay_memory', 22000, 
                            """number of previous transitions to remember.""")
tf.app.flags.DEFINE_integer('no_op_steps', 30,
                            """Number of the steps that runs before script begin.""")
tf.app.flags.DEFINE_float('regularizer_scale', 0.01,
                          """L1 regularizer scale.""")
tf.app.flags.DEFINE_integer('batch_size', 32,
                            """Size of minibatch to train.""")
tf.app.flags.DEFINE_float('learning_rate', 0.00025,
                          """Number of batches to run.""")
tf.app.flags.DEFINE_float('init_epsilon', 1.0,
                          """starting value of epsilon.""")
tf.app.flags.DEFINE_float('final_epsilon', 0.1,
                          """final value of epsilon.""")
tf.app.flags.DEFINE_float('gamma', 0.99,
                          """decay rate of past observations.""")
tf.app.flags.DEFINE_boolean('render', False,
                            """Whether to display the game.""")

ATARI_SHAPE = (84, 84, 4)  # input image size to model
ACTION_SIZE = 3
ENV_CHOSEN = None


def pre_processing(observe):
    """Pre-processing the input image to reduce dimensionnality.
       The input image is reduced to a 84 by 84 pixels image
       and from RGB to B&W in order to remove dimensions
    
    Arguments:
        observe {Image} -- Screen capture of the game
    
    Returns:
        Image -- Processed image
    """
    processed_observe = np.uint8(
        resize(rgb2gray(observe), (84, 84), mode='constant') * 255)
    return processed_observe


def huber_loss(y, q_value):
    """This function rpocess the huber loss for the input data.
    The huber loss have the advantage to be less sensitive to
    absurd data points

    
    Returns:
        float -- The huber loss for this Q_value
    """
    error = K.abs(y - q_value)
    quadratic_part = K.clip(error, 0.0, 1.0)
    linear_part = error - quadratic_part
    loss = K.mean(0.5 * K.square(quadratic_part) + linear_part)
    return loss


def breakout_model():
    """Define the a convolutionnal model we will be using during the learning process. 
    This is created of differents layers.
    
    Returns:
        tf.model -- the model we will be feeding data
    """

    # Here we define the inputs layers
    frames_input = layers.Input(ATARI_SHAPE, name='frames')
    actions_input = layers.Input((ACTION_SIZE,), name='action_mask')

    # Normalizing from [0,255] to [0,1]
    normalized = layers.Lambda(lambda x: x / 255.0, name='normalization')(frames_input)

    # "The first hidden layer convolves 16 8×8 filters with stride 4 with the input image and applies a rectifier nonlinearity."
    conv_1 = layers.convolutional.Conv2D(
        16, (8, 8), strides=(4, 4), activation='relu'
    )(normalized)
    # "The second hidden layer convolves 32 4×4 filters with stride 2, again followed by a rectifier nonlinearity."
    conv_2 = layers.convolutional.Conv2D(
        32, (4, 4), strides=(2, 2), activation='relu'
    )(conv_1)
    # Flattening the second convolutional layer.
    conv_flattened = layers.core.Flatten()(conv_2)
    # "The final hidden layer is fully-connected and consists of 256 rectifier units."
    hidden = layers.Dense(256, activation='relu')(conv_flattened)
    # "The output layer is a fully-connected linear layer with a single output for each valid action."
    output = layers.Dense(ACTION_SIZE)(hidden)
    # Finally, we multiply the output by the mask!
    filtered_output = layers.Multiply(name='QValue')([output, actions_input])

    model = Model(inputs=[frames_input, actions_input], outputs=filtered_output)
    model.summary()
    optimizer = RMSprop(lr=FLAGS.learning_rate, rho=0.95, epsilon=0.01)

    model.compile(optimizer, loss=huber_loss)
    return model


def get_action(history, epsilon, step, model):
    """Get the action to  do from the model
    
    Arguments:
        history -- A representation of the previous moves
        epsilon -- Random state. Helps to keep the agent discover new moves
        step -- Current step in the learning process
        model -- The current model we want an action from
    
    Returns:
        Integer -- An integer in range(0,action_size) (for breakout games action_size = 3)
    """
    if np.random.rand() <= epsilon or step <= FLAGS.observe_step_num:
        return random.randrange(ACTION_SIZE)
    else:
        q_value = model.predict([history, np.ones(ACTION_SIZE).reshape(1, ACTION_SIZE)])
        return np.argmax(q_value[0])



def store_memory(memory, history, action, reward, next_history, dead):
    """Store step data in memory to be used later
    """
    memory.append((history, action, reward, next_history, dead))


def get_one_hot(targets, nb_classes):
    return np.eye(nb_classes)[np.array(targets).reshape(-1)]


def train_memory_batch(memory, model, log_dir):
    """Use the mini-batch approach to train the model
    
    Arguments:
        memory -- Short term memory of previous training
        model -- The model we want to train
        log_dir -- The directory where to save logs
    
    Returns:
        float -- Loss of the last training step
    """
    mini_batch = random.sample(memory, FLAGS.batch_size)
    history = np.zeros((FLAGS.batch_size, ATARI_SHAPE[0],
                        ATARI_SHAPE[1], ATARI_SHAPE[2]))
    next_history = np.zeros((FLAGS.batch_size, ATARI_SHAPE[0],
                             ATARI_SHAPE[1], ATARI_SHAPE[2]))
    target = np.zeros((FLAGS.batch_size,))
    action, reward, dead = [], [], []

    for idx, val in enumerate(mini_batch):
        history[idx] = val[0]
        next_history[idx] = val[3]
        action.append(val[1])
        reward.append(val[2])
        dead.append(val[4])

    actions_mask = np.ones((FLAGS.batch_size, ACTION_SIZE))
    next_Q_values = model.predict([next_history, actions_mask])

    # like Q Learning, get maximum Q value at s'
    # But from target model
    for i in range(FLAGS.batch_size):
        if dead[i]:
            target[i] = -1
        else:
            target[i] = reward[i] + FLAGS.gamma * np.amax(next_Q_values[i])

    action_one_hot = get_one_hot(action, ACTION_SIZE)
    target_one_hot = action_one_hot * target[:, None]

    h = model.fit(
        [history, action_one_hot], target_one_hot, epochs=1,
        batch_size=FLAGS.batch_size, verbose=0)

    return h.history['loss'][0]


def train(env_chosen):
    env = env_chosen

    # deque: Once a bounded length deque is full, when new items are added,
    # a corresponding number of items are discarded from the opposite end
    memory = deque(maxlen=FLAGS.replay_memory)
    episode_number = 0
    epsilon = FLAGS.init_epsilon
    epsilon_decay = (FLAGS.init_epsilon - FLAGS.final_epsilon) / FLAGS.epsilon_step_num
    global_step = 0
    scores = []

    if FLAGS.resume:
        model = load_model(FLAGS.restore_file_path, custom_objects={'huber_loss': huber_loss})
        # Assume when we restore the model, the epsilon has already decreased to the final value
        epsilon = FLAGS.final_epsilon
    else:
        model = breakout_model()

    now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    log_dir = "{}/run-{}-log".format(FLAGS.train_dir, now)
    file_writer = tf.summary.FileWriter(log_dir, tf.get_default_graph())

    model_target = clone_model(model)
    model_target.set_weights(model.get_weights())

    while episode_number < FLAGS.num_episode:

        done = False
        dead = False
        # 1 episode = 5 lives
        step, score, start_life = 0, 0, 5
        loss = 0.0
        observe = env.reset()

        # this is one of DeepMind's idea.
        # just do nothing at the start of episode to avoid sub-optimal
        for _ in range(random.randint(1, FLAGS.no_op_steps)):
            observe, _, _, _ = env.step(1)
        # At start of episode, there is no preceding frame
        # So just copy initial states to make history
        state = pre_processing(observe)
        history = np.stack((state, state, state, state), axis=2)
        history = np.reshape([history], (1, 84, 84, 4))

        while not done:
            if FLAGS.render:
                #env.render()
                time.sleep(0.01)

            # get action for the current history and go one step in environment
            action = get_action(history, epsilon, global_step, model_target)

            # scale down epsilon, the epsilon only begin to decrease after observe steps
            if epsilon > FLAGS.final_epsilon and global_step > FLAGS.observe_step_num:
                epsilon -= epsilon_decay

            observe, reward, done, _ = env.step(action)
            # pre-process the observation --> history
            next_state = pre_processing(observe)
            next_state = np.reshape([next_state], (1, 84, 84, 1))
            next_history = np.append(next_state, history[:, :, :, :3], axis=3)

            # if the agent missed ball, agent is dead --> episode is not over
            #if start_life > info['ale.lives']:
            #    dead = True
            #    start_life = info['ale.lives']

            # TODO: may be we should give negative reward if miss ball (dead)
            # reward = np.clip(reward, -1., 1.)  # clip here is not correct

            # save the statue to memory, each replay takes 2 * (84*84*4) bytes = 56448 B = 55.125 KB
            store_memory(memory, history, action, reward, next_history, dead)  #

            # check if the memory is ready for training
            if global_step > FLAGS.observe_step_num:
                loss = loss + train_memory_batch(memory, model, log_dir)
                # if loss > 100.0:
                #    print(loss)
                if global_step % FLAGS.refresh_target_model_num == 0:  # update the target model
                    model_target.set_weights(model.get_weights())

            score += reward

            # If agent is dead, set the flag back to false, but keep the history unchanged,
            # to avoid to see the ball up in the sky
            if dead:
                dead = False
            else:
                history = next_history

            #print("step: ", global_step)
            global_step += 1
            step += 1

            if done:
                if global_step <= FLAGS.observe_step_num:
                    state = "observe"
                elif FLAGS.observe_step_num < global_step <= FLAGS.observe_step_num + FLAGS.epsilon_step_num:
                    state = "explore"
                else:
                    state = "train"
                scores.append(score)
                print('state: {}, episode: {}, score: {}, global_step: {}, avg loss: {}, step: {}, memory length: {}'
                      .format(state, episode_number, score, global_step, loss / float(step), step, len(memory)))

                if episode_number % 100 == 0 or (episode_number + 1) == FLAGS.num_episode:
                #if episode_number % 1 == 0 or (episode_number + 1) == FLAGS.num_episode:  # debug
                    now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
                    file_name = "breakout_model_{}.h5".format(now)
                    model_path = os.path.join(FLAGS.train_dir, file_name)
                    model.save(model_path)

                # Add user custom data to TensorBoard
                loss_summary = tf.Summary(
                    value=[tf.Summary.Value(tag="loss", simple_value=loss / float(step))])
                file_writer.add_summary(loss_summary, global_step=episode_number)

                score_summary = tf.Summary(
                    value=[tf.Summary.Value(tag="score", simple_value=score)])
                file_writer.add_summary(score_summary, global_step=episode_number)

                episode_number += 1

    file_writer.close()
    plt.scatter(scores)
    z = np.polyfit([elem for elem in range(len(scores))],scores, 1)
    p = np.poly1d(z)
    plt.plot(scores,p(scores),"ro")
    plt.show()


def test(env_chosen):
    env = env_chosen

    episode_number = 0
    epsilon = 0.001
    global_step = FLAGS.observe_step_num+1
    # model = load_model(FLAGS.restore_file_path)
    model = load_model(FLAGS.restore_file_path, custom_objects={'huber_loss': huber_loss})  # load model with customized loss func

    # test how to deep copy a model
    '''
    model_copy = clone_model(model)    # only copy the structure, not the value of the weights
    model_copy.set_weights(model.get_weights())
    '''

    while episode_number < FLAGS.num_episode:

        done = False
        dead = False
        # 1 episode = 5 lives
        score, start_life = 0, 5
        observe = env.reset()

        observe, _, _, _ = env.step(1)
        # At start of episode, there is no preceding frame
        # So just copy initial states to make history
        state = pre_processing(observe)
        history = np.stack((state, state, state, state), axis=2)
        history = np.reshape([history], (1, 84, 84, 4))

        while not done:

            # get action for the current history and go one step in environment
            action = get_action(history, epsilon, global_step, model)
            # change action to real_action
            real_action = action + 1

            observe, reward, done, _ = env.step(real_action)
            # pre-process the observation --> history
            next_state = pre_processing(observe)
            next_state = np.reshape([next_state], (1, 84, 84, 1))
            next_history = np.append(next_state, history[:, :, :, :3], axis=3)

            # if the agent missed ball, agent is dead --> episode is not over
            #if start_life > info['ale.lives']:
            #    dead = True
            #    start_life = info['ale.lives']

            # TODO: may be we should give negative reward if miss ball (dead)
            reward = np.clip(reward, -1., 1.)

            score += reward

            # If agent is dead, set the flag back to false, but keep the history unchanged,
            # to avoid to see the ball up in the sky
            if dead:
                dead = False
            else:
                history = next_history

            # print("step: ", global_step)
            global_step += 1

            if done:
                episode_number += 1
                print('episode: {}, score: {}'.format(episode_number, score))


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("env", help="The model you want to use. At the moment it only support 'atari' or 'homemade'")
    parser.add_argument("mode", help="Wether you want to train or test the model. Use 'train' or 'test'")
    parser.add_argument("--model", help="Path to a model you want to use. If you define one for a \
    training, this model will be loaded and training will pursue")
    args = parser.parse_args()
    if args.env == 'homemade':
        tf.app.flags.DEFINE_string('train_dir', 'tf_train_breakout/homemade',
                           """Directory where to write event logs and checkpoint. """)
        ENV_CHOSEN = Game_adapted(limit_fps=False)
    elif args.env =='atari':
        tf.app.flags.DEFINE_string('train_dir', 'tf_train_breakout/atari',
                           """Directory where to write event logs and checkpoint. """)
        ENV_CHOSEN = gym.make('BreakoutDeterministic-v4')
    else:
        print("Missing or unknown env. Switching to atari")
        ENV_CHOSEN = gym.make('BreakoutDeterministic-v4')

    if args.model:
        tf.app.flags.DEFINE_string('restore_file_path',
                           args.model,
                           """Path of the restore file """)
        tf.app.flags.DEFINE_boolean('resume', True,
                            """Whether to resume from previous checkpoint.""")
    else:
        tf.app.flags.DEFINE_boolean('resume', False,
                            """Whether to resume from previous checkpoint.""")

    if args.mode == 'train':
        train(ENV_CHOSEN)
    elif args.mode == 'test':
        test(ENV_CHOSEN)
    else:
        print("You have to choose a mode to launch this script. Run with --help to have more information")


if __name__ == '__main__':
    tf.app.run()
