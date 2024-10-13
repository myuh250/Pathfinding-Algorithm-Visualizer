from collections import deque

def bfs(start, end, grid, obstacles):
    queue = deque([start])
    visited = set()
    visited.add(start)
    parent = {start: None}
    steps = []  # Save all steps

    while queue:
        current = queue.popleft()
        steps.append(current)  

        if current == end:
            break

        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # (x, y) → (East, South, West, North)
            neighbor = (current[0] + direction[0], current[1] + direction[1])

            if (0 <= neighbor[0] < len(grid) and  
                0 <= neighbor[1] < len(grid[0]) and
                neighbor not in visited and
                neighbor not in obstacles):  
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    # Reconstruct the path
    path = []
    step = end
    while step is not None:
        path.append(step)
        step = parent[step]
    path.reverse()

    return path, steps  
