from HAL import HAL
from GUI import GUI
import MAP
import numpy as np
from numpy.linalg import norm
import time
from multiprocessing import Pool

N_PARTICLES = 100
OBSTACLE_VALUE = 0
LINEAR_VEL = 0.3
ANGULAR_VEL = 1

MAX_LASER_DISTANCE = 100
MAP_OFFSET = (200, 260)
LASER_SKIP_RATIO = 10

# Time of the last propagation of the particles
last_update_time = time.time()

map = MAP.getMap()

def initialize_particles():
    """ Generate random particles in world coordinates (meters).
        X/Y values are constrained within the map limits.
        Yaw values are in the [0, 2*pi] range.
    """
    # Allocate space
    particles = np.zeros((N_PARTICLES, 4))
    # Get the limits from the MAP module
    x_low, y_low = MAP.WORLD_LIMITS_LOW
    x_high, y_high = MAP.WORLD_LIMITS_HIGH
    # Distribute randomly in the map inside the limits
    particle = []
    for i in range(N_PARTICLES):
        particles = np.random.uniform(low=[x_low, y_low, 0.0],
                                  high=[x_high, y_high, 2*np.pi],
                                  size=(3,))
        particle_map = MAP.worldToMap(particles[0], particles[1])
        
        while map[particle_map[1], particle_map[0]] == 0:
            particles = np.random.uniform(low=[x_low, y_low, 0.0],
                                  high=[x_high, y_high, 2*np.pi],
                                  size=(3,))
            particle_map = MAP.worldToMap(particles[0], particles[1])
        particle.append(particles)
    return particle

def compute_particle_weights(particles_laser, real_laser):
    weights = []

    for particle_laser in particles_laser:
        # Convertir la lista de lecturas láser de la partícula en un array numpy
        particle_laser_array = np.array(particle_laser)

        # Calcular la similitud (inversa de la diferencia) entre la referencia y la partícula
        similarity = np.linalg.norm(real_laser - particle_laser_array)

        # Normalizar la similitud para obtener los pesos
        weights.append(1 / (1 + similarity))
    #print("Pesos", weights, "\n")

    return np.array(weights)

def resample_particles(old_particles, weights):
    """ Resample the set of particles given their weights. """
    # Allocate space for new particles
    old_particles = np.array(old_particles)
    particles = np.zeros((N_PARTICLES, 3))
    print(weights.shape)
    # Normalize the weights so the total sum is 1
    weights /= np.sum(weights)
    #print(F"Normalized weights: {weights}")

    # Get random indices from the list of particles
    selected_idx = np.random.choice(N_PARTICLES, replace=True, size=N_PARTICLES, p=weights)
    particles = old_particles[selected_idx]
    return particles

def update_particle_pose(particle, dt):
    """ Update the pose of a particle in the dt period.
        Add a random Gaussian noise to the movement.
    """
    yaw = particle[2]
    # Estimate robot movement in dt according to the set velocities
    dx = dt * LINEAR_VEL * np.cos(yaw)
    dy = dt * LINEAR_VEL * np.sin(yaw)
    dyaw = dt * ANGULAR_VEL
    # Add this movement to the particle, with an extra Gaussian noise
    particle[0] += dx + np.random.normal(0.0, 0.02)
    particle[1] += dy + np.random.normal(0.0, 0.02)
    particle[2] += dyaw + np.random.normal(0.0, 0.01)

def propagate_particles(particles):
    """ Estimate the movement of the robot since the last update
        and propagate the pose of all particles according to this movement.
    """
    global last_update_time
    # Get the time diference since the last update
    current_time = time.time()
    dt = current_time - last_update_time
    # Update all particles according to dt
    for p in particles:
        update_particle_pose(p, dt)
    # Reset the update time
    last_update_time = current_time
    return particles

def particle_virtual_laser_beam(start_x, start_y, end_x, end_y):
        """ Generates a line using DDA algorithm until an obstacle is found
            or the end point is reached.
            Returns the point (x,y) where the line ends.
            If the end point is reached, returns infinite.
        """
        # Find the slope and direction of the line
        dx = int(abs(end_x - start_x))
        dy = int(abs(end_y - start_y))
        # Number of steps (dx or dy depending on what is bigger)
        steps = max(dx, dy)

        # Adjust dx and dy to the small step value according to previous calculations
        dx = (end_x - start_x) / steps
        dy = (end_y - start_y) / steps

        for i in range(0, steps):
            # Compute the indices for each step and convert to int to get cell positions
            x = start_x + int(dx * i)
            y = start_y + int(dy * i)
            if 0 <= x < 400 and 0<= y < 400:
                if map[y, x] == OBSTACLE_VALUE:
                    return (x, y)

        return (np.inf, np.inf)

def getParticlesLaser(particles):
    """ Returns the measurements from the laser sensor for a list of particles.
        Returns a list of lists of (x, y) points in global world coordinates for each particle.
    """
    virtual_laser_readings = []

    for particle in particles:
        # Get the robot pose in map coordinates as the origin of the laser 
        start_x, start_y, particle_yaw_map = MAP.worldToMap(particle[0], particle[1], particle[2])
        # Convert max laser detection distance from meters to map cells
        laser_distance_cells = MAX_LASER_DISTANCE * MAP.MAP_SCALE
        virtual_laser_xy = []
        laser_count = 1

        for beam_angle in range(180):
            if laser_count == LASER_SKIP_RATIO:
                # Actual beam's angle in map coordinates
                # Subtract 90º to have the center aligned with the robot
                angle = particle_yaw_map + np.radians(beam_angle) - np.pi/2
                # Compute the theoretical (max) endpoint of the laser
                end_x = start_x + laser_distance_cells * np.cos(angle)
                end_y = start_y + laser_distance_cells * np.sin(angle)
                # Get the laser measurement
                laser_x, laser_y = particle_virtual_laser_beam(start_x, start_y, end_x, end_y)
                virtual_laser_xy.append((laser_x, laser_y, 0))
                laser_count = 1
            else:
                laser_count += 1

        world_laser_xy = MAP.mapToWorldArray(np.array(virtual_laser_xy))
        #print(world_laser_xy.shape)
        #print(world_laser_xy.shape)
        virtual_laser_readings.append(world_laser_xy.tolist())
    return np.array(virtual_laser_readings)

def reduceLaserData(laser_data):
    """ Reduces the laser data array to include only one measurement
        out of every six.
    """
    reduced_laser_data = laser_data[::LASER_SKIP_RATIO]
    return reduced_laser_data

def main():
    gui = GUI()
     # Create a HAL (robot) object
    robot = HAL()
    # Set a custom initial pose
    robot.pose[0] = 1.1
    # Create a GUI object and link it with the robot
    gui = GUI(robot=robot)

    # Initialize some random particles
    particles = initialize_particles()
    # Set a small velocity
    robot.setV(LINEAR_VEL)
    robot.setW(ANGULAR_VEL)

    # Store the time of the last pose update
    last_update_time = time.time()

    #print(particles)
    while True:
        # Propagation (prediction) step
        particles = propagate_particles(particles)
        laser_data = robot.getLaserData()
        real_laser = reduceLaserData(laser_data)
        
        particles_laser = getParticlesLaser(particles)
        #print("Particles: ",particles_laser.shape)
        #print("Robot: ",real_laser.shape)
        # Show the particles in the GUI
        gui.showParticles(particles)
        gui.showLaser(real_laser)     
       
        weights = compute_particle_weights(particles_laser, real_laser)
       
        # Resample the particles
        particles = resample_particles(particles, weights)
        # Robot pose is automatically updated inside the GUI "updateGUI"
        gui.updateGUI()
        
    
if __name__ == '__main__':
    main()   