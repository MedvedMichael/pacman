from time import time
from character import Character
import pygame.image as image
import pygame.transform as transform
from threading import Timer
import pygame.draw as pydraw
import pygame


class Pacman(Character):

    def __init__(self, x, y, width, matrix):
        Character.__init__(self, x, y, width, matrix)
        self.score = 0
        self.find_way = True
        self.angry_mode = False
        self.win = False
        self.time_counter = 0

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

    def draw(self, window, state):
        if self.angry_mode:
            pydraw.rect(window, (255, 0, 0 if self.time_counter >= 200 else 255, 255), pygame.Rect(
                self.x, self.y, self.width, self.width))

        Character.draw(self, window, state)
