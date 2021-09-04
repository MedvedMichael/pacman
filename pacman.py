from io import TextIOWrapper
import directions
import pygame.image as image
import pygame.transform as transform


class Pacman():

    def __init__(self, x: int, y: int, width: int, file: TextIOWrapper):
        self.x = x
        self.y = y
        self.score = 0
        self.width = width
        self.direction = directions.DOWN
        self.choice = directions.NOWAY
        self.matrix = list(map(lambda line: list(
            map(lambda x: int(x), line[:-1])), file))

        walkRight = list(map(lambda x: transform.scale(x, (width, width)), [image.load(
            './assets/right1.png'), image.load('./assets/right2.png'), image.load('./assets/right3.png')]))

        walkLeft = list(map(lambda x: transform.scale(x, (width, width)), [image.load(
            './assets/left1.png'), image.load('./assets/left2.png'), image.load('./assets/left3.png')]))

        walkUp = list(map(lambda x: transform.rotate(x, 90), walkRight))

        walkDown = list(map(lambda x: transform.rotate(x, 90), walkLeft))
        self.walk_images = [walkLeft, walkUp, walkRight, walkDown]

    def get_current_frame(self, state):
        return self.walk_images[self.direction][state]

    def change_direction(self, direction):
        self.choice = direction

    def move(self):
        matrix_x = self.x // self.width + \
            (1 if self.x % self.width != 0 and self.direction == directions.LEFT else 0)
        matrix_y = self.y // self.width + \
            (1 if self.y % self.width != 0 and self.direction == directions.UP else 0)

        if self.x % self.width == 0 and self.y % self.width == 0:
            if(self.matrix[matrix_y][matrix_x] == 2):
                self.score += 1
                self.matrix[matrix_y][matrix_x] = 0
            elif(self.matrix[matrix_y][matrix_x] == 3):
                self.score += 3
                self.matrix[matrix_y][matrix_x] = 0

            if self.choice != directions.NOWAY and \
                ((self.choice == directions.LEFT and not (self.x % self.width == 0 and self.matrix[matrix_y][matrix_x-1] == 1)) or
                 (self.choice == directions.UP and not (self.y % self.width == 0 and self.matrix[matrix_y-1][matrix_x] == 1)) or
                    (self.choice == directions.RIGHT and not (self.x % self.width == 0 and self.matrix[matrix_y][matrix_x+1] == 1)) or
                    (self.choice == directions.DOWN and not (self.y % self.width == 0 and self.matrix[matrix_y+1][matrix_x] == 1))):
                self.direction = self.choice
                self.choice = directions.NOWAY

        if self.direction == directions.LEFT and not (self.x % self.width == 0 and self.matrix[matrix_y][matrix_x-1] == 1):
            self.x -= 1
        elif self.direction == directions.UP and not (self.y % self.width == 0 and self.matrix[matrix_y-1][matrix_x] == 1):
            self.y -= 1
        elif self.direction == directions.RIGHT and not (self.x % self.width == 0 and self.matrix[matrix_y][matrix_x+1] == 1):
            self.x += 1
        elif self.direction == directions.DOWN and not (self.y % self.width == 0 and self.matrix[matrix_y+1][matrix_x] == 1):
            self.y += 1

    def draw(self, window, state):
        window.blit(self.get_current_frame(state), (self.x, self.y))

        # To draw a red rectangle uncomment
        # pydraw.rect(window, (255, 0, 0), pygame.Rect(
        #     (self.x // self.width + (1 if self.direction ==
        #                              directions.LEFT and self.x % self.width != 0 else 0))*self.width,
        #     (self.y // self.width + (1 if self.direction ==
        #                              directions.UP and self.y % self.width != 0 else 0))*self.width,
        #     self.width, self.width), 2)
