'''
Modulo encargado mostrar el aqueducto
Autores: Ramon Escoda Semís y Marc Godia Calderó
'''
import math
import matplotlib.pyplot as plt
import numpy as np

def plot_all(intervals, columns=None, height=None, cost=None):
    '''
        Dibuja el Aqueducto
    '''
    # Pinta el acueducto
    if columns is not None and height is not None:
        p_x = np.array([intervals[0][0], intervals[-1][0]])
        p_y = np.array([height for i in p_x])
        plt.plot(p_x, p_y, color='black')
        plot_colunms(columns, height)
        plot_arc(columns, height)
    # Pinta el suelo
    x_floor = np.arange(intervals[0][0], intervals[-1][0] +  1, 1)
    y_floor = np.array([get_y(i, intervals) for i in x_floor])
    plt.plot(x_floor, y_floor, color='black', alpha=1.00, zorder=10)
    plt.fill_between(x_floor, y_floor, y_floor - y_floor, color='green', zorder=10)
    plt.xlim(-0.5, intervals[-1][0] + 0.5)
    if cost is None:
        plt.title('Aqueducte')
    else:
        plt.title('Aqueducte \nCoste: ' + str(cost))
    plt.gcf().canvas.set_window_title('Aqueducte')
    plt.show()

def plot_colunms(columns, height):
    '''
        Dibujas las columnas del acueducto
    '''
    for column in columns:
        x_pos = [column[0]] * 2
        y_pos = [column[1], height]
        plt.plot(x_pos, y_pos, 'black')

def plot_arc(columns, height):
    '''
        Dibuja los arcos del arco
    '''
    for index, column in enumerate(columns[:-1]):
        distance = columns[index + 1][0] - column[0]
        radius = distance / 2
        center = (column[0] + radius, height - radius)
        x_positions = np.arange(column[0], columns[index + 1][0] + 1, 0.119)
        # Descarta todas las posiciones generadas y que no esten el arco
        x_positions = x_positions[x_positions <= center[0] + radius]
        y_positions = np.array([get_arc_y(x, center, radius) for x in x_positions])
        plt.fill_between(x_positions, [height]* x_positions.shape[0], y_positions, color='C0')
        plt.plot(x_positions, y_positions, color='black')

def get_y(x_value, intervals):
    '''
        Obtiene el valor de y del suelo que corresponde al valor de x
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
        Obtiene la cordenada y del arco correspondiente al valor x
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
