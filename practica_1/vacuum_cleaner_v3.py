from GUI import GUI
from HAL import HAL

import random
import math
import time

INITIAL_RADIUS = 0.10
RADIUS_INCREMENT = 0.30

LINEAR_VEL = 1.25
ANGULAR_VEL = LINEAR_VEL / INITIAL_RADIUS

ANGULAR_VEL_R = 0.70
ANGULAR_VEL_L = -0.70

OBSTACLE_DIST = 0.30

STATE = 0

def parse_laser_data(laser_data):
    laser = []
    for i in range(180):
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
            return True
    return False
# Sleep with condition to break it
def my_sleep(segundos, condition):
    tiempo_inicial = time.time()
    while True:
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - tiempo_inicial
        if tiempo_transcurrido >= segundos:
            break 
        elif condition:
            break

def my_sleep_NO_condition(segundos):
    tiempo_inicial = time.time()
    while True:
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - tiempo_inicial
        if tiempo_transcurrido >= segundos:
            break 
        
def random_turn():
    HAL.setV(0)  # Detener el movimiento lineal
    while True:
        number = random.randint(0, 9)
        if number % 2 == 0:
            HAL.setW(0.2)  # Giro a la derecha
        else:
            HAL.setW(-0.2)  # Giro a la izquierda
        
        if number == 0 or number == 9:
            time_to_turn = 5
        elif number == 1 or number == 8:
            time_to_turn = 4
        elif number == 2 or number == 7:
            time_to_turn = 3
        elif number == 3 or number == 6:
            time_to_turn = 2
        else:
            time_to_turn = 1
        my_sleep_NO_condition(time_to_turn)
        break
        
while True:
    
    if STATE == 0:
        laser_data = HAL.getLaserData()
        
        if distance_control(laser_data, OBSTACLE_DIST):
            STATE = 1
            
       
        HAL.setV(LINEAR_VEL)
        HAL.setW(ANGULAR_VEL)
        
        INITIAL_RADIUS += RADIUS_INCREMENT
        ANGULAR_VEL = LINEAR_VEL / INITIAL_RADIUS
        
        #lap_time = 2 * math.pi * INITIAL_RADIUS / LINEAR_VEL
        #my_sleep(lap_time, distance_control(laser_data, 0.4))
        
    if STATE == 1:
        
        laser_data = HAL.getLaserData()
            
        random_turn()
        state = 2
        
    if STATE == 2:
        laser_data = HAL.getLaserData()
        
        if distance_control(laser_data, OBSTACLE_DIST):
            STATE = 1
            
        HAL.setV(LINEAR_VEL)
        HAL.setW(0)