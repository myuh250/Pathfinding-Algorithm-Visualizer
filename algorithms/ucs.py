import heapq
from algorithms.func import reconstruct_path

def ucs(start, end, grid, obstacles):
    pq = [(0, start)]
    visited = set()
    visited.add(start)
    parent = {start: None}
    cost = {start: 0}
    steps = []

    while pq:
        current_cost, current = heapq.heappop(pq)
        steps.append(current)

        if current == end:
            break

        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + direction[0], current[1] + direction[1])

            if (0 <= neighbor[0] < len(grid) and
                0 <= neighbor[1] < len(grid[0]) and
                neighbor not in visited and
                neighbor not in obstacles):
                new_cost = current_cost + 1
                if neighbor not in cost or new_cost < cost[neighbor]:
                    cost[neighbor] = new_cost
                    heapq.heappush(pq, (new_cost, neighbor))
                    visited.add(neighbor)
                    parent[neighbor] = current

    path = reconstruct_path(parent, start, end)
    return path, steps
