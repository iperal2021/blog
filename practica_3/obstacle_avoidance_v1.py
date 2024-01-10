from GUI import GUI
from HAL import HAL
import math
import time
import numpy as np
# Enter sequential code!

# Current target
target = [1.0, 1.0]
GUI.showLocalTarget(target)

x_var = 1.3
y_var = 10
vel_adj = 1.2

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

def parse_laser_data(laser_data):
    laser = []
    i = 0
  
    for i, dist in enumerate(laser_data.values):
        if dist > 10:
            dist = 10
        angle = math.radians(i-90) # because the front of the robot is -90 degrees
        laser += [(dist, angle)]
        i+=1
    return laser

def get_repulsive_force(parse_laser):
    laser = parse_laser
    
    laser_vectorized = []
    for dist, angle in laser:
      
        x = 1/dist * math.cos(angle) * -1
        y = 1/dist * math.sin(angle) * -1

        v = (x,y)
        laser_vectorized += [v]
    laser_mean = np.mean(laser_vectorized, axis=0)
    return laser_mean

while True:
    # Enter iterative code!
    image = HAL.getImage()
    laser_data = HAL.getLaserData()
    laser = parse_laser_data(laser_data)

    currentTarget = GUI.map.getNextTarget()  
    GUI.map.targetx = currentTarget.getPose().x
    GUI.map.targety = currentTarget.getPose().y

    target_abs_x = currentTarget.getPose().x
    target_abs_y = currentTarget.getPose().y

    robotx = HAL.getPose3d().x
    roboty = HAL.getPose3d().y
    robott = HAL.getPose3d().yaw

    absolute_taget = target_abs_x, target_abs_y
    
    target_rel_x, target_rel_y = absolute2relative(absolute_taget[0], absolute_taget[1], robotx, roboty, robott)

    relative_target = target_rel_x, target_rel_y

    # Car direction  (green line in the image below)
    carForce = [max(min(target_rel_x, 3.5), -3.5), max(min(target_rel_y, 3.2), -3.2)]
    # Obstacles direction (red line in the image below)
    obsForce = [get_repulsive_force(laser)[0]*x_var, get_repulsive_force(laser)[1]*y_var]
    # Average direction (black line in the image below)
    avgForce = [(carForce[0]+obsForce[0])* vel_adj, (carForce[1] + obsForce[1])]

    #distance2objetive = distance(relative_target[0], relative_target[1])

    arctan = math.atan(avgForce[1]/avgForce[0])

    print("Tangente:", arctan)
    #print("Distancia al punto", distance2objetive)
    print("velocidad linear: ", abs(avgForce[0]))
    
    GUI.showLocalTarget(relative_target)

    GUI.showForces(carForce, obsForce, avgForce)

    if (target_rel_x < 1.3 and target_rel_y < 1.3):
        currentTarget.setReached(True)
  
    #distance_to_obstacle = min([dist for dist, angle in laser])
    
    HAL.setW(arctan)
    HAL.setV(abs(avgForce[0]))

    GUI.showImage(image)