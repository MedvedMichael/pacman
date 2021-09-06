from character import Character
import directions
import pygame.image as image
import pygame.transform as transform
from random import randint


class Enemy(Character):
    def __init__(self, x, y, width, matrix, type):
        Character.__init__(self, x, y, width, matrix)
        dirs = ["left", "up", "right", "down"]
        self.walk_images = []
        self.color = type
        for name in dirs:
            self.walk_images.append(
                [transform.scale(
                    image.load('./assets/enemies/' + type + '/' +
                               name + '_' + str(i+1) + '.png'),
                    (width, width))
                 for i in range(2)])

    def move(self):
        moved = Character.move(self)
        if not moved or (self.y % self.width == 0 and self.x % self.width == 0 and randint(0, 100) > 70):
            (matrix_y, matrix_x) = self.get_matrix_coordinates()
            available_directions = []
            if self.matrix[matrix_y][matrix_x-1] != 1:
                available_directions.append(directions.LEFT)
            if self.matrix[matrix_y-1][matrix_x] != 1:
                available_directions.append(directions.UP)
            if self.matrix[matrix_y][matrix_x+1] != 1:
                available_directions.append(directions.RIGHT)
            if self.matrix[matrix_y+1][matrix_x] != 1:
                available_directions.append(directions.DOWN)

            if len(available_directions) > 1:
                if self.direction == directions.LEFT and directions.RIGHT in available_directions:
                    available_directions.remove(directions.RIGHT)
                elif self.direction == directions.RIGHT and directions.LEFT in available_directions:
                    available_directions.remove(directions.LEFT)
                elif self.direction == directions.UP and directions.DOWN in available_directions:
                    available_directions.remove(directions.DOWN)
                elif self.direction == directions.DOWN and directions.UP in available_directions:
                    available_directions.remove(directions.UP)
            random_choice = randint(0, len(available_directions) - 1)
            self.direction = available_directions[random_choice]
