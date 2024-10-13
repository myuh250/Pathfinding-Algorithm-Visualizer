import pygame
import random
from config import ROWS, COLS, CELL_SIZE, NUM_OBSTACLES
from map.obstacles import Obstacle
from algorithms.bfs import bfs

class Button:
    def __init__(self, text, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = (200, 200, 200)
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Grid:
    def __init__(self, rows, cols, cell_size, num_obstacles):
        # Initialize grid
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.width = cols * cell_size + 200
        self.height = rows * cell_size
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]  
        
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Grid Map")
        
        # Obstacles
        self.obstacle = Obstacle(rows, cols, cell_size, num_obstacles)
        self.obstacle.generate_random_obstacles()
        
        # Start and end points
        self.start_point = None
        self.end_point = None
        self.visited_cells = []
        
        # Buttons
        self.reset_button = Button("Reset", self.width - 180, 20, 150, 50)
        self.start_button = Button("Start", self.width - 180, 90, 150, 50)
        self.algorithm_button = Button("Algorithm", self.width - 180, 160, 150, 50)
        
        # Dropdown menu
        self.selected_algorithm = None
        self.dropdown_open = False
        self.algorithms = ["BFS", "DFS", "UCS", "Greedy", "A*"]

    def draw(self):
        for row in range(self.rows):
            for col in range(self.cols):
                rect = (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)  
                
        self.obstacle.draw_obstacles(self.screen)
        
        # Start and end points
        if self.start_point:
            row, col = self.start_point
            start_rect = (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, (0, 255, 0), start_rect)  # Green color for start point

        if self.end_point:
            row, col = self.end_point
            end_rect = (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, (255, 0, 0), end_rect)  # Red color for end point
            
        # Draw buttons
        self.reset_button.draw(self.screen)
        self.start_button.draw(self.screen)
        self.algorithm_button.draw(self.screen)
        self.draw_dropdown()
        
    def draw_dropdown(self):
        if self.dropdown_open:
            dropdown_rect = pygame.Rect(self.width - 180, 210, 150, 40 * len(self.algorithms))  # Update Y position
            pygame.draw.rect(self.screen, (255, 255, 255), dropdown_rect)  

            for i, algorithm in enumerate(self.algorithms):
                button_rect = pygame.Rect(self.width - 180, 210 + i * 40, 150, 40)  # Update Y position
                pygame.draw.rect(self.screen, (200, 200, 200), button_rect)  
                self.draw_text(algorithm, button_rect)  
                
                if button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    self.selected_algorithm = algorithm
                    self.algorithm_button.text = algorithm
                    self.dropdown_open = False
            
    def draw_text(self, text, rect):
        font = pygame.font.Font(None, 24)
        text_surface = font.render(text, True, (0, 0, 0))
        self.screen.blit(text_surface, (rect.x + 10, rect.y + 10))

    def draw_path(self, path):
        for (row, col) in path:
            rect = (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, (146, 120, 232), rect)  # Màu sắc của đường đi
        pygame.display.flip()
        
    def simulate_steps(self, steps):
        start_row, start_col = self.start_point
        for step in steps:
            row, col = step
            if (row, col) != (start_row, start_col):
                rect = (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (190, 245, 245), rect)  

            pygame.display.flip()  
            # CHANGE SPEED HERE
            pygame.time.delay(10) 
        self.pathfinding_complete = True

    def update(self):
        self.screen.fill((230, 230, 211))
        self.draw()
        pygame.display.flip()  
        
    def is_click_on_obstacle(self, pos):
        x, y = pos
        col = x // self.cell_size
        row = y // self.cell_size
        return (row, col) in self.obstacle.obstacles
        
    def handle_click(self, pos):
        # Get the row and column of the clicked cell
        col = pos[0] // self.cell_size
        row = pos[1] // self.cell_size
        
        # Check if the clicked cell is within the grid
        if 0 <= col < self.cols and 0 <= row < self.rows:
            if not self.is_click_on_obstacle(pos):
                if self.start_point == (row, col):
                    self.start_point = None 
                elif self.end_point == (row, col):
                    self.end_point = None 
                elif not self.start_point:
                    self.start_point = (row, col) 
                elif not self.end_point:
                    self.end_point = (row, col)  
                
        # Check if any button is clicked
        if self.reset_button.is_clicked(pos):
            self.reset_map()  
        elif self.start_button.is_clicked(pos):
            self.start_algorithm()  
        elif self.algorithm_button.is_clicked(pos):
            self.select_algorithm()  
            
    def reset_map(self):
        self.start_point = None
        self.end_point = None
        self.obstacle.generate_random_obstacles()
        self.pathfinding_complete = False
        
    def start_algorithm(self):
        algorithms = {
            "BFS": bfs,
            # "DFS": dfs,
            # "UCS": ucs,
            # "Greedy": greedy,
            # "A*": astar
        }

        if self.start_point and self.end_point:
            algorithm_function = algorithms.get(self.selected_algorithm)
            if algorithm_function:
                path, steps = algorithm_function(self.start_point, self.end_point, self.grid, self.obstacle.obstacles)
                self.simulate_steps(steps)
                self.draw_path(path)
                self.wait_for_exit()
                
    def wait_for_exit(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.reset_button.is_clicked(event.pos):
                            waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  
                        waiting = False

    def select_algorithm(self):
        self.dropdown_open = not self.dropdown_open

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.pathfinding_complete:
                        running = False

            self.update()
            clock.tick(60)  # 60 FPS
