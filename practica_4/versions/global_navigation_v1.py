from GUI import GUI
from HAL import HAL
from MAP import MAP
import cv2
import numpy as np
from queue import PriorityQueue
# Enter sequential code!


x_cord = 0
y_cord = 0
x = 0
y = 0 

up = (x_cord, y_cord-1)
down = (x_cord, y_cord+1)
rigth = (x_cord+1, y_cord)
left = (x_cord-1, y_cord)

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

def get_grid(x, y, carPose):
    points.put(0, x, y)
    

    while not points.empty():
        next_point = points.get()
        priority, x, y = next_point
        grid[y, x] = priority
        if x >=  0 and x <= 400 and next_point not in expanded:
            if y >=  0 and y <= 400: 
                
                if (x == carPose[0] and y == carPose[1]):

                    return grid
                expanded.append(next_point)
                
                for j in range(-1, 1):
                    for k in range(-1, 1):
                        if (map_array[x+j][y+k] != 0):
                            points.put(priority+1.4, x+j, y+k)
                
                for i in range(-1, 1):
                    if (map_array[x][y+i] != 0):
                            points.put(priority+1, x, y+i)
                    if (map_array[x+i][y] != 0):
                            points.put(priority+1, x+i, y)

while True:
    # Enter iterative code!
    new_target = GUI.getTargetPose()
    target_map = MAP.rowColumn(new_target)
    
    new_target_map = tuple(MAP.rowColumn(new_target))
    carPose = MAP.rowColumn([HAL.getPose3d().x, HAL.getPose3d().y])
    targetPose = MAP.rowColumn(GUI.getTargetPose())
    path = [carPose, targetPose]
    GUI.showPath(path)
    
    x, y = targetPose
    grid = get_grid(x, y, carPose)
    