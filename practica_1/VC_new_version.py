from GUI import GUI
from HAL import HAL

import random
import math
import time

LINEAR_VEL = 0
ANGULAR_VEL = 2


FORWARD_VEL = 2
ANGULAR_VEL_R = 2
ANGULAR_VEL_L = -2

OBSTACLE_DIST = 0.35

STATE = 0

timeDetection = time.time()
sideList = ['Left', 'Right']
timeList = [1, 2, 3, 5]
turnSelected = False

def parse_laser_data(laser_data):
    laser = []
    centro = 90
    rango = 40
    for i in range(centro - rango, centro + rango + 1):
        if 0 <= i < 180:  # Asegurarse de que el índice esté en el rango válido
            dist = laser_data.values[i]
            angle = math.radians(i)
            laser += [(dist, angle)]
    return laser

def distance_control(laser_data, dist):
    laser_info = parse_laser_data(laser_data)
    for distancia, _ in laser_info:
        if distancia < dist:
            HAL.setV(0)
            HAL.setW(0)
            timeDetection = time.time()
            return True
    return False
        
def random_turn():
    HAL.setV(0)  # Detener el movimiento lineal
    turnSide = random.choice(sideList)
    turnTime = random.choice(timeList)
    print (turnTime)
    
    return turnSide, turnTime
        
while True:
    
    if STATE == 0:
        laser_data = HAL.getLaserData()
        
        if distance_control(laser_data, OBSTACLE_DIST):
            LINEAR_VEL = 0
            STATE = 1
            
       
        HAL.setV(LINEAR_VEL)
        HAL.setW(ANGULAR_VEL)
        LINEAR_VEL += 0.005
        
    if STATE == 1:
        
        laser_data = HAL.getLaserData()
        if not turnSelected:
            turnSide, turnTime = random_turn()
            
            if turnSide == 'Left':
                HAL.setW(ANGULAR_VEL_L)  # Giro a la izquierda
            elif turnSide == 'Right':
                HAL.setW(ANGULAR_VEL_R)  # Giro a la derecha
            turnSelected = True
        
        if (time.time() - timeDetection) > turnTime:
            timeDetection = time.time()
            turnSelected = False
            STATE = 2
        
    if STATE == 2:
        laser_data = HAL.getLaserData()
        
        if (time.time() - timeDetection) > 3 and not distance_control(laser_data, OBSTACLE_DIST):
            timeDetection = time.time()
            STATE = 0
        
        if distance_control(laser_data, OBSTACLE_DIST):
            STATE = 1
            
        HAL.setV(FORWARD_VEL)
        HAL.setW(0)