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
expanded = set()

def get_map():
  map_array = MAP.getMap('/RoboticsAcademy/exercises/static/exercises/global_navigation_newmanager/resources/images/cityLargenBin.png')
  return map_array
  
map_array = get_map()

def gridToWorld(mapcell):
    world_x=mapcell[1] * 500 / 400 - 250
    world_y=mapcell[0] * 500 / 400 - 250
    
    return(world_x,world_y)

def distance_heuristic(pos1, pos2):
    return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

target = None

initial_point = False
target_found = False

def normalized(grid):
    normaliced_grid = np.where(grid == 1000)
    grid[normaliced_grid] = 0

    return grid
    
counter = 0
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
            print(counter)
            print("FIN")
            target_found = True

        if (x,y) not in expanded:
            counter += 1
            expanded.add((x, y))
            print("X: ", coords[0], "Y: ", coords[1])
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(map_array) and 0 <= ny < len(map_array[0]):
                    if map_array[nx][ny] != 0 and (nx, ny) not in expanded:
                        heuristic = distance_heuristic((nx, ny), targetPose)
                        cost = heuristic + priority + 1
                        grid[ny][nx] = cost
                        points.put((cost, [nx, ny]))
                    elif map_array[nx][ny] == 0 and (nx, ny) not in expanded:
                        grid[ny][nx] = priority + 1000

            for j in range(-1, 1):
                for k in range(-1, 1):
                    if 0 <= x+j < len(map_array) and 0 <= y+k < len(map_array[0]):
                        if map_array[x+j][y+k] != 0 and (x+j, y+k) not in expanded:
                            heuristic = distance_heuristic((x+j, y+k), targetPose)
                            cost = heuristic + priority + 1.4
                            grid[y+j][x+k] = cost

                            points.put((cost, [x+j, y+k]))
                        elif map_array[x+j][y+k] == 0 and (x+j, y+k) not in expanded:
                            grid[y+j][x+k] = priority + 1000

                    
    if target_found:
      
        GUI.showNumpy(normalized(grid))
    