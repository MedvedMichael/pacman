from draws import draw_unit
import directions
from math import sqrt, pow
import pygame
from pygame import draw as pydraw


class Character:
    def __init__(self, x, y, width, matrix):
        self.x = x
        self.y = y
        self.width = width
        self.direction = directions.RIGHT
        self.choice = directions.NOWAY
        self.matrix = matrix
        self.speed = width

    def get_current_frame(self, state):
        return self.walk_images[self.direction][state]

    def change_direction(self, direction):
        self.choice = direction

    def get_matrix_coordinates(self):
        matrix_x = self.x // self.width + \
            (1 if self.x % self.width != 0 and self.direction == directions.LEFT else 0)
        matrix_y = self.y // self.width + \
            (1 if self.y % self.width != 0 and self.direction == directions.UP else 0)
        return (matrix_y, matrix_x)
    
    def get_next_matrix_coordinates(self):
        matrix_x = self.x // self.width + \
            (1 if self.x % self.width != 0 and self.direction == directions.RIGHT else 0)
        matrix_y = self.y // self.width + \
            (1 if self.y % self.width != 0 and self.direction == directions.DOWN else 0)

        return (matrix_y, matrix_x)

    def paintover(self, window):
        # Last method of paintover, redraws food!!!
        # draw_unit(window, draws.EMPTY, (self.x, self.y))

        (matrix_y, matrix_x) = self.get_next_matrix_coordinates()
        # print('Paintover')
        # print(self.get_matrix_coordinates())
        draw_unit(window, self.matrix[matrix_y][matrix_x],
                  (matrix_x*self.width, matrix_y*self.width))
        extra_unit = (matrix_y,matrix_x+1)
        if self.direction == directions.LEFT:
            extra_unit = (matrix_y,matrix_x-1)
        if self.direction == directions.UP:
            extra_unit = (matrix_y-1,matrix_x)
        if self.direction == directions.DOWN:
            extra_unit = (matrix_y+1,matrix_x)
        
        draw_unit(window, self.matrix[extra_unit[0]][extra_unit[1]],
                  (extra_unit[1]*self.width, extra_unit[0]*self.width))
        

    def move(self):
        (matrix_y, matrix_x) = self.get_matrix_coordinates()

        if self.x % self.width == 0 and self.y % self.width == 0:
            if self.choice != directions.NOWAY and \
                ((self.choice == directions.LEFT and not (self.x % self.width == 0 and self.matrix[matrix_y][matrix_x-1] == 1)) or
                 (self.choice == directions.UP and not (self.y % self.width == 0 and self.matrix[matrix_y-1][matrix_x] == 1)) or
                    (self.choice == directions.RIGHT and not (self.x % self.width == 0 and self.matrix[matrix_y][matrix_x+1] == 1)) or
                    (self.choice == directions.DOWN and not (self.y % self.width == 0 and self.matrix[matrix_y+1][matrix_x] == 1))):
                self.direction = self.choice
                self.choice = directions.NOWAY

        moved = False
        if self.direction == directions.LEFT and not (self.x % self.width == 0 and self.matrix[matrix_y][matrix_x-1] == 1):
            self.x -= self.speed
            moved = True
        elif self.direction == directions.UP and not (self.y % self.width == 0 and self.matrix[matrix_y-1][matrix_x] == 1):
            self.y -= self.speed
            moved = True
        elif self.direction == directions.RIGHT and not (self.x % self.width == 0 and self.matrix[matrix_y][matrix_x+1] == 1):
            moved = True
            self.x += self.speed
        elif self.direction == directions.DOWN and not (self.y % self.width == 0 and self.matrix[matrix_y+1][matrix_x] == 1):
            moved = True
            self.y += self.speed

        return moved

    def get_center_coordinate(self):
        return (self.x + self.width/2, self.y + self.width / 2)

    def get_distance_between_coordinates(coord1, coord2):
        (x1, y1) = coord1
        (x2, y2) = coord2
        return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))

    def check_collision(self, character):
        return Character.get_distance_between_coordinates((self.x, self.y), (character.x, character.y)) <= self.width * 0.4

    def draw(self, window, state):
        window.blit(self.get_current_frame(state), (self.x, self.y))

        # To draw a red rectangle uncomment
        # pydraw.rect(window, (255, 0, 0), pygame.Rect(
        #     (self.x // self.width + (1 if self.direction ==
        #                              directions.LEFT and self.x % self.width != 0 else 0))*self.width,
        #     (self.y // self.width + (1 if self.direction ==
        #                              directions.UP and self.y % self.width != 0 else 0))*self.width,
        #     self.width, self.width), 2)
