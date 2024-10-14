import random
import pygame
from config import ROWS, COLS, CELL_SIZE, NUM_OBSTACLES

class Obstacle:
    def __init__(self, rows, cols, cell_size, num_obstacles):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.num_obstacles = num_obstacles
        self.obstacles = []  
        
    def is_invalid_pattern(self, row, col):
        patterns = [
            [(row-1, col-1), (row-1, col), (row, col-1)],  # Pattern 1
            [(row-1, col+1), (row-1, col), (row, col+1)],  # Pattern 2
            [(row+1, col-1), (row+1, col), (row, col-1)],  # Pattern 3
            [(row+1, col+1), (row+1, col), (row, col+1)],  # Pattern 4
        ]
        for pattern in patterns:
            if all(0 <= r < self.rows and 0 <= c < self.cols and (r, c) in self.obstacles for r, c in pattern):
                return True
        return False
        
    def generate_random_obstacles(self):
        self.obstacles = []
        while len(self.obstacles) < self.num_obstacles:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            new_obstacle = (row, col)

            if new_obstacle not in self.obstacles and not self.is_invalid_pattern(row, col):
                self.obstacles.append(new_obstacle)

    def draw_obstacles(self, screen):
        for obstacle in self.obstacles:
            row, col = obstacle
            rect = (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(screen, (0, 0, 0), rect)  