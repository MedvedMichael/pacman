from random import randint
from enemy import Enemy
from pacman import Pacman
import pygame
import pygame.display as display
import pygame.image as image
import pygame.event as events
import pygame.key as key
import pygame.transform as transform
import directions
import pygame.draw as pydraw
from draws import unit_width, images, draw_unit

[empty, wall, small_food, big_food] = images

matrix = list(map(lambda line: list(
    map(lambda x: int(x), line[:-1])), open("level.txt", "r")))

player = Pacman(unit_width, unit_width, unit_width, matrix)

game_bounds = [len(matrix[0])*unit_width,
               len(matrix)*unit_width + 40]

[width, height] = game_bounds


def get_enemies_start_positions():
    arr = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 6:
                arr.append((j*unit_width, i*unit_width))
                matrix[i][j] = 0
    return arr


colors = ["red", "pink", "blue", "yellow"]
enemies_start_positions = get_enemies_start_positions()
enemies = [Enemy(enemies_start_positions[i][0], enemies_start_positions[i]
                 [1], unit_width, matrix, colors[i]) for i in range(len(colors))]


pygame.init()
font = pygame.font.SysFont('Comic Sans MS', 30)
window = display.set_mode((width, height))
display.set_caption("Pac-Man")





def init_draw():
    matrix = player.matrix
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            num = matrix[i][j]
            if num != 6:
                draw_unit(window, num, (j*unit_width, i*unit_width))


ticks = 0
change_skin_ticks = 0
last_score = -1


def draw():
    player.draw(window, change_skin_ticks % 3)
    for enemy in enemies:
        enemy.draw(window, change_skin_ticks % 2)

    if last_score != player.score:
        textsurface = font.render(
            'Score: ' + str(player.score), False, (255, 255, 255))
        pydraw.rect(window, (0, 0, 0, 255), pygame.Rect(
            0, game_bounds[1]-40, game_bounds[0], game_bounds[1]))
        window.blit(textsurface, (10, game_bounds[1]-40))
    display.update()

init_draw()

def check_for_collisions():
    for enemy in enemies:
        check = player.check_collision(enemy)
        if check:
            return True
    return False


run = True
while run:
    pygame.time.delay(10)
    ticks += 1
    if ticks % 10 == 0:
        change_skin_ticks += 1

    check = check_for_collisions()
    if check:
        break
    for event in events.get():
        if event.type == pygame.QUIT:
            run = False
    keys = key.get_pressed()

    player.paintover(window)
    player.move()

    for enemy in enemies:
        enemy.paintover(window)
        enemy.move()

    draw()

    if keys[pygame.K_LEFT]:
        player.change_direction(directions.LEFT)

    elif keys[pygame.K_RIGHT]:
        player.change_direction(directions.RIGHT)

    elif keys[pygame.K_UP]:
        player.change_direction(directions.UP)

    elif keys[pygame.K_DOWN]:
        player.change_direction(directions.DOWN)
