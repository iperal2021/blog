from GUI import GUI
from HAL import HAL
from MAP import MAP
import numpy as np
from queue import PriorityQueue

# Definir el tamaño del grid
grid_size = (400, 400)
# Inicializar el grid con ceros
grid = np.zeros(grid_size)

expanded = []

# Obtener el mapa del archivo de imagen
map_array = MAP.getMap('/RoboticsAcademy/exercises/static/exercises/global_navigation_newmanager/resources/images/cityLargenBin.png')

# Función para calcular la heurística de distancia
def distance_heuristic(pos1, pos2):
    return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

# Función para normalizar el grid
def normalized(grid):
    normaliced_grid = np.where(grid == 1000)
    grid[normaliced_grid] = 0
    return grid

# Obtener las posiciones inicial y objetivo
carPose = MAP.rowColumn([HAL.getPose3d().x, HAL.getPose3d().y])
targetPose = MAP.rowColumn(GUI.getTargetPose())

# Inicializar la cola de prioridad
points = PriorityQueue()
# Agregar la posición inicial a la cola de prioridad
points.put((0, targetPose))

target_found = False

# Bucle principal
while True:
        
    if not target_found:
        
        # Obtener el punto actual y su peso
        weight, current_point = points.get()
    
        # Verificar si llegamos a la coordenada de carPose
        if current_point == carPose:
            target_found = True
        # Obtener las coordenadas x, y del punto actual
        x, y = current_point
        print(x,y)
        # Definir los vecinos del punto actual
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    
        for neighbor in neighbors:
            nx, ny = neighbor
            print("2: ", nx,ny)
    
            # Verificar si el vecino está dentro del límite del grid
            if 0 <= nx < 400 and 0 <= ny < 400:
                # Verificar si el vecino no es un obstáculo
                if map_array[nx][ny] != 0:
                    # Calcular el peso del vecino sumando el peso actual
                    new_weight = weight + distance_heuristic(current_point, neighbor)
                    print("new weight: ", new_weight)
                    print("grid[ny][nx]: ", grid[ny][nx])
                    # Verificar si el vecino ya ha sido explorado
                    if neighbor not in expanded or new_weight < grid[ny][nx]:
                        # Actualizar el peso del vecino en el grid
                        grid[ny][nx] = new_weight
                        print(neighbor)
                        # Agregar el vecino a la cola de prioridad con su nuevo peso
                        points.put((new_weight, neighbor))

        # Marcar el punto actual como explorado
        expanded.append(current_point)


    if target_found:
        print("FIN")
        # Normalizar el grid
        grid = normalized(grid)
        
        # Mostrar el gradiente en la interfaz gráfica
        GUI.showNumpy(grid)
