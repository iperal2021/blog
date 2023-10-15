---
layout: post
title: Second Practice
---

# Follow Line

For this second practice for mobile robotics, I need to implement the code for a line follower, which must adjust its speed automatically through the use of *PID* controllers and I will use image filters to isolate the line and be able to follow it effectively.

For the image code I have to use the [OpenCV library](http://opencv.org)

## Before starting

Before starting to program I must set some objectives so that little by little the program develops.

1. Get the line.
2. Find the centroid.
3. PID for angular velocity.
4. PID for linear velocity.
5. (Possible improvement) Split the image in two: whit two centroids calculate linear and angular errors.
 
## PID

A *PID* controller (proportional, integral and derivative controller) is a control mechanism that, through a feedback loop, allows the regulation of speed, temperature, pressure and flow among other variables of a process in general. The *PID* controller calculates the difference between our actual variable versus the desired variable.

To adjust the speed of the 'car' I have to use this controllers, wich will make it automatically. The best way to get a useful *PID* is to start bit by bit. That is to start whit a *P* controller, then a *D* controller and if needed, a *I* controller.

## OpenCV

OpenCV is an open source library that is designed to work with images. This package includes different features like fillters and options to customize the image.

Since the line to follow is red, I must create a filter that only detects that color. This is the code that filters the image to only show that color:

```python
image = HAL.getImage()
    
    boundaries = [
	([17, 15, 100], [50, 56, 255])]

    for (lower, upper) in boundaries:
      	# create NumPy arrays from the boundaries
      	lower = np.array(lower, dtype = "uint8")
      	upper = np.array(upper, dtype = "uint8")
      	# find the colors within the specified boundaries and apply
      	# the mask
      	mask = cv2.inRange(image, lower, upper)
      	output = cv2.bitwise_and(image, image, mask = mask)
      	# show the images
      	GUI.showImage(output)
      	cv2.waitKey(0)
```

![filtro_rojo](../images/red_filter.png)

The next thing to find once we have created the mask is the ***centroid*** of the figure to be able to make the necessary calculations to follow the line.

```python
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
```

A change regarding the original *centroid* code is the if-else statement, wich allows to avoid an ocassional bug.

![filtro_rojo](../images/centroid.png)

To further improve the reactivity of the program, we can leave out the upper part of the image because nothing relevant to the execution of the program is shown. Therefore, using openCV once again we crop it before working with it.
> corte = image_hsv[250:450, 0:image_hsv.shape[1]]

![imagen_corte](../images/filtroRecortado.png)

To achieve this, I follow the tutorials and recomendations given to us in the documentation of the practice. Here are two links I used:

[OpenCV en español](https://omes-va.com/deteccion-de-colores/)

[OpenCV en inglés](https://stackoverflow.com/questions/10469235/opencv-apply-mask-to-a-color-image)

To improve once more the processing of the image, I change the code used in the mask to get the red line. 

## 

The first step to start once I have the processed image, is to implement the *P* controller to adjust the angular speed to maintain the car with straight movement in staight line an to take the curves without oscillation.

The calculations are simple, only I need to find the error between the **centroid** and the center of the image to then multiply it by the **Kp** parameter wich I have to adjust until I have the proper functioning.

Once I have this first controller the bugs start to appear. By now I have 3 different errors:

1. The process dies and the car starts spinning without any control.
2. The process dies and the car doesn't move at all.
3. The process does not die and the car moves exclusively in a straight line

> **Escenario 1**:
![error_1_video](../images/fl_error1.gif)


> **Escenario 2**:
![error_2](../images/fl_error2.gif)


> **Escenario 3**			:
![error_3_video](../images/fl_error3.gif)

To resolve these erros I modify different parts of the code. The first change was to add the if-else statement I note before in the centroid code. Another change was to add a maximum angular velocity.

The next change was to add the *D* controller to avoid oscillations and be able to use a higher linear speed. The calculation for this term is to multiply the *Kd* variable by the substration of the error and the previous error.

```python
derivative_term = Kd * ((error - prev_error))
angular_vel = Kp * error + derivative_term

[...]

prev_error = error
```

I tried to add the *I* controller but no matter the value of the *Ki* variable, the movement I get isn't the correct one. For this reason this term will be 0 until I really need it and it doesn't ruin the functioning.

