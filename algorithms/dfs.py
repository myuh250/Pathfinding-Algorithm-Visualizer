from collections import deque
from algorithms.func import reconstruct_path

def dfs(start, end, grid, obstacles):
    stack = deque([start])  
    visited = set()
    visited.add(start)
    parent = {start: None}
    steps = []  

    while stack:
        current = stack.pop()  
        steps.append(current)  

        if current == end:
            break

        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + direction[0], current[1] + direction[1])

            if (0 <= neighbor[0] < len(grid) and  
                0 <= neighbor[1] < len(grid[0]) and
                neighbor not in visited and
                neighbor not in obstacles):  
                stack.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    path = reconstruct_path(parent, start, end)

    return path, steps