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
        self.intersection_points = None
        self.epsilon = None
        self.P = None
        self.Q = None

    def __call__(self, P, Q, epsilon):
        # P.shape = (n, 2)
        # Q.shape = (m,2)
        # Epsilon controlara si se aproxima el poligono 
        #   de control mediante un segmento
        self.epsilon = epsilon
        self.P = P
        self.Q = Q

        # Calculamos interseccion
        self.intersection_points = self.intersection(P, Q)
        # Returns: K puntos de interseccion calculados como un array
        # de numpy de dimensiones (K, 2)
        return self.intersection_points

    
    def intersection(self, P, Q):
        if not self._boxes_overlap(P,Q):
            return np.array([])
        m = P.shape[0]-1
        if (m*(m-1)*np.max(np.linalg.norm(P[0:m-2]+P[2:m],axis=1))) > self.epsilon:
            P1,P2 = self._subdivision(P)
            intersec_points = self.intersection(P1,Q)
            return np.concatenate(intersec_points,self.intersection(P2,Q))
        n = Q.shape[0]-1
        if (n*(n-1)*np.max(np.linalg.norm(Q[0:n-2]+Q[2:n],axis=1))) > self.epsilon:
            Q1,Q2 = self._subdivision(Q)
            intersec_points = self.intersection(P,Q1)
            return np.concatenate(intersec_points,self.intersection(P,Q2))
        return self._intersect_segment(P[0],P[m],Q[0],Q[n])


    def plot(self, k=3):
        # Metodo que produce el dibujo de las curvas y las
        # intersecciones.
        if k == 0:
        pass

    # PRIVATE METHODS #
    #-----------------#

    def _boxes_overlap(self,P,Q):
        maxs_P,mins_P = np.amax(P,axis=0),np.amin(P,axis=0)
        maxs_Q,mins_Q = np.amax(Q,axis=0),np.amin(Q,axis=0)
        return ( (mins_P[0] < maxs_Q[0]) and (maxs_P[0] > mins_Q[0]) and (mins_P[1] < maxs_Q[1]) and (max_P[1] > mins_Q[1]) )
    
    def _side(self,A,B,C):
        # X - Y > 0 ==> X > Y
        return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

    def _intersect_segment(self,A,B,C,D):
        # segmento A-B y C-D
        #comprobamos que se cortan:
        if ((self._side(A,C,D) and self._side(B,C,D)) 
            or (self._side(A,B,C) and self._side(A,B,D))):
            return np.array([])

        # falta calcular el punto de corte!
        pass # devolver el punto en un numpy array
        
    def _subdivision(self,P):
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
        




class Graphic:
    def __init__(self):
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
