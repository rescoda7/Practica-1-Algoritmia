'''
    Modulo encargado de obtener el aqueducto de coste
    minimo, si es posible

    Autor: Ramon Escoda Semis
'''
import math
import sys
import argparse
import aqutils
def load_file(path):
    '''
        Funcion encargada de leer el fichero
    '''
    try:
        # Abre el archivo
        aqueducte_file = open(path, 'r')
        # Trata la primera linea
        n_columns, hight, alpha, beta = aqueducte_file.readline().split(' ')
        # Trata el resto de lineas
        points = []
        for line in aqueducte_file:
            x_value, y_value = line.split(' ')
            points.append((int(x_value), int(y_value)))
    except (FileNotFoundError, ValueError) as exception:
        if exception == FileNotFoundError:
            print('Error no se ha encontrado el fichero')
        elif exception == ValueError:
            print('Error formato del fichero es erroneo')
        return None
    return {
        'n':int(n_columns),
        'height':int(hight),
        'alpha':int(alpha),
        'beta':int(beta),
        'points':points,
    }

def get_y(x_value, intervals):
    '''
        Obtiene el valor de y que corresponde al valor de x
    '''
    for index, interval in enumerate(intervals[:-1]):
        if x_value > intervals[index + 1][0]:
            continue
        vector_xa, vector_ya = interval
        vector_xb, vector_yb = intervals[index + 1]
        vector = (vector_xa - vector_xb, vector_ya -  vector_yb)
        return (vector[1]/vector[0]) * (x_value - interval[0]) + interval[1]

def get_arc_y(x_pos, center, radius):
    '''
        Obtiene la posicion y del arco
    '''
    # Obtiene los coeficientes de la ecuacion
    b_coef = -2 * center[1]
    c_coef = ((x_pos - center[0]) ** 2)  + (center[1] ** 2) - (radius ** 2)
    sq_coef = (b_coef ** 2) - 4 * c_coef
    # Optiene las dos soluciones
    y1_pos = (-b_coef - math.sqrt(sq_coef)) / 2
    y2_pos = (-b_coef  + math.sqrt(sq_coef)) / 2
    # Devuelve la solucion que representa el punto superior de la circuferencia
    return y1_pos if y1_pos >= center[1] else y2_pos

def calculate_cost(columns, height, alpha, beta):
    '''
        Calcula el coste de la configuracion del aqueducto
    '''
    sum_heights = 0
    sum_distances = 0
    for index_col, column in enumerate(columns):
        sum_heights += height - column[1]
        if index_col + 1 < len(columns):
            sum_distances += (columns[index_col + 1][0] - column[0]) ** 2
    return alpha * sum_heights + beta * sum_distances

def is_possible(points, columns, height):
    '''
        Comprueba si es posible construir el puente
    '''
    # Opcions acueducto puente
    if len(columns) == 2:
        radius = (columns[1][0] - columns[0][0]) / 2
        center = [columns[0][0] + radius, height - radius]
        for column_pos in points[1:-1]:
            y_arc = get_arc_y(column_pos[0], center, radius)
            if column_pos[1] > y_arc:
                return False
    else:
        # Opcions acueducto normal
        for idx, column in enumerate(columns[:-1]):
            radius = (columns[idx + 1][0] - column[0]) / 2
            center = [column[0] + radius, height - radius]
            y_arc_c1 = get_arc_y(column[0], center, radius)
            y_arc_c2 = get_arc_y(columns[idx + 1][0], center, radius)
            if y_arc_c1 < column[1] or y_arc_c2 < columns[idx + 1][1]:
                return False
    return True

def recursive_find_best_aqueducte(aqueducte):
    '''
        Optiene la mejor opcion del acueducto de forma recursiva
    '''
    points = aqueducte['points']
    height = aqueducte['height']
    alpha = aqueducte['alpha']
    beta = aqueducte['beta']
    # Seleccionamos las dos opciones columnas en los extremos o en todos los puntos
    columns_options = [[points[0], points[-1]], points]
    return recursive_find(points, columns_options, height, alpha, beta)

def recursive_find(points, columns_options, height, alpha, beta):
    '''
        Busca la mejor opcion de puente de una lista de opciones de forma recursiva
    '''
    # Caso base no quedan opciones por evaluar
    if len(columns_options) == 0:
        return None, -1
    # Escogemos la opcion de la lista
    option = columns_options[0]
    # Comprobamos que sea posible
    if not is_possible(points, option, height):
        # Si no es posible se continua con la siguiente
        return recursive_find(points, columns_options[1:], height, alpha, beta)
    # Si es posible calculamos su coste
    current_cost = calculate_cost(option, height, alpha, beta)
    # Obtenemos el coste de la siguiente opcion posible
    next_option, next_cost = recursive_find(points, columns_options[1:], height, alpha, beta)
    # Si no exite ninguna opcion posible se retorna el coste de la actual
    if next_option is None:
        return option, current_cost
    # Si es posible se comparan los costes
    if current_cost < next_cost:
        # Si el coste actual es mejor al mejor coste de las siguientes opciones
        return option, current_cost

    return next_option, next_cost

def main():
    '''
        Funcion main
    '''
    # Parsea los argumentos de entrada
    parser = argparse.ArgumentParser(description='Aqueducte')
    parser.add_argument('aqueducte_file', help='Fichero del aqueducto')
    parser.add_argument('-g', '--showAqueducte', help='Mostrar acueducto',
                        action='store_true')
    args = parser.parse_args()
    # Lee el fichero
    aqueducte_info = load_file(args.aqueducte_file)
    if aqueducte_info is None:
        print('Error no se ha optenido la informacion del aqueducto')
        sys.exit(0)
    best_option, cost = recursive_find_best_aqueducte(aqueducte_info)
    # Guarda la solucion en el fichero output.ans
    file_ans = open('output.ans', 'w')
    if best_option is None:
        file_ans.write('imposible' + '\n')
    else:
        file_ans.write(str(cost)+ '\n')
    file_ans.close()
    # Muestra el aqueducto si se ha puesto el flag -g
    if args.showAqueducte:
        aqutils.plot_all(aqueducte_info['points'], best_option, aqueducte_info['height'], cost)

if __name__ == '__main__':
    main()
