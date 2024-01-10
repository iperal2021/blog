from GUI import GUI
from HAL import HAL
from MAP import MAP
import numpy as np
from queue import PriorityQueue
import math

# Enter sequential code!

points = PriorityQueue()
expanded = set()
carPose = MAP.rowColumn([HAL.getPose3d().x, HAL.getPose3d().y])
targetPose = MAP.rowColumn(GUI.getTargetPose())

initial_point = False
target_found = False
isGradient = False
goal_reached = False
target_reached = False

# Get the image of the mapzz
def get_map():
  map_array = MAP.getMap('/RoboticsAcademy/exercises/static/exercises/global_navigation_newmanager/resources/images/cityLargenBin.png')
  return map_array
  
map_array = get_map()

grid = np.zeros_like(map_array)

# Turn the grid coordinate into gazebo world coordinates
def gridToWorld(mapcell):
    world_x=mapcell[1] * 500 / 400 - 250
    world_y=mapcell[0] * 500 / 400 - 250
    
    return(world_x,world_y)


def normalized(grid):
    normaliced_grid = np.where(grid == 1000)
    grid[normaliced_grid] = 0

    return grid


# Create a gradient of the map whit start point in targetPose and finish point in carPose
def gradient(x, y, carPose, target_found, initial_point):
    counter = 0
    
    # Until it reach caPose the gradient is generated
    while not target_found:
        # the first point is added to points
        if not initial_point:
            points.put((0, [x, y]))
            initial_point = True
        
        # Have to take the first coordinate
        next_point = points.get()
        priority, coords = next_point # taken priority (weight) and coordinates
        x, y = coords
        
        # if coords are carPose cords, the grid is finished
        if coords == carPose:
            print(counter)
            print("FIN")
            print(grid[targetPose[0],targetPose[1]])
            target_found = True
            break
        
        # if the coord isn't visited it's expanded
        if (x, y) not in expanded:
            counter += 1
            expanded.add((x, y)) # added to visited coords list
            print("X: ", x, "Y: ", y)
            
            # coordinates up, down, left and right
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            
            # weights or priorities
            cost_cross = priority + 1
            cost_x = priority + 1.4
            
            # added to the grid and the points queue the horizontal and vertical coords
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 400 and 0 <= ny < 400:
                    if map_array[ny][nx] != 0 and (nx, ny) not in expanded:
                        grid[ny][nx] = cost_cross
                        points.put((cost_cross, [nx, ny]))
                    elif map_array[ny][nx] == 0 and (nx, ny) not in expanded:
                        grid[ny][nx] = 1000
            
            # added the diagonal coordinates
            for j in range(-1, 1):
                for k in range(-1, 1):
                    if 0 <= x + j < 400 and 0 <= y + k < 400:
                        if map_array[y + k][x + j] != 0 and (x + j, y + k) not in expanded:
                            grid[y + k][x + j] = cost_x
                            points.put((cost_x, [x + j, y + k]))
                        elif map_array[y + k][x + j] == 0 and (x + j, y + k) not in expanded:
                            grid[y + k][x + j] = 1000
                            
def absolute2relative (x_abs, y_abs, robotx, roboty, robott):

    # robotx, roboty are the absolute coordinates of the robot
    # robott is its absolute orientation
    # Convert to relatives
    dx = x_abs - robotx
    dy = y_abs - roboty

    # Rotate with current angle
    x_rel = dx * math.cos (-robott) - dy * math.sin (-robott)
    y_rel = dx * math.sin (-robott) + dy * math.cos (-robott)

    return x_rel, y_rel

def getCarForces(grid, targetPose):
  
    while not target_reached:
        carPose = MAP.rowColumn([HAL.getPose3d().x, HAL.getPose3d().y])
        robotx = HAL.getPose3d().x
        roboty = HAL.getPose3d().y
        robott = HAL.getPose3d().yaw
        
        weight = 1000
        for i in range(-1,2):
            for j in range(-1,2):
                current_weight = grid[carPose[0] + i][carPose[1] + j]
                if current_weight < weight and current_weight != 0:
                    weight = current_weight
                    
                    irl_coord = gridToWorld([carPose[0]+i, carPose[1]+j])
            
            target_rel_x, target_rel_y = absolute2relative(irl_coord[1], irl_coord[0], robotx, roboty, robott)
            carForce = [target_rel_x, target_rel_y]
            
            HAL.setV(carForce[0])
            HAL.setW(carForce[1])

        
while True:
    # Enter iterative code!

    new_target = GUI.getTargetPose()
    target_map = MAP.rowColumn(new_target)

    new_target_map = tuple(MAP.rowColumn(new_target))
    path = [carPose, targetPose]
    GUI.showPath(path)

    # convert carPose and targetPose into x, y variables
    if not goal_reached:
        x_cord, y_cord = carPose
        x, y = targetPose
        

        # The gradient is created
        if not isGradient:
            gradient(x, y, carPose, target_found, initial_point)

            GUI.showNumpy(grid)
            isGradient = True
        
        getCarForces(grid, targetPose)
        carPose = MAP.rowColumn([HAL.getPose3d().x, HAL.getPose3d().y])
