from time import time
from a_star import a_star
from character import Character
import pygame.image as image
import pygame.transform as transform
from threading import Timer
import pygame.draw as pydraw
import pygame

import directions


class Pacman(Character):

    def __init__(self, x, y, width, matrix):
        Character.__init__(self, x, y, width, matrix)
        self.score = 0
        self.find_way = True
        self.angry_mode = False
        self.win = False
        self.time_counter = 0
        self.path = []
        self.speed = 2
        self.target = None

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
