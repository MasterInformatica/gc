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

        # Si no hay puntos de interseccion, devolvemos np.array([])

        # Hacemos las subdivisiones y vamos llamando a otra funcion interseccion
        return self.intersection(P, Q)

    def _box_overlap(self,P,Q):
        maxs_P,mins_P = np.amax(P,axis=0),np.amin(P,axis=0)
        maxs_Q,mins_Q = np.amax(Q,axis=0),np.amin(Q,axis=0)
        return ( (mins_P[0] < maxs_Q[0]) and (maxs_P[0] > mins_Q[0]) and (mins_P[1] < maxs_Q[1]) and (max_P[1] > mins_Q[1]) )

    def intersection(self, P, Q):
        if not self._box_overlap(P,Q):
            return np.array([])
        m = P.shape[0]
        n = Q.shape[0]
        


    def subdivision(self,P):
        N = P.shape[0] - 1
        #                       k    N  (x,y)
        compuesto =  np.zeros((N+1, N+1,  2)) 
        div1 = np.zeros((N+1,2))
        div2 = np.zeros((N+1,2))
        compuesto[0,:N+1,:] = P
        div1[0,:] = compuesto[0,N]
        for k in range(0, N):
            compuesto[k+1,0:N-k, :] = np.add( np.multiply( 0.5 , compuesto[k,0:N-k, :].transpose()),
                                                        np.multiply( 0.5 , compuesto[k,1:N-k+1,:].transpose()) ).transpose()
            div1[k+1,:] = compuesto[k+1,N-k-1,:]
        div2[:,:] = compuesto[:,0,:]
        return (div1,div2)

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
