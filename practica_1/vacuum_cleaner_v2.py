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

TURN_TIME_0_9 = 1
TURN_TIME_1_8 = 2
TURN_TIME_2_7 = 3
TURN_TIME_3_6 = 4
TURN_TIME_4_5 = 5

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
    number = random.randint(0, 9)
    if number >= 0 and number <= 4:
        HAL.setW(ANGULAR_VEL_R)
        if number == 0:
            my_sleep_NO_condition(TURN_TIME_0_9)
        elif number == 1:
            my_sleep_NO_condition(TURN_TIME_1_8)
        elif number == 2:
            my_sleep_NO_condition(TURN_TIME_2_7)
        elif number == 3:
            my_sleep_NO_condition(TURN_TIME_3_6)
        elif number == 4:
            my_sleep_NO_condition(TURN_TIME_4_5)
            
    elif number >= 5 and number <= 9:
        HAL.setW(ANGULAR_VEL_L)
        if number == 5:
            my_sleep_NO_condition(TURN_TIME_4_5)
        elif number == 6:
            my_sleep_NO_condition(TURN_TIME_3_6)
        elif number == 7:
            my_sleep_NO_condition(TURN_TIME_2_7)
        elif number == 8:
            my_sleep_NO_condition(TURN_TIME_1_8)
        elif number == 9:
            my_sleep_NO_condition(TURN_TIME_0_9)
        
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