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
        
    def generate_random_obstacles(self):
        self.obstacles = []
        for _ in range(self.num_obstacles):
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            self.obstacles.append((row, col))

    def draw_obstacles(self, screen):
        for obstacle in self.obstacles:
            row, col = obstacle
            rect = (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(screen, (0, 0, 0), rect)  