# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle

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
        print self.intersection_points
        # Returns: K puntos de interseccion calculados como un array
        # de numpy de dimensiones (K, 2)
        return self.intersection_points

    
    def intersection(self, P, Q):
        if not self._boxes_overlap(P,Q):
            return np.array([[]])
        m = P.shape[0]-1
        b = P[0:m+1]-2*np.concatenate((P[1:m+1],[[0,0]]),axis=0)+np.concatenate((P[2:m+1],[[0,0],[0,0]]),axis=0)
        print "-",b
        B= np.linalg.norm(b,axis=1)# 
        print "*",B
        print P
        print "----"
        print Q
        print "----***"
        if np.random.rand() > 0.99:                  
        #if ((m*(m-1)*np.amax(B)) > self.epsilon):
            print "DENTRO"
            P1,P2 = self._subdivision(P)
            print "P1-Q"
            intersec_points = self.intersection(P1,Q)
            print "P2-Q"
            return np.concatenate((intersec_points,self.intersection(P2,Q)))
        n = Q.shape[0]-1
        if np.random.rand() > 0.99:
        #if (n*(n-1)*np.amax(np.linalg.norm(Q[0:n-2]+Q[2:n],axis=1))) > self.epsilon:
            Q1,Q2 = self._subdivision(Q)
            print "P-Q1"
            intersec_points = self.intersection(P,Q1)
            print "P-Q2"
            return np.concatenate((intersec_points,self.intersection(P,Q2)))
        print "holi"
        return self._intersect_segment(P[0],P[m],Q[0],Q[n])


    def plot(self, k=3):
        # Metodo que produce el dibujo de las curvas y las
        # intersecciones.
        self.window = Graphicalica()
        self._plot(self.P,k,'b')
        self._plot(self.Q,k,'r')
        self.window.drawPoints(self.intersection_points,'g')
        self.window.show()
    # PRIVATE METHODS #
    #-----------------#

    def _boxes_overlap(self,P,Q):
        maxs_P,mins_P = np.max(P,axis=0),np.min(P,axis=0)
        maxs_Q,mins_Q = np.amax(Q,axis=0),np.amin(Q,axis=0)
        return ( (mins_P[0] < maxs_Q[0]) and (maxs_P[0] > mins_Q[0]) and (mins_P[1] < maxs_Q[1]) and (maxs_P[1] > mins_Q[1]) )
    
    def _side(self,A,B,C):
        # X - Y > 0 ==> X > Y
        return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

    def _intersect_segment(self,A,B,C,D):
        # segmento A-B y C-D
        #comprobamos que se cortan:
        if ((self._side(A,C,D) and self._side(B,C,D)) 
            or (self._side(A,B,C) and self._side(A,B,D))):
            return np.array([[]])

        # falta calcular el punto de corte!
        return np.array([[0,0]])
        
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
        
    def _plot(self,P,k,colour):
        if k == 0:
            self.window.drawLine(Line2D(P[:,0],P[:,1]))
        else:
            div1,div2 = self._subdivision(P)
            self._plot(div1, k-1,colour)
            self._plot(div2, k-1,colour)
            
            
class Graphicalica:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, aspect=1)
        self.ax.set_xlim(-20,20)
        self.ax.set_ylim(-20,20)
        
    def drawLine(self,line):
        self.ax.add_line(line)
        self.fig.canvas.draw()

    def drawPoints(self,points,colour):
        for p in points:
            self.ax.add_patch(Circle((p[0],p[1]),0.3))
        self.fig.canvas.draw()

    def show(self):
        plt.show()

        
if __name__ == '__main__':
    N = 15  
    epsilon = 0.1

    # Instancia de la clase
    intersect = IntersectionBezier()
    
    # Puntos aleatorios para generar las curvas de Bezier
    P = np.random.uniform(-20, 20, (N + 1, 2))
    Q = np.random.uniform(-20, 20, (N + 1, 2))
    points = [[0,0],[20,0],[20,20]]
    P = np.array(points)
    points = [[0,0],[20,0],[20,20]]
    Q = np.array(points)
    intersect(P, Q, epsilon) # Llamada al __call__ de la clase

    intersect.plot(0)
