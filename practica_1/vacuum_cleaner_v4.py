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

def parse_laser_data(laser_data):
    laser = []
    centro = 90
    rango = 45
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
            return True
    return False
    

def my_sleep(segundos):
    tiempo_inicial = time.time()
    while True:
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - tiempo_inicial
        if tiempo_transcurrido >= segundos:
            break 
        
def random_turn():
    HAL.setV(0)  # Detener el movimiento lineal
    
    number = random.randint(0, 9)
    if number % 2 == 0:
        HAL.setW(ANGULAR_VEL_R)  # Giro a la derecha
    else:
        HAL.setW(ANGULAR_VEL_L)  # Giro a la izquierda
    
    if number == 0 or number == 9:
        time_to_turn = 3
    elif number == 1 or number == 8:
        time_to_turn = 2
    elif number == 2 or number == 7:
        time_to_turn = 1.5
    elif number == 3 or number == 6:
        time_to_turn = 1
    else:
        time_to_turn = 0.5
    my_sleep(time_to_turn)
        
        
while True:
    
    if STATE == 0:
        laser_data = HAL.getLaserData()
        
        if distance_control(laser_data, OBSTACLE_DIST):
            STATE = 1
            
       
        HAL.setV(LINEAR_VEL)
        HAL.setW(ANGULAR_VEL)
        LINEAR_VEL += 0.005
        
    if STATE == 1:
        
        laser_data = HAL.getLaserData()
            
        random_turn()
        STATE = 2
        
    if STATE == 2:
        laser_data = HAL.getLaserData()
        
        if distance_control(laser_data, OBSTACLE_DIST):
            STATE = 1
            
        HAL.setV(FORWARD_VEL)
        HAL.setW(0)