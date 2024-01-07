def distance_control(particles, dist):
    
    X_robot = 0
    Y_robot = 0
    
    distances = []
    for i in range(N_PARTICLES):
        X_robot += particles[i][0]
        Y_robot += particles[i][1]
    
    X_robot = X_robot / N_PARTICLES
    Y_robot = Y_robot / N_PARTICLES
    #print("X_robot", X_robot, "Y_robots", Y_robot)
    #print("n particles", PARTICLES_LASER_ARRAY.shape[0])
    
    
    for i in range(PARTICLES_LASER_ARRAY.shape[0]):
        x_coordinates = PARTICLES_LASER_ARRAY[i][0]
        y_coordinates = PARTICLES_LASER_ARRAY[i][1]
        distances.append(np.sqrt((x_coordinates - X_robot)**2 + (y_coordinates - Y_robot)**2))

    for element in distances:
        print("Distance", element)
        if element < dist:
            return True
    return False