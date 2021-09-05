from character import Character
import pygame.image as image
import pygame.transform as transform


class Pacman(Character):

    def __init__(self, x, y, width, matrix):
        Character.__init__(self, x, y, width, matrix)
        self.score = 0
        self.find_way = True

        walkRight = list(map(lambda x: transform.scale(x, (width, width)), [image.load(
            './assets/pacman/right1.png'), image.load('./assets/pacman/right2.png'), image.load('./assets/pacman/right3.png')]))

        walkLeft = list(map(lambda x: transform.scale(x, (width, width)), [image.load(
            './assets/pacman/left1.png'), image.load('./assets/pacman/left2.png'), image.load('./assets/pacman/left3.png')]))

        walkUp = list(map(lambda x: transform.rotate(x, 90), walkRight))

        walkDown = list(map(lambda x: transform.rotate(x, 90), walkLeft))
        self.walk_images = [walkLeft, walkUp, walkRight, walkDown]

    def move(self):
        (matrix_y, matrix_x) = self.get_matrix_coordinates()
        if self.x % self.width == 0 and self.y % self.width == 0:
            self.find_way = True
            if(self.matrix[matrix_y][matrix_x] == 2):
                self.score += 1
                self.matrix[matrix_y][matrix_x] = 0
            elif(self.matrix[matrix_y][matrix_x] == 3):
                self.score += 3
                self.matrix[matrix_y][matrix_x] = 0

        moved = Character.move(self)
        if not moved:
            self.find_way = False
