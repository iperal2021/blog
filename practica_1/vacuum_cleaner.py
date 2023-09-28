from GUI import GUI
from HAL import HAL

import random, math, time

INITIAL_RADIUS = 0.10
RADIUS_INCREMENT = 0.30

#SPIRAL_VEL_LINEAR = 1.00
SPIRAL_VEL_ANGULAR = 1.50

#SPIRAL_VEL_ANGULAR = SPIRAL_VEL_LINEAR / INITIAL_RADIUS
SPIRAL_VEL_LINEAR = SPIRAL_VEL_ANGULAR * INITIAL_RADIUS

FORWARD_VEL = 1.00
BACKWARDS_VEL = -0.25

ANGULAR_VEL_R = 0.70
ANGULAR_VEL_L = -0.70

TURN_TIME_0_9 = 1
TURN_TIME_1_8 = 2
TURN_TIME_2_7 = 3
TURN_TIME_3_6 = 4
TURN_TIME_4_5 = 5

OBSTACLE_DIST = 0.35

state = 0

# Enter sequential code!

def parse_laser_data(laser_data):
    laser = []
    centro = 90 
    rango = 60
    for i in range(centro - rango, centro + rango + 1):
        if 0 <= i < 180:  # Me aseguro de que el índice esté en el rango válido
            dist = laser_data.values[i]
            angle = math.radians(i)
            laser += [(dist, angle)]
    return laser

# Condition of distance to stop the robot
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
     
# random choice of the direction and time of the turn      
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
    # Enter iterative code!
    if state == 0:
      
        laser_data = HAL.getLaserData()
    
        if distance_control(laser_data, OBSTACLE_DISTANCE):
            state = 1
    
        HAL.setV(SPIRAL_VEL_LINEAR)
        HAL.setW(SPIRAL_VEL_ANGULAR)
        INITIAL_RADIUS += RADIUS_INCREMENT
        
        #SPIRAL_VEL_ANGULAR = SPIRAL_VEL_LINEAR / INITIAL_RADIUS
        SPIRAL_VEL_LINEAR = SPIRAL_VEL_ANGULAR * INITIAL_RADIUS

        lap_time = 2 * math.pi * INITIAL_RADIUS / SPIRAL_VEL_LINEAR
            
        my_sleep(lap_time, distance_control(laser_data, OBSTACLE_DIST))
  
    if state == 1:
      
        laser_data = HAL.getLaserData()
        if distance_control(laser_data, OBSTACLE_DIST):
            state = 1
        else:
            state = 2
        random_turn()
       
    if state == 2:
      
        laser_data = HAL.getLaserData()
        if distance_control(laser_data, OB):
            state = 1
        HAL.setV(FORWARD_VEL)
        HAL.setW(0)
