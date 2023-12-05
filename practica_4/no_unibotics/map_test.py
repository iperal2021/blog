import numpy as np
import MAP
import GUI

def normalize_grid(grid):
    max_grid = np.max(grid)
    return np.clip(grid * 255 / max_grid, 0, 255).astype('uint8')

# Get the map image and show the car and target positions
map_img = MAP.getMap()
map_draw = GUI.showTargets()

# This is an example test grid
grid = np.zeros((MAP.MAP_HEIGHT, MAP.MAP_WIDTH))
for i in range(MAP.MAP_WIDTH):
    for j in range(MAP.MAP_HEIGHT):
        if map_img[j][i] != 0: # Only draw if this cell is not an obstacle
            grid[j][i] = i+j

# Normalize the grid to show it
grid_normalized = normalize_grid(grid)
GUI.showCost(grid_normalized, block=True)


# Create a test path and show it
plan_points_test = [
    (290, 245),
    (290, 200),
    (110, 200),
    (110, 30),
    (200, 30),
]
GUI.showPath(plan_points_test, map_draw, block=True)
