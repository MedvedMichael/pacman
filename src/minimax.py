import math
import random
from typing import List
from copy import deepcopy
from a_star import a_star
import constants

from wayfinders import bfs, dfs, get_neighbors


class GameState:
    def __init__(self, matrix, is_pacman_angry=False, score=0) -> None:
        self.matrix = matrix
        self.score = score
        self.is_pacman_angry = is_pacman_angry

    def __str__(self) -> str:
        return '\n'.join([str(line) for line in self.matrix]) \

    def get_pacman_position(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j] == constants.PLAYER:
                    return (i, j)

    def get_enemies_positions(self):
        coords = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j] == constants.ENEMY:
                    coords.append((i, j))
        return coords

    def change_character_position(self, coord, new_coord, new_value_on_last_coord):
        new_matrix = deepcopy(self.matrix)
        character_number = new_matrix[coord[0]][coord[1]]
        new_coord_value = new_matrix[new_coord[0]][new_coord[1]]
        new_matrix[coord[0]][coord[1]] = new_value_on_last_coord
        new_matrix[new_coord[0]][new_coord[1]] = character_number
        new_score = self.score
        new_angry = self.is_pacman_angry
        if character_number == constants.PLAYER:
            if new_coord_value == constants.SMALL_FOOD:
                new_score += 10
            elif new_coord_value == constants.BIG_FOOD:
                new_angry = True
        state = GameState(new_matrix, new_angry, new_score)
        return state


class Node:
    def __init__(self, state: GameState, value) -> None:
        self.state = state
        self.value = value
        self.children: list[Node] = []

    def __str__(self) -> str:
        output = str(self.state) + " \nValue: " + str(self.value) + "\n"
        strings = '\n'.join(map(lambda x: '\n'.join(map(lambda y: " " + y,str(x).split('\n'))), self.children))
        output += '{\n' + strings + '}\n' if strings != '' else ''
        return output

    def count(self, counter):
        counter += 1
        for child in self.children:
            counter = child.count(counter)
        return counter


def evaluate(node: Node, target):
    delta = math.inf
    pacman_coord = node.state.get_pacman_position()
    if target == pacman_coord:
        return -math.inf
    enemies_coords = node.state.get_enemies_positions()

    for enemy in enemies_coords:
        # distance = math.sqrt(math.pow(
        #     enemy[0] - pacman_coord[0], 2) + math.pow(enemy[1] - pacman_coord[1], 2))
        distance = len(a_star(node.state.matrix, pacman_coord, enemy))
        if delta is None or delta > distance:
            delta = distance

    # target_distance = math.sqrt(math.pow(
    #     target[0] - pacman_coord[0], 2) + math.pow(target[1] - pacman_coord[1], 2))
    # delta = len(dfs(node.state.matrix, pacman_coord, target))
    target_distance = len(a_star(node.state.matrix, pacman_coord, target))
    output = -(target_distance + 0.1*delta)

    return output


def generate_tree(start_state: GameState, target, depth=2):
    start_node = Node(start_state, None)
    generate_tree_recurs(start_node, depth, start_state.matrix, target)
    return start_node


def generate_tree_recurs(curr_node: Node, depth, start_matrix, target):
    if depth <= 0:
        curr_node.value = evaluate(curr_node, target)
        return None
    curr_state = curr_node.state
    pacman_coord = curr_state.get_pacman_position()
    enemies_coords = curr_state.get_enemies_positions()
    if depth % 2 == 0:
        # print(pacman_coord)
        neighboring_nodes = list(filter(
            lambda x: not curr_state.is_pacman_angry and x not in enemies_coords, get_neighbors(curr_state.matrix, pacman_coord)))

        new_nodes = list(map(lambda node: Node(curr_state.change_character_position(
            pacman_coord, node, constants.EMPTY), None), neighboring_nodes))

        curr_node.children = new_nodes

    else:
        neighboring_nodes = [get_neighbors(
            curr_state.matrix, coord) for coord in enemies_coords]

        variations = get_variations(neighboring_nodes)
        new_nodes = []
        for variant in variations:
            if pacman_coord in variant:
                continue
            state = curr_state
            for i in range(len(enemies_coords)):
                state = state.change_character_position(
                    enemies_coords[i], variant[i], constants.EMPTY)

            new_nodes.append(Node(state, None))
        curr_node.children = new_nodes
    for child in curr_node.children:
        generate_tree_recurs(child, depth-1, start_matrix, target)


def get_variations(arr):
    result = []

    def get_variations_recurs(last_arr, res):
        if len(last_arr) == 0:
            result.append(res)
            return
        curr_arr = last_arr[0]
        for item in curr_arr:
            get_variations_recurs(last_arr[1:], res + [item])
    get_variations_recurs(arr, [])
    return result

    # new_states = map(lambda node: Node(curr_state.change_character_position(
    #     pacman_coord, node, 0), None), neighboring_nodes)


def minimax(curr_node: Node, alpha, beta, depth):
    is_max = depth % 2 == 0
    if len(curr_node.children) == 0:
        # print(curr_node.value)
        return curr_node.value

    if is_max:
        best_value = -math.inf
        for child in curr_node.children:
            value = minimax(child, alpha, beta, depth+1)
            best_value = max(
                best_value, value) if value is not None else best_value
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        curr_node.value = best_value
        return best_value

    else:
        best_value = math.inf
        for child in curr_node.children:
            value = minimax(child, alpha, beta, depth+1)
            best_value = min(
                best_value, value) if value is not None else best_value
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        curr_node.value = best_value
        return best_value


def expectimax(curr_node: Node, depth):
    is_max = depth % 2 == 0
    if len(curr_node.children) == 0:
        # print(curr_node.value)
        return curr_node.value

    if is_max:
        best_value = -math.inf
        for child in curr_node.children:
            value = expectimax(child, depth+1)
            best_value = max(
                best_value, value) if value is not None else best_value
        curr_node.value = best_value
        return best_value

    else:
        values = 0
        for child in curr_node.children:
            value = expectimax(child, depth+1)
            values += value if value is not None else 0
        curr_node.value = values / len(curr_node.children)
        return curr_node.value
