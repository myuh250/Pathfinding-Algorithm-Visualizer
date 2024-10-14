import heapq
from algorithms.func import reconstruct_path, heuristic

def greedy(start, end, grid, obstacles):
    pq = [(heuristic(start, end), start)]
    visited = set()
    visited.add(start)
    parent = {start: None}
    steps = []

    while pq:
        _, current = heapq.heappop(pq)
        steps.append(current)

        if current == end:
            break

        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + direction[0], current[1] + direction[1])

            if (0 <= neighbor[0] < len(grid) and
                0 <= neighbor[1] < len(grid[0]) and
                neighbor not in visited and
                neighbor not in obstacles):
                heapq.heappush(pq, (heuristic(neighbor, end), neighbor))
                visited.add(neighbor)
                parent[neighbor] = current

    path = reconstruct_path(parent, start, end)
    return path, steps
