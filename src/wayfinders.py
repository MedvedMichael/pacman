import time


def bfs(matrix, start_coord, finish_coord):
    start_time = time.time()
    queue = [start_coord]
    parents = {start_coord: None}
    while len(queue) != 0:
        current_coord = queue.pop(0)
        if current_coord == finish_coord:
            print(time.time() - start_time)
            return get_path(parents, finish_coord)

        (cy, cx) = current_coord
        neighboring_nodes = [(cy-1, cx), (cy, cx+1), (cy+1, cx), (cy, cx-1)]

        neighboring_nodes = list(filter(
            lambda node: matrix[node[0]][node[1]] != 1 and node[0] >= 0 and node[0] < len(
                matrix) and node[1] >= 0 and node[1] < len(matrix[0]),
            neighboring_nodes
        ))

        for node in neighboring_nodes:
            if node not in parents:
                parents[node] = current_coord
                queue.append(node)



def get_path(parents, finish_coord):
    arr = []
    current = finish_coord
    while current != None:
        arr.insert(0, current)
        current = parents[current]

    return arr


def dfs(matrix, start_coord, finish_coord):
    start_time = time.time()
    stack = [start_coord]
    result = [start_coord]
    visited = [[False for i in range(len(matrix[0]))]
               for j in range(len(matrix))]
    visited[start_coord[0]][start_coord[1]] = True

    
    while len(stack) != 0:
        current_coord = stack[-1]
        result.append(current_coord)
        if current_coord == finish_coord:
            print(time.time() - start_time)
            return stack
        (cy, cx) = current_coord
        visited[cy][cx] = True
        neighboring_nodes = [(cy-1, cx), (cy, cx+1), (cy+1, cx), (cy, cx-1)]

        neighboring_nodes = list(filter(
            lambda node: not visited[node[0]][node[1]] and matrix[node[0]][node[1]] != 1 and node[0] >= 0 and node[0] < len(
                matrix) and node[1] >= 0 and node[1] < len(matrix[0]),
            neighboring_nodes
        ))
        # See for changes
        # neighboring_nodes.reverse()
        stack.extend(neighboring_nodes)
        
        if len(neighboring_nodes) == 0:
            stack.pop()
            result.pop()
