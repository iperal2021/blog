from GUI import GUI
from HAL import HAL
from MAP import MAP
import numpy as np
from queue import PriorityQueue

# Inicialización de variables

points = PriorityQueue()
expanded = set()
counter = 0
carPose = MAP.rowColumn([HAL.getPose3d().x, HAL.getPose3d().y])
targetPose = MAP.rowColumn(GUI.getTargetPose())
x0, y0 = targetPose

# Obtener el mapa
def get_map():
    map_array = MAP.getMap('/RoboticsAcademy/exercises/static/exercises/global_navigation_newmanager/resources/images/cityLargenBin.png')
    return map_array

map_array = get_map()
grid = np.zeros_like(map_array)

# Convertir coordenadas del mapa a coordenadas del mundo
def gridToWorld(mapcell):
    world_x = mapcell[1] * 500 / 400 - 250
    world_y = mapcell[0] * 500 / 400 - 250
    return world_x, world_y

# Calcular heurística de distancia entre dos posiciones
def distance_heuristic(pos1, pos2):
    return np.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

# Normalizar el grid, reemplazando ciertos valores por cero
def normalized(grid):
    normalized_grid = np.where(grid == 1000)
    grid[normalized_grid] = 0
    return grid

# Función sigmoide para suavizar la diferencia entre coordenadas
def sigmoid(x):
    return 1 / (1 + np.exp(-0.1 * x))  # Ajusta el factor de escala según sea necesario

# Generar el gradiente
# Generar el gradiente
def gradient(target_found, initial_point):
    global counter
    
    while not target_found:
        if not initial_point:
            # Inicializar el punto de inicio en las coordenadas del objetivo
            points.put((0, [x0, y0]))
            initial_point = True

        if not target_found:
            next_point = points.get()
            priority, coords = next_point
            x, y = coords

            if coords == carPose:
                print(counter)
                print("FIN")
                target_found = True
                break

            if (x, y) not in expanded:
                counter += 1
                expanded.add((x, y))
                print(x, y)
                distance_to_target = distance_heuristic(coords, targetPose)
                heuristic = sigmoid(distance_to_target)

                cost_cross = priority + heuristic + 1
                cost_x = priority + heuristic + 1.2

                if (0 <= y < 400) and (0 <= x + 1 < 400):
                    if map_array[x + 1][y] != 0 and (x + 1, y) not in expanded:
                        grid[x + 1][y] = cost_cross
                        points.put((cost_cross, [x + 1, y]))

                if (0 <= y < 400) and (0 <= x - 1 < 400):
                    if map_array[x - 1][y] != 0 and (x - 1, y) not in expanded:
                        grid[x - 1][y] = cost_cross
                        points.put((cost_cross, [x - 1, y]))

                if (0 <= y + 1 < 400) and (0 <= x < 400):
                    if map_array[x][y + 1] != 0 and (x, y + 1) not in expanded:
                        grid[x][y + 1] = cost_cross
                        points.put((cost_cross, [x, y + 1]))

                if (0 <= y - 1 < 400) and (0 <= x < 400):
                    if map_array[x][y - 1] != 0 and (x, y - 1) not in expanded:
                        grid[x][y - 1] = cost_cross
                        points.put((cost_cross, [x, y - 1]))

                for j in range(-1, 2):
                    for k in range(-1, 2):
                        new_x, new_y = x + j, y + k
                        if (0 <= new_y < 400) and (0 <= new_x < 400):
                            if map_array[new_x][new_y] != 0 and (new_x, new_y) not in expanded:
                                grid[new_x][new_y] = cost_cross
                                points.put((cost_cross, [new_x, new_y]))


initial_point = False
target_found = False
# Bucle principal
while True:
    new_target = GUI.getTargetPose()
    target_map = MAP.rowColumn(new_target)

    path = [carPose, targetPose]
    GUI.showPath(path)
    

    gradient(target_found, initial_point)
    GUI.showNumpy(normalized(grid))
