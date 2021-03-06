from math import e
import math
from random import randint, shuffle
import constants


def generate_base_matrix(free_width, free_height):
    width = free_width*2 + 1
    height = free_height*2 + 1
    matrix = []
    for i in range(height):
        if i % 2 == 0:
            matrix.append([1 for j in range(width)])
        else:
            matrix.append([1 if j % 2 == 0 else 0 for j in range(width)])

    return matrix


def break_walls(base_matrix, start_node, end_node):
    real_start_node = (start_node[0]*2 + 1, start_node[1]*2 + 1)
    # real_end_node = (end_node[0]*2 + 1, end_node[1]*2 + 1)
    delta = (end_node[1] - start_node[1], end_node[0] - start_node[0])
    if delta[0] == -1:
        base_matrix[real_start_node[0]][real_start_node[1]-1] = constants.EMPTY
    elif delta[0] == 1:
        base_matrix[real_start_node[0]][real_start_node[1]+1] = constants.EMPTY
    elif delta[1] == -1:
        base_matrix[real_start_node[0] -
                    1][real_start_node[1]] = constants.EMPTY
    elif delta[1] == 1:
        base_matrix[real_start_node[0] +
                    1][real_start_node[1]] = constants.EMPTY

    return base_matrix


def maze_generate(free_width, free_height, player_start_coords=(1, 1), enemies_coords=[]):
    player_start_coords = (
        player_start_coords[0]*2+1, player_start_coords[1]*2+1)
    enemies_coords = list(map(lambda coord: (
        coord[0]*2+1, coord[1]*2+1), enemies_coords))
    base_matrix = generate_base_matrix(free_width, free_height)
    visited = [[False for i in range(free_width)] for j in range(free_height)]
    current_node = (0, 0)
    visited[current_node[0]][current_node[1]] = True

    stack = [current_node]
    while len(stack) != 0:
        (cy, cx) = current_node
        neighboring_nodes = [(cy-1, cx), (cy, cx+1), (cy+1, cx), (cy, cx-1)]
        neighboring_nodes = list(filter(
            lambda node: node[0] >= 0 and node[0] < free_height
            and node[1] >= 0 and node[1] < free_width
            and not visited[node[0]][node[1]], neighboring_nodes))
        if len(neighboring_nodes) != 0:
            chosen_node = neighboring_nodes[randint(
                0, len(neighboring_nodes) - 1)]
            stack.append(chosen_node)
            visited[chosen_node[0]][chosen_node[1]] = True
            base_matrix = break_walls(base_matrix, current_node, chosen_node)
            current_node = chosen_node
        else:
            current_node = stack.pop()

    base_matrix[player_start_coords[0]
                ][player_start_coords[1]] = constants.PLAYER
    spaces = []
    for i in range(len(base_matrix)):
        for j in range(len(base_matrix[0])):
            if base_matrix[i][j] == constants.EMPTY:
                spaces.append((i, j))

    shuffle(spaces)
    real_enemies_coords = enemies_coords if len(
        enemies_coords) != 0 else spaces[1, 3]
    for coord in real_enemies_coords:
        base_matrix[coord[0]][coord[1]] = constants.ENEMY

    for i in range(5, len(spaces)):
        choice = randint(0, 100)
        if base_matrix[spaces[i][0]][spaces[i][1]] == constants.EMPTY:
            if choice >= 95:
                base_matrix[spaces[i][0]][spaces[i][1]] = constants.BIG_FOOD
            elif choice >= 40:
                base_matrix[spaces[i][0]][spaces[i][1]] = constants.SMALL_FOOD
            # break

    for i in range(1, len(base_matrix) - 1):
        for j in range(1, len(base_matrix[0]) - 1):
            if base_matrix[i][j] == 1:
                choice = randint(0, 10)
                if choice >= 5:
                    base_matrix[i][j] = constants.EMPTY

    return base_matrix
