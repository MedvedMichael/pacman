from hashlib import new
from random import randint

from pygame.rect import Rect
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
import wayfinders
import draws
import pygame.font as pyfont
from copy import deepcopy

[empty, wall, small_food, big_food] = images

start_matrix = list(map(lambda line: list(
    map(lambda x: int(x), line[:-1])), open("level3.txt", "r")))

game_bounds = [len(start_matrix[0])*unit_width,
               len(start_matrix)*unit_width + 40]

[width, height] = game_bounds


def get_characters_start_positions(matrix):
    enemies = []
    pacman = None
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 6:
                enemies.append((j*unit_width, i*unit_width))
                matrix[i][j] = 0
            elif matrix[i][j] == 5:
                pacman = (j*unit_width, i*unit_width)
                matrix[i][j] = 0
    return (enemies, pacman)


pygame.init()
font = pyfont.SysFont('Comic Sans MS', 30)
window = display.set_mode((width, height))
display.set_caption("Pac-Man")


def init_draw():
    for i in range(len(start_matrix)):
        for j in range(len(start_matrix[0])):
            num = start_matrix[i][j]
            if num != 6 and num != 5:
                draw_unit(window, num, (j*unit_width, i*unit_width))
    display.update()


def check_for_collisions(player, enemies):
    for enemy in enemies:
        check = player.check_collision(enemy)
        if check:
            return enemy
    return None


last_game_result = None


def menu():

    run = True
    while run:
        pygame.time.delay(10)
        init_draw()
        keys = key.get_pressed()
        if keys[pygame.K_SPACE]:
            toQuit = game()
            if toQuit:
                break

        for event in events.get():
            if event.type == pygame.QUIT:
                run = False
        textsurface = font.render(
            ("Last game result: " + str(last_game_result[0]) + (
                " Won! " if last_game_result[1] else " Lost! ") if last_game_result != None else "")
            + "To play press Enter", False, (255, 255, 255))
        rect = textsurface.get_bounding_rect()
        pydraw.rect(window, (0, 0, 0, 255), pygame.Rect(
            0, game_bounds[1]-40, game_bounds[0], 40))
        window.blit(
            textsurface, (game_bounds[0]/2 - rect.width/2, game_bounds[1]-40))


def game():
    init_draw()
    matrix = deepcopy(start_matrix)
    colors = ["red", "pink", "blue", "yellow"]
    (enemies_start_positions,
     pacman_start_position) = get_characters_start_positions(matrix)
    enemies = [Enemy(enemies_start_positions[i][0], enemies_start_positions[i]
                     [1], unit_width, matrix, colors[i]) for i in range(len(colors))]
    player = Pacman(
        pacman_start_position[0], pacman_start_position[1], unit_width, matrix)

    mode = 'bfs'
    show_way = True
    ticks = 0
    change_skin_ticks = 0
    last_score = -1
    last_way = []

    def draw():
        player.draw(window, change_skin_ticks % 3)
        for enemy in enemies:
            enemy.draw(window, change_skin_ticks % 2)

        if last_score != player.score:
            textsurface = font.render(
                'Score: ' + str(player.score) +
                "   Mode " + mode +
                " Time: " + str(round(time*10000)/10000) +
                " Way length: " + str(len(way)), False, (255, 255, 255))
            pydraw.rect(window, (0, 0, 0, 255), pygame.Rect(
                0, game_bounds[1]-40, game_bounds[0], game_bounds[1]))
            window.blit(textsurface, (10, game_bounds[1]-40))
        display.update()

    toQuit = False
    run = True
    while run:
        pygame.time.delay(10)
        ticks += 1
        if ticks % 10 == 0:
            change_skin_ticks += 1

        check = check_for_collisions(player, enemies)
        if check != None:
            if not player.angry_mode:
                break
            else:
                check.paintover(window)
                enemies.remove(check)
                new_enemy = Enemy(enemies_start_positions[0][0], enemies_start_positions[0]
                     [1], unit_width, matrix, check.color)
                enemies.append(new_enemy)
                player.score+=400
        for event in events.get():
            if event.type == pygame.QUIT:
                run = False
                toQuit = True
                if player.timer:
                    print('lalala')
                    player.timer.cancel()
        keys = key.get_pressed()

        player.paintover(window)
        player.move()

        for enemy in enemies:
            enemy.paintover(window)
            enemy.move()

        if player.find_way:
            player.find_way = False
            func = wayfinders.bfs if mode == 'bfs' else wayfinders.dfs if mode == 'dfs' else wayfinders.uniform_cost_search
            player_coords = player.get_matrix_coordinates()
            enemy_coords = enemies[0].get_matrix_coordinates()
            (way, time) = wayfinders.count_time(lambda: func(
                matrix, player_coords, enemy_coords))
            # print(time)
            # print(len(way))
            for node in last_way:
                draw_unit(window, matrix[node[0]][node[1]],
                          (node[1]*unit_width, node[0]*unit_width))
            last_way = way
            if show_way:
                for i in range(len(way)):
                    pydraw.rect(window, ((i + 85) % 255, (i + 170) % 255, i % 255), pygame.Rect(
                        way[i][1]*unit_width, way[i][0]*unit_width, unit_width, unit_width))

            # For debug
            # pydraw.rect(window, (255, 0, 0), pygame.Rect(
            #     enemy_coords[1]*unit_width, enemy_coords[0]*unit_width, unit_width, unit_width), 2)

        if player.win:
            break
        draw()

        if keys[pygame.K_LEFT]:
            player.change_direction(directions.LEFT)

        elif keys[pygame.K_RIGHT]:
            player.change_direction(directions.RIGHT)

        elif keys[pygame.K_UP]:
            player.change_direction(directions.UP)

        elif keys[pygame.K_DOWN]:
            player.change_direction(directions.DOWN)

        elif keys[pygame.K_d]:
            mode = 'dfs'

        elif keys[pygame.K_b]:
            mode = 'bfs'

        elif keys[pygame.K_u]:
            mode = 'ucs'
        
        elif keys[pygame.K_s]:
            show_way = not show_way
            

    global last_game_result
    last_game_result = (player.score, player.win)
    return toQuit


menu()
# game()
