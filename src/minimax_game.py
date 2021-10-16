import math
from maze_generate import maze_generate
from draws import unit_width, images
from minimax import GameState, generate_tree, minimax


[empty, wall, small_food, big_food] = images
start_matrix = list(map(lambda line: list(
    map(lambda x: int(x), line[:-1])), open("level3.txt", "r")))
# start_matrix = maze_generate(5, 5)
game_bounds = [len(start_matrix[0])*unit_width,
               len(start_matrix)*unit_width + 40]

[width, height] = game_bounds


# def play():
   


# play()
