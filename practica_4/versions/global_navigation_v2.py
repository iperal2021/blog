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

target_found = False
  
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
    
    points.put((0, [x, y]))
    
    for i in range(10):
        if not target_found:
            next_point = points.get()
            print(next_point)
            print("carPose: ", carPose)
            if (next_point == carPose):
                print("FIN")
                target_found = True
            priority, coords = next_point
            x,y = coords
            grid[y, x] = priority
            print("X: ", x_cord, " Y: ", y_cord)
            print("Expanded: ",expanded)
            if x_cord >=  0 and x_cord <= 400 and next_point not in expanded:
                print("Primer sub-if")
                if y_cord >=  0 and y_cord <= 400: 
                    
                    print("vecinos")
                    expanded.append(next_point)
                    if (map_array[x][y+1] != 0):
                        print("1 ", map_array[x][y+1])
                        grid[y+1][x] = priority+1
                        points.put((priority+1, [x, y+1]))
                    elif ( map_array[x-1][y] == 0):
                          grid[y+1][x] = priority+10      
                        
                    if (map_array[x][y-1] != 0):
                        print("2", map_array[x][y-1])
                        grid[y-1][x] = priority+1
                        points.put((priority+1, [x, y-1]))
                    elif ( map_array[x-1][y] == 0):
                          grid[y-1][x] = priority+10    
                        
                    if (map_array[x+1][y] != 0):
                        print("3", map_array[x+1][y])
                        grid[y][x+1] = priority+1
                        points.put((priority+1, [x+1, y]))
                    elif ( map_array[x+1][y] == 0):
                          grid[y][x+1] = priority+10    
                        
                    if (map_array[x-1][y] != 0):
                        print("4", map_array[x-1][y])
                        grid[y][x-1] = priority+1
                        points.put((priority+1, [x-1, y]))
                    elif ( map_array[x-1][y] == 0):
                          grid[y][x-1] = priority+1000
                    
                    for j in range(-1, 1):
                        for k in range(-1, 1):
                            if (map_array[x+j][y+k] != 0):
                                grid[y+j][x+k] = priority+1.4
                                points.put((priority+1.4, [x+j, y+k]))
                            elif ( map_array[y+k][x+j] == 0):
                                grid[y+j][x+k] = priority+1000
               
    GUI.showNumpy(grid)