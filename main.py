from config import *
from map.window import Grid
# from map.obstacles import Obstacle

if __name__ == "__main__":
    window = Grid(ROWS, COLS, CELL_SIZE, NUM_OBSTACLES)
    window.run()