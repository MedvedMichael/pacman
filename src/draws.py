import pygame
from pygame import image
unit_width = 24

EMPTY = 0
WALL = 1
SMALL_FOOD = 2
BIG_FOOD = 3


paths = ['./assets/empty.png', './assets/wall2.png',
         './assets/food_small.png', './assets/food_big.png']
images = list(map(lambda x: pygame.transform.scale(
    image.load(x), (unit_width, unit_width)), paths))

def draw_unit(window, number, coords):
    window.blit(images[number], coords)