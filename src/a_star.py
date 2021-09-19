from copy import deepcopy
from wayfinders import get_neighbors
from math import e, sqrt


class Node:
    def __init__(self, coord, parent_node=None):
        self.coord = coord
        self.parent_node = parent_node
        self.g = 0
        self.h = 0
        self.f = 0


def euclidean_distance(start_coord, finish_coord):
    return sqrt((start_coord[0]-finish_coord[0])**2) + ((start_coord[1]-finish_coord[1])**2)


def get_path(finish_node):
    path = []
    current = finish_node
    while current is not None:
        path.append(current.coord)
        current = current.parent_node

    path.reverse()
    return path


def a_star(matrix, start_coord, finish_coord, enemies_coords=[]):
    start_node = Node(start_coord)
    # finish_node = Node(finish_coord)
    visited = []
    to_visit = []
    to_visit.append(start_node)
    counter = len(matrix)*len(matrix[0])

    while len(to_visit) != 0 and counter >= 0:
        counter -= 1
        # while counter != 0:
        # counter -= 1
        curr_node = to_visit[0]
        curr_index = 0
        # print(finish_coord)
        # print(list(map(lambda x: x.coord, to_visit)))
        for i in range(len(to_visit)):
            if to_visit[i].f < curr_node.f:
                curr_node = to_visit[i]
                curr_index = i

        to_visit.pop(curr_index)
        visited.append(curr_node)

        if curr_node.coord == finish_coord:
            return get_path(curr_node)

        neighboring_nodes = list(map(lambda coord: Node(coord, curr_node),
                                     get_neighbors(matrix, curr_node.coord)))

        # print(list(map(lambda x: x.coord, neighboring_nodes)))
        # print(enemies_coords)
        for neighbor in neighboring_nodes:

            if len([
                visited_neighbor
                for visited_neighbor in visited
                if visited_neighbor.coord == neighbor.coord
            ]) > 0:
                continue

            if len([
                enemy
                for enemy in enemies_coords
                if enemy == neighbor.coord
            ]) > 0:
                continue

            neighbor.g = curr_node.g + 1
            neighbor.h = euclidean_distance(neighbor.coord, finish_coord)
            neighbor.f = neighbor.g + neighbor.h

            if len([
                    to_visit_node
                    for to_visit_node in to_visit
                    if to_visit_node.coord == neighbor.coord
                    and to_visit_node.g < neighbor.g]) > 0:
                continue

            # print(neighbor.coord)
            to_visit.append(neighbor)

    return []
