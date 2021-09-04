from pacman import Pacman
import pygame
import pygame.display as display
import pygame.image as image
import pygame.event as events
import pygame.key as key
import pygame.transform as transform
import directions
import pygame.draw as pydraw

unit_width = 24
player = Pacman(unit_width, unit_width, unit_width, open("level.txt", "r"))
game_bounds = [len(player.matrix[0])*unit_width,
               len(player.matrix)*unit_width + 40]

[width, height] = game_bounds

pygame.init()
font = pygame.font.SysFont('Comic Sans MS', 30)
window = display.set_mode((width, height))
display.set_caption("Pac-Man")

paths = ['./assets/empty.png', './assets/wall2.png',
         './assets/food_small.png', './assets/food_big.png']
images = map(lambda x: pygame.transform.scale(
    image.load(x), (unit_width, unit_width)), paths)

[empty, wall, small_food, big_food] = images


def init_draw():
    matrix = player.matrix
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            num = matrix[i][j]
            picture = empty
            if num == 1:
                picture = wall
            if num == 2:
                picture = small_food
            if num == 3:
                picture = big_food

            window.blit(picture, (j*unit_width, i*unit_width))


ticks = 0
change_skin_ticks = 0
last_score = -1


def draw():
    player.draw(window, change_skin_ticks % 3)
    if last_score != player.score:
        textsurface = font.render(
            'Score: ' + str(player.score), False, (255, 255, 255))
        pydraw.rect(window, (0, 0, 0, 255), pygame.Rect(
            0, game_bounds[1]-40, game_bounds[0], game_bounds[1]))
        window.blit(textsurface, (10, game_bounds[1]-40))
    display.update()


init_draw()

run = True
while run:
    pygame.time.delay(10)
    ticks += 1
    if ticks % 10 == 0:
        change_skin_ticks += 1
    for event in events.get():
        if event.type == pygame.QUIT:
            run = False
    keys = key.get_pressed()
    window.blit(empty, (player.x, player.y))
    player.move()

    draw()

    if keys[pygame.K_LEFT]:
        player.change_direction(directions.LEFT)

    elif keys[pygame.K_RIGHT]:
        player.change_direction(directions.RIGHT)

    elif keys[pygame.K_UP]:
        player.change_direction(directions.UP)

    elif keys[pygame.K_DOWN]:
        player.change_direction(directions.DOWN)
