---
layout: post
title: First Practice
---

# Basic Vacuum Cleaner

For the first practice, I have to program the behavior of a basic vacuum cleaner.

Program Requirements:

* State machine
* Random movement
* Spiral movement
* Use of laser

Before starting to implement the program, following the requested requirements, I need to think about how I want it to behave, meaning what states it will have, what algorithm it will follow for random movement, and how I will read distances to avoid obstacles on the map.

## First step in implementation

The conclusions I draw are as follows:

1. State machine

   The state machine I want to implement has a total of three states: spiral movement, forward movement, and the turn that I plan to convert into random movement.

2. Spiral movement

   To achieve a spiral movement, I need to calculate the linear and angular velocities mathematically to get the desired movement. The idea is that this will be the first state of the program and a possible recurring state.

3. Obstacle detection

   It's important to detect obstacles throughout the program to avoid any type of collision regardless of the state we are in. To achieve this, we start from the code provided in the practice documentation:

   ```python
   laser_data = HAL.getLaserData()

   def parse_laser_data(laser_data):
       laser = []
       for i in range(180):
           dist = laser_data.values[i]
           angle = math.radians(i)
           laser += [(dist, angle)]
       return laser
   ```

4. Random turn

   This is an important part of the program because by creating an algorithm that randomly chooses the direction of the turn and its duration, I can achieve semi-random behavior, which is what has been requested in the practice.

   One idea for this algorithm is to randomly select a number from a list, and based on the value of this number, perform the turn to the left or right, with the value of the number dictating the duration of the turn.

## Implementation kickoff

### Spiral

I set aside working with the laser while I try to create the spiral movement. To achieve this movement, I need to make the necessary calculations to optimize the linear and angular velocities.

Knowing that ***v = w * r***, where v is the linear velocity, w is the angular velocity, and r is the radius. To obtain the spiral, I need to increase the radius after each turn and reduce the angular velocity. The initial calculation I try is as follows:

```python
INITIAL_RADIUS = 0.10
RADIUS_INCREMENT = 0.20
spiral_linear_vel = 1.00
spiral_angular_vel = spiral_linear_vel / INITIAL_RADIUS
```

With this operation, each time the radius increases, the angular velocity decreases, creating a wider movement each time.

Within the `while` loop, I have the following code:

```python
HAL.setV(spiral_linear_vel)
HAL.setW(spiral_angular_vel)
INITIAL_RADIUS += RADIUS_INCREMENT
spiral_angular_vel = spiral_linear_vel / INITIAL_RADIUS
```

Unfortunately, these lines of code do not give the expected result when simulating, as the movement becomes linear shortly after starting the program.

![video_spiral_1](../images/spiral_failed_1.gif)

After this problem, I concluded that I needed to add a `Timer` that allows me to perform multiple turns.

```python
time_per_turn = 2 * math.pi * INITIAL_RADIUS / spiral_linear_vel
time.sleep(time_per_turn)
``` 

The result obtained now is more satisfactory.

![video_spiral_2](../images/spiral_good_linear.gif)

After reading the practice documentation, I found that it was more effective to increase the linear velocity rather than the angular velocity. After testing this, I concluded that indeed the velocity seems more consistent, but a perfectly uniform spiral is not achieved.

![video_spiral_3](../images/spiral_good_angular.gif)

Researching a way to keep track of time without using a sleep that could interrupt execution, I found that with the `time.time()` function, I can create a function to which I can add a condition to break the waiting loop.

```python
def my_sleep(seconds, condition):
    start_time = time.time()
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= seconds:
            break 
        elif elapsed_time < seconds and condition:
            break
```
---
#### Laser

Once I have achieved spiral movement, I need to start working with the laser to detect obstacles and stop the robot's movement to initiate the next state.

To obtain the distance read by the laser, I use the code given in the practice documentation, as mentioned earlier. This code stores all the distances detected by the laser in a range of 180 degrees in a tuple.

Since the base range is too large for the movement I want to achieve, I edit the code to reduce the detection range and have a more uniform movement, focusing on obstacles in front of the robot.

> Original function

```python
def parse_laser_data(laser_data):
    laser = []
    for i in range(180):
        dist = laser_data.values[i]
        angle = math.radians(i)
        laser += [(dist, angle)]
    return laser
```

> Edited function

```python
def parse_laser_data(laser_data):
    laser = []
    center = 90  # Laser's central angle (180 degrees divided by 2)
    range = 45   # Range of ±45 degrees or the desired angle; in case of choosing a different distance range, I need to check if additional calculations are needed
    for i in range(center - range, center + range + 1):
        if 0 <= i < 180:  # Ensure the index is within the valid range
            dist = laser_data.values[i]
            angle = math.radians(i)
            laser += [(dist, angle)]
    return laser
```
---
#### Random Turn

For the turn, I thought about implementing an algorithm that chooses the direction and duration of the turn randomly. This implementation went through two different versions, with the second one being visually clearer.

The algorithm is as follows: I choose an integer number from 0 to 9. In the first version, numbers 0 to 4 would make the robot turn in one direction, and 5 to 9 in the other direction. In the second version, I opted for odd numbers to indicate a left turn and even numbers for a right turn.

Once the direction of the turn is chosen, I need to select the duration. To avoid having to choose another random number, I decided to assign times in pairs, for example, if it's 0 or 9, it's 5 seconds; if it's 1 or 8, it's 4 seconds, and so on.

> Version 1.0
```python
def random_turn():
    number = random.randint(0, 9)
    if 0 <= number <= 4:
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
            
    elif 5 <= number <= 9:
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
```

> Version 2.0

```python
number = random.randint(0, 9)
if number % 2 == 0:
    setW(0.2)  # Turn right
else:
    setW(-0.2)  # Turn left

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
```

As we can see, the second version uses fewer lines of code.

The final turns are as follows:

| NUMBER    | DIRECTION    | TIME    |
|-----------|--------------|---------|
| 0         | Right        | 4       |
| 1         | Left         | 3       |
| 2         | Right        | 2.5     |
| 3         | Left         | 2       |
| 4         | Right        | 1       |
| 5         | Left         | 1       |
| 6         | Right        | 2       |
| 7         | Left         | 2.5     |
| 8         | Right        | 3       |
| 9         | Left         | 4       |

Certainly, here is your text translated into English while preserving the Markdown format:
---
#### TESTING

Once we have the obstacle-detecting laser and the random turn function, it's time to test everything together since until now, I have only tested each part separately. It is now that syntactic and logical errors start to appear.

A machine with only 2 states, random turn, and linear forward movement, seems to work quite well. But when adding the spiral movement, the program experiences logical errors.

The main problem is the inability to detect objects correctly while the spiral movement is being executed. This error is accompanied by a failure in transitioning from one state to another.

Without the state that performs the spiral movement, an example of the result is as follows:

![test_without_spiral](../images/program_without_spiral.gif)

As you can see, there is a random movement when choosing the direction of the turn and its duration.

This program, without the spiral movement, can produce good results after a long period.

![test_without_spiral2](../images/test_WITHOUT_spiral.png)

It should be noted that if it enters the middle-left room at any time, the time the robot spends there can be very high.
---
#### FIXING ERRORS

Once the main error has been identified, which is, as explained earlier, that the program does not detect obstacles correctly when executing the spiral movement, it is time to fix it. For this, I chose to start the implementation of the spiral from scratch, but this time trying to find the simplest solution to the problem (Ockham's razor).

The conclusion I reach that may be simpler is to avoid unnecessary calculations and only increase the *linear velocity* after each iteration as stated in the documentation.

```python
HAL.setV(LINEAR_VEL)
HAL.setW(ANGULAR_VEL)   
LINEAR_VEL += 0.00125
```

The increase must be small so that the spiral has a compact shape without leaving gaps after each turn.

![spiral_GOOD](../images/spiral_GOOD.gif)

---
#### FINAL PROGRAM

Once the problem with the spiral has been fixed, and with the rest of the states already in place, it is time to put everything together and start adjusting the times and velocities to achieve the most optimal performance.

Due to the semi-random movement, each time the program starts, if measured at the same time, we will always get a different pattern than the previous one, sometimes resulting in a better outcome.

The best implementation so far was to start with the spiral movement and once an obstacle is detected, follow a loop of forward movement followed by a random turn whenever an obstacle is detected at the specified distance. But it is necessary to add a way to return to the spiral movement and make it efficient.

To perform the previous turn, I used a function with a `while` loop, but since it is not a good programming practice, I modified it as follows, reducing the number of functions used:

```python
 if STATE == 1:
        
        laser_data = HAL.getLaserData()
        
        HAL.setV(0)  # Stop linear movement
    
        number = random.randint(0, 9)
        if number % 2 == 0:
            HAL.setW(ANGULAR_VEL_R)  # Turn right
        else:
            HAL.setW(ANGULAR_VEL_L)  # Turn left
        global time_to_turn
        if number == 0 or number == 9:
            time_to_turn = 10
        elif number == 1 or number == 8:
            time_to_turn = 9
        elif number == 2 or number == 7:
            time_to_turn = 8
        elif number == 3 or number == 6:
            time_to_turn = 7
        else:
            time_to_turn = 6
        if (time.time() - Initial_time) >= time_to_turn:
            Initial_time = time.time()
            STATE = 2
```

This way, it should avoid using the previously mentioned loop that could interrupt the program's execution. Unfortunately, the final operation is not as expected, as the time it takes to cover the same area is longer than in the previous version of the program.

Below are two videos of the program's execution with this version and the previous one.

[Video 1: Version without Loop](https://github.com/iperal2021/blog/assets/113594702/e26f310b-3b4e-49d8-969b-b198cbb760e1)

As we can see in this version, which I tried to eliminate unnecessary loops that would stop the execution, the turns are not exact, resulting in less ground covered.
> [Code of this version.](https://github.com/iperal2021/blog/blob/master/practica_1/vacuum_cleaner_v5.py)

[Video 2: Version with While Loop](https://github.com/iperal2021/blog/assets/113594702/0802bc5b-5b2c-4751-bdf4-f2ff83f94ed1)

In this version, a `while` loop is used, but the turns are more accurate and faster, resulting in greater ground coverage and a faster movement which enables the option to scape from narrow paths or rooms.

> [Code of this version.](https://github.com/iperal2021/blog/blob/master/practica_1/vacuum_cleaner_v4.py)

All the changes of this two versions and the other ones can be consulted in the **[repository](https://github.com/iperal2021/blog/tree/master/practica_1)** which hold this **[blog](https://github.com/iperal2021/blog)**.
