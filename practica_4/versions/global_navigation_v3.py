from GUI import GUI
from HAL import HAL
from MAP import MAP
import cv2
import numpy as np
from queue import PriorityQueue

# Enter sequential code!

x=0
y=0
grid = np.zeros((400,400))

points = PriorityQueue()
expanded = []

def get_map():
  map_array = MAP.getMap('/RoboticsAcademy/exercises/static/exercises/global_navigation_newmanager/resources/images/cityLargenBin.png')
  return map_array
  
map_array = get_map()

def gridToWorld(mapcell):
    world_x=mapcell[1] * 500 / 400 - 250
    world_y=mapcell[0] * 500 / 400 - 250
    
    return(world_x,world_y)

target = None

initial_point = False
target_found = False

def normaliced(grid):
    normaliced_grid = np.where(grid == 1000)
    grid[normaliced_grid] = 0

    return grid
    

while True:
    # Enter iterative code!
    
    new_target = GUI.getTargetPose()
    target_map = MAP.rowColumn(new_target)
    
    new_target_map = tuple(MAP.rowColumn(new_target))
    carPose = MAP.rowColumn([HAL.getPose3d().x, HAL.getPose3d().y])
    targetPose = MAP.rowColumn(GUI.getTargetPose())
    path = [carPose, targetPose]
    GUI.showPath(path)
    
    x_cord, y_cord = carPose
    x, y = targetPose
    
    if not initial_point:
        points.put((0, [x, y]))
        initial_point = True
        
    if not target_found:
        next_point = points.get()
        priority, coords = next_point
        x, y = coords
        
        if coords == carPose:
            print("FIN")
            target_found = True
            print(grid)
        
        if coords not in expanded:
            expanded.append(coords)
            print("X: ", coords[0], "Y: ", coords[1])
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(map_array) and 0 <= ny < len(map_array[0]):
                    if map_array[nx][ny] != 0:
                        grid[ny][nx] = priority + 1
                        print(grid)
                        points.put((priority + 1, [nx, ny]))
                    elif map_array[nx][ny] == 0:
                        grid[ny][nx] = priority + 10
                        
            for j in range(-1, 1):
                for k in range(-1, 1):
                    if 0 <= x+j < len(map_array) and 0 <= y+k < len(map_array[0]):
                        if map_array[x+j][y+k] != 0:
                            grid[y+j][x+k] = priority+1.4
                            print(grid)
                            points.put((priority+1.4, [x+j, y+k]))
                        elif map_array[x+j][y+k] == 0:
                            grid[y+j][x+k] = priority+10
                            
    
    GUI.showNumpy(normaliced(grid))
    