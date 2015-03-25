# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import binom
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D

class IntersectionBezier:
    def __init__(self):
        # Aqui habra cosas bonitas para la creacion del Intersection
        pass

    def __call__(self, P, Q, epsilon):
        # P.shape = (n, 2)
        # Q.shape = (m,2)
        # Epsilon controlara si se aproxima el poligono 
        #   de control mediante un segmento
        self.epsilon = epsilon

        # Returns: K puntos de interseccion calculados como un array
        # de numpy de dimensiones (K, 2)

        # Si no hay puntos de interseccion, podemos devolver un None

        # Hacemos las subdivisiones y vamos llamando a otra funcion interseccion
        intersection_points = self.intersection(P, Q)

        # Revisar el length y la forma de crear el array cuando sepamos que devuelve el intersection
        if intersection_points == None:
            return None
        else:
            return np.array(intersection_points)
        
    def intersection(self, P, Q):
        return None
        
    def plot(self, k=3):
        # Metodo que produce el dibujo de las curvas y las
        # intersecciones.
        pass
        
        
if __name__ == '__main__':
    N = 15  
    epsilon = 0.1

    # Instancia de la clase
    intersect = IntersectionBezier()
    
    # Puntos aleatorios para generar las curvas de Bezier
    P = np.random.uniform(-20, 20, (N + 1, 2))
    Q = np.random.uniform(-20, 20, (N + 1, 2))

    intersect(P, Q, epsilon) # Llamada al __call__ de la clase

    intersect.plot()
