from os import system
import random
from time import time, strftime, localtime
from a_star import a_star
from character import Character
import pygame.image as image
import pygame.transform as transform
from threading import Timer
import pygame.draw as pydraw
import pygame

import directions
from collections import deque

import tensorflow as tf
from dqn import *

# f = open(r'./saves/checkpoint', encoding='latin-1')
# path = 'saves/' + f.readline().split(": ")[-1][1:-2]
# print(path)

dqn_params = {
    "width": 21,
    "height": 18,
    "num_training": 10000,
    # Model backups
    'load_file': 'saves/model-model_1_9565_125',
    'save_file': 'model_1',
    'save_interval': 20,

    # Training parameters
    'train_start': 30,    # Episodes before training starts
    'batch_size': 32,       # Replay memory batch size
    'mem_size': 100000,     # Replay memory size

    'discount': 0.95,       # Discount rate (gamma value)
    'lr': .0002,            # Learning reate
    # 'rms_decay': 0.99,      # RMS Prop decay (switched to adam)
    # 'rms_eps': 1e-6,        # RMS Prop epsilon (switched to adam)

    # Epsilon value (epsilon-greedy)
    'eps': 1.0,             # Epsilon start value
    'eps_final': 0.1,       # Epsilon end value
    'eps_step': 10000       # Epsilon steps between start and end (linear)
}

qnet = DQN(dqn_params)


class Pacman(Character):

    def __init__(self, x, y, width, matrix, args):
        Character.__init__(self, x, y, width, matrix)
        self.score = 0
        self.find_way = True
        self.angry_mode = False
        self.win = False
        self.time_counter = 0
        self.path = []
        self.speed = 1
        self.target = None
        self.last_action = None
        self.frame = 0
        self.terminal = True
        self.ep_rew = 0
        self.debounceCounter = 0

        walkRight = list(map(lambda x: transform.scale(x, (width, width)), [image.load(
            './assets/pacman/right1.png'), image.load('./assets/pacman/right2.png'), image.load('./assets/pacman/right3.png')]))

        walkLeft = list(map(lambda x: transform.scale(x, (width, width)), [image.load(
            './assets/pacman/left1.png'), image.load('./assets/pacman/left2.png'), image.load('./assets/pacman/left3.png')]))

        walkUp = list(map(lambda x: transform.rotate(x, 90), walkRight))

        walkDown = list(map(lambda x: transform.rotate(x, 90), walkLeft))
        self.walk_images = [walkLeft, walkUp, walkRight, walkDown]

        print("Initialise DQN Agent")

        self.params = dqn_params

        gpu_options = tf.compat.v1.GPUOptions(
            per_process_gpu_memory_fraction=0.1)
        self.sess = tf.compat.v1.Session(
            config=tf.compat.v1.ConfigProto(gpu_options=gpu_options))
        self.qnet = qnet

        self.general_record_time = strftime(
            "%a_%d_%b_%Y_%H_%M_%S", localtime())

        self.Q_global = []
        self.cost_disp = 0

        self.cnt = self.qnet.sess.run(self.qnet.global_step)
        self.local_cnt = 0

        self.numeps = 0
        self.last_score = 0
        self.s = time()
        self.last_reward = 0.

        self.replay_mem = deque()
        self.last_scores = deque()
    
    def reset(self):
        self.numeps += 1
        self.last_action = None
        self.frame = 0
        self.terminal = True
        self.ep_rew = 0
        self.debounceCounter = 0
        self.Q_global = []
        self.cost_disp = 0

        # Stats
        self.cnt = self.qnet.sess.run(self.qnet.global_step)
        self.local_cnt = 0

        self.last_score = 0
        self.s = time()
        self.last_reward = 0.

        self.replay_mem = deque()
        self.last_scores = deque()

        self.score = 0


    def set_coords(self, y, x):
        self.x = x
        self.y = y

    def ai_move(self):
        self.debounceCounter += 1

        if self.x % self.width == 0 and self.y % self.width == 0:
            if self.debounceCounter >= 20:
                self.debounceCounter = 0
                self.observation_step()
            if np.random.rand() > self.params['eps']:
                self.Q_pred = self.qnet.sess.run(
                    self.qnet.y,
                    feed_dict={self.qnet.x: np.reshape(self.matrix,
                                                       (1, self.params['width'], self.params['height'], 1)),
                               self.qnet.q_t: np.zeros(1),
                               self.qnet.actions: np.zeros((1, 4)),
                               self.qnet.terminals: np.zeros(1),
                               self.qnet.rewards: np.zeros(1)})[0]

                self.Q_global.append(max(self.Q_pred))
                a_winner = np.argwhere(self.Q_pred == np.amax(self.Q_pred))
                if len(a_winner) > 1:
                    move = a_winner[np.random.randint(0, len(a_winner))][0]
                else:
                    move = a_winner[0][0]
            else:
                move = np.random.randint(0, 4)

            self.change_direction(move)
            self.last_action = move

        self.move()

    def train(self):
        # Train
        if (self.local_cnt > self.params['train_start']):
            batch = random.sample(self.replay_mem, self.params['batch_size'])
            batch_s = []  # States (s)
            batch_r = []  # Rewards (r)
            batch_a = []  # Actions (a)
            batch_n = []  # Next states (s')
            batch_t = []  # Terminal state (t)

            for i in batch:
                batch_s.append(i[0])
                batch_r.append(i[1])
                batch_a.append(i[2])
                batch_n.append(np.transpose(i[3]))
                batch_t.append(i[4])
            batch_s = np.reshape(
                batch_s[0], (1, self.params['width'], self.params['height'], 1))
            batch_r = np.array(batch_r)
            batch_a = self.get_onehot(np.array(batch_a))
            batch_n = np.reshape(
                batch_n[0], (1, self.params['width'], self.params['height'], 1))
            batch_t = np.array(batch_t)

            self.cnt, self.cost_disp = self.qnet.train(
                batch_s, batch_a, batch_t, batch_n, batch_r)

    def get_onehot(self, actions):
        """ Create list of vectors with 1 values at index of action in list """
        actions_onehot = np.zeros((self.params['batch_size'], 4))
        for i in range(len(actions)):
            actions_onehot[i][int(actions[i])] = 1
        return actions_onehot

    def observation_step(self, final=False):
        if self.last_action is not None:
            self.last_state = np.copy(self.matrix)

            # Process current experience reward
            self.current_score = self.score
            reward = self.current_score - self.last_score
            self.last_score = self.current_score

            if reward >= 400:
                self.last_reward = 200
            elif reward >= 10:
                self.last_reward = 70
            elif reward <= -10:
                self.last_reward = -700
            elif reward <= 0:
                self.last_reward = -3

            
            self.ep_rew += self.last_reward

            experience = (self.last_state, float(self.last_reward),
                          self.last_action, self.matrix, self.terminal)
            self.replay_mem.append(experience)
            if len(self.replay_mem) > self.params['mem_size']:
                self.replay_mem.popleft()

            if final and dqn_params['save_file'] :
                if self.local_cnt > self.params['train_start']:# and self.local_cnt % self.params['save_interval'] == 0:
                    self.qnet.save_ckpt(
                        'saves/model-' + dqn_params['save_file'] + "_" + str(self.cnt) + '_' + str(self.numeps))

            self.train()

        self.local_cnt += 1
        self.frame += 1
        self.params['eps'] = max(self.params['eps_final'],
                                 1.00 - float(self.cnt) / float(self.params['eps_step']))

    def set_angry_mode(self, value):
        self.angry_mode = value

    def set_angry(self):
        self.angry_mode = True
        self.time_counter = 1000

    def check_for_empty_matrix(matrix):
        for line in matrix:
            for num in line:
                if num == 2 or num == 3:
                    return False
        return True

    def tick_counter(self):
        if self.time_counter != 0:
            self.time_counter -= 1
        else:
            if self.angry_mode:
                self.angry_mode = False

    def move(self):
        self.tick_counter()
        (matrix_y, matrix_x) = self.get_matrix_coordinates()
        if self.x % self.width == 0 and self.y % self.width == 0:
            self.find_way = True
            if self.matrix[matrix_y][matrix_x] == 2 or self.matrix[matrix_y][matrix_x] == 3:
                if self.matrix[matrix_y][matrix_x] == 2:
                    self.score += 10
                else:
                    self.set_angry()

                self.matrix[matrix_y][matrix_x] = 0
                empty = Pacman.check_for_empty_matrix(self.matrix)
                if empty:
                    self.win = True
                    return

        moved = Character.move(self)
        if not moved:
            self.find_way = False

    def set_new_target(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] in [2, 3]:
                    self.target = (i, j)
                    return

    def auto_move(self, enemies_coords=[]):
        if self.x % self.width == 0 and self.y % self.width == 0:
            current_coord = self.get_matrix_coordinates()
            if self.target is None and self.time_counter % 50 == 0:
                for i in range(len(self.matrix)):
                    for j in range(len(self.matrix[0])):
                        if self.matrix[i][j] in [2, 3]:
                            node = (i, j)
                            path = a_star(
                                self.matrix, current_coord, node, enemies_coords if not self.angry_mode else [])
                            if len(path) == 0:
                                continue

                            self.target = (i, j)
                            return
            if self.target is not None:
                self.path = a_star(
                    self.matrix, current_coord, self.target, enemies_coords if not (self.angry_mode and self.time_counter >= 100) else [])
                if len(self.path) > 0:
                    next_node = self.path[1 if len(self.path) > 1 else 0]
                    vector_dict = {(0, 1): directions.LEFT, (0, -1): directions.RIGHT,
                                   (-1, 0): directions.DOWN, (1, 0): directions.UP}
                    delta = (current_coord[0] - next_node[0],
                             current_coord[1] - next_node[1])

                    new_direction = vector_dict.get(delta)
                    if new_direction is not None:
                        self.direction = new_direction
                    else:
                        self.target = None
                else:
                    self.target = None

        self.move()

    def draw(self, window, state):
        if self.angry_mode:
            pydraw.rect(window, (255, 0, 0 if self.time_counter >= 200 else 255, 255), pygame.Rect(
                self.x, self.y, self.width, self.width))

        Character.draw(self, window, state)
