import math
from time import time
from a_star import a_star
from character import Character
import pygame.image as image
import pygame.transform as transform
from threading import Timer
import pygame.draw as pydraw
import pygame

import directions
from minimax import GameState, expectimax, generate_tree, generate_tree_recurs, minimax


class Pacman(Character):

    def __init__(self, x, y, width, matrix):
        Character.__init__(self, x, y, width, matrix)
        self.score = 0
        self.find_way = True
        self.angry_mode = False
        self.win = False
        self.time_counter = 0
        self.path = []
        self.speed = width
        self.target = None
        self.root_node = None
        self.vector_dict = {(0, 1): directions.LEFT, (0, -1): directions.RIGHT,
                            (-1, 0): directions.DOWN, (1, 0): directions.UP}

        walkRight = list(map(lambda x: transform.scale(x, (width, width)), [image.load(
            './assets/pacman/right1.png'), image.load('./assets/pacman/right2.png'), image.load('./assets/pacman/right3.png')]))

        walkLeft = list(map(lambda x: transform.scale(x, (width, width)), [image.load(
            './assets/pacman/left1.png'), image.load('./assets/pacman/left2.png'), image.load('./assets/pacman/left3.png')]))

        walkUp = list(map(lambda x: transform.rotate(x, 90), walkRight))

        walkDown = list(map(lambda x: transform.rotate(x, 90), walkLeft))
        self.walk_images = [walkLeft, walkUp, walkRight, walkDown]

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
            # print(self.matrix[matrix_y][matrix_x])

            if self.matrix[matrix_y][matrix_x] == 2 or self.matrix[matrix_y][matrix_x] == 3:
                if self.matrix[matrix_y][matrix_x] == 2:
                    self.score += 10
                else:
                    self.set_angry()

                self.matrix[matrix_y][matrix_x] = 0
                # print('NULL')
                # print((matrix_y, matrix_x))
                # print( (matrix_y, matrix_x))
                empty = Pacman.check_for_empty_matrix(self.matrix)
                if empty:
                    self.win = True
                    return

        moved = Character.move(self)
        if not moved:
            self.find_way = False

    def set_new_target(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j] in [2, 3]:
                    self.target = (i, j)
                    return

    def auto_move(self, enemies_coords=[]):
        if self.x % self.width == 0 and self.y % self.width == 0:
            current_coord = self.get_matrix_coordinates()
            if self.target is None:  # and self.time_counter % 50 == 0:
                for i in range(len(self.matrix)):
                    for j in range(len(self.matrix[0])):
                        if self.matrix[i][j] in [2, 3]:
                            # node = (i, j)
                            # path = a_star(
                            # self.matrix, current_coord, node, enemies_coords if not self.angry_mode else [])
                            # if len(path) == 0:
                            #     continue

                            self.target = (i, j)
            if self.target is not None:
                self.path = a_star(
                    self.matrix, current_coord, self.target, enemies_coords if not (self.angry_mode and self.time_counter >= 100) else [])
                if len(self.path) > 0:
                    next_node = self.path[1 if len(self.path) > 1 else 0]

                    delta = (current_coord[0] - next_node[0],
                             current_coord[1] - next_node[1])

                    new_direction = self.vector_dict.get(delta)
                    if new_direction is not None:
                        self.direction = new_direction
                    else:
                        self.target = None
                else:
                    self.target = None

        self.move()

    def minimax_move(self, matrix):
        # current_coord = self.get_matrix_coordinates()
        # if current_coord == self.target:
        #     self.target = None
        # if self.target is None:  # and self.time_counter % 50 == 0:
        self.set_new_target()
        if self.target is not None:
            state = GameState(matrix)
            enemies_coords = state.get_enemies_positions()
            if self.root_node is not None:
                nodes = [item for sublist in
                    list(map(lambda child: child.children, self.root_node.children))
                 for item in sublist]
                big_flag = False
                for last_node in nodes:
                    last_enemies_coords = last_node.state.get_enemies_positions()
                    flag = True
                    for enemies_coord in enemies_coords:
                        if enemies_coord not in last_enemies_coords:
                            flag = False
                            break

                    if flag:
                        self.root_node = last_node
                        generate_tree_recurs(last_node, 1, self.matrix, self.target)
                        print('FOUND')
                        big_flag = True
                        break
                # if not big_flag:
                self.root_node = generate_tree(state, self.target)
            else:
                self.root_node = generate_tree(state, self.target)
            best_value = minimax(self.root_node, -math.inf, math.inf, 0)
            # best_value = expectimax(self.root_node, 0)

            pacman_position = self.get_matrix_coordinates()
            for child in self.root_node.children:
                if child.value == best_value:
                    new_position = child.state.get_pacman_position()
                    delta = (pacman_position[0] - new_position[0],
                             pacman_position[1] - new_position[1])
                    new_direction = self.vector_dict.get(delta)
                    if new_direction is not None:
                        self.direction = new_direction
                    else:
                        self.set_new_target()
                    break
        self.move()

    def draw(self, window, state):
        if self.angry_mode:
            pydraw.rect(window, (255, 0, 0 if self.time_counter >= 200 else 255, 255), pygame.Rect(
                self.x, self.y, self.width, self.width))

        Character.draw(self, window, state)
