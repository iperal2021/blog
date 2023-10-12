from GUI import GUI
from HAL import HAL

import time
import cv2
import numpy as np
# Enter sequential code!

# VEL variables
linear_vel = 4.0
max_angular_vel = 1.0
# PID variables
Kp = 0.005
Kd = 0.000015
Ki = 0.000001

sum_error = 0.0
prev_error = 0.0
prev_time = 0
prev_sum_error = 0.0

image_center = (0.0, 0.0)

def image_mask(image_hsv):
    corte = image_hsv[245:460, 0:image_hsv.shape[1]]
    lower1 = np.array([0, 50, 50])
    upper1 = np.array([10, 255, 255])
    
    lower2 = np.array([170,50,500])
    upper2 = np.array([179,255,255])
    
    mask1 = cv2.inRange(corte, lower1, upper1)
    mask2 = cv2.inRange(corte, lower2, upper2)
    
    mask = mask1 + mask2
    output = cv2.bitwise_and(corte, corte, mask = mask)
    # convert the input image to grayscale
    gray_img = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    
    # apply thresholding to convert grayscale to binary image
    ret,thresh = cv2.threshold(gray_img,70,255,0,cv2.THRESH_BINARY)
    contour, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in contour:
        M = cv2.moments(c)
        print()
        if M["m00"] != 0:
           cx = int(M["m10"] / M["m00"])
           cy = int(M["m01"] / M["m00"])
        else:
           cx, cy = 0, 0
        
        cv2.circle(output, (cx, cy), 5, (255, 255, 255), -1)
        cv2.putText(output, 'centroid', (cx - 25, cy - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    GUI.showImage(output)
    return cx 

while True:
    image = HAL.getImage()
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    
    height = image_hsv.shape[0]
    width = image_hsv.shape[1]
    image_center = (width/2, height/2)

    copyImage = image_hsv.copy()
    cX = image_mask(copyImage)
    # Enter iterative code!
    
    error = image_center[0] - cX
    
    current_time = time.time()
    time_elapsed = current_time - prev_time
    derivative_term = Kd * ((error - prev_error))
    sum_error += error * time_elapsed
    integral_term = Ki * sum_error


    angular_vel = Kp * error + integral_term + derivative_term
    angular_vel = max(-max_angular_vel, min(max_angular_vel, angular_vel))
    
    print('la coordenada X:', cX)
    print('El error es:', error)
    print('La velocidad angular:', angular_vel)
    
    HAL.setW(angular_vel)
    HAL.setV(linear_vel)
    
    # show the images
    
    cv2.waitKey(0)
    
    prev_error = error
    prev_time = current_time