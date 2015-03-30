# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
from matplotlib.widgets import Slider, Button

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


        m = P.shape[0]-1 #apunta al ultimo indice accesible
        #Delta2(b_i) = b_(i+2) - 2 b_(i+1) + b_i     i=0...m-2
        b =           P[2:m+1] - 2*P[1:m]  + P[0:m-1]
        B = np.linalg.norm(b, axis=1)
        if ((m*(m-1)*np.amax(B)) > self.epsilon):
            P1, P2 = self._subdivision(P)
            ####
            # ARREGLAR: Aquí habría que coger solo los que no son duplicados
            #           y no hacer tantos if, usar el concatenate/append de
            #           alguna forma inteligente
            ###
            intersec_points1 = self.intersection(P1,Q)
            intersec_points2 = self.intersection(P2,Q)

            if(intersec_points1.shape[0] == 0): #array vacio
                return intersec_points2
            elif(intersec_points2.shape[0] == 0):
                return intersec_points1
            else:
                return np.concatenate((intersec_points1, intersec_points2), axis=0)


        n = Q.shape[0]-1
        b = Q[2:n+1] - 2*Q[1:n] + Q[0:n-1]
        B = np.linalg.norm(b, axis=1)
        #if np.random.rand() > 0.99:
        if (n*(n-1)*np.amax(B)) > self.epsilon:
            Q1, Q2 = self._subdivision(Q)
            ####
            # ARREGLAR: Aquí habría que coger solo los que no son duplicados
            #           y hacerlo de una forma inteligente igual que el caso 
            #           anterior con P
            ###
            intersec_points1 = self.intersection(P,Q1)
            intersec_points2 = self.intersection(P,Q2)
            if(intersec_points1.shape[0] == 0): #array vacio
                return intersec_points2
            elif(intersec_points2.shape[0] == 0):
                return intersec_points1
            else:
                return np.concatenate((intersec_points1, intersec_points2), axis=0)

        return self._intersect_segment(P[0],P[m],Q[0],Q[n])


    def plot(self, k=3):
        # Metodo que produce el dibujo de las curvas y las
        # intersecciones.
        if(self.window == None):
            self.window = Graphicalica()
        else:
            self.window.clean()

        
        self._plot(self.P,k,'b')
        self._plot(self.Q,k,'r')
        self.window.drawPoints(self.intersection_points,'g')
        self.window.show()


    def interactive(self):
        self.window = Graphicalica()
        self.window.init_interaction(self)
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
            return np.array([])

        # falta calcular el punto de corte!
        line1 = np.cross([A[0],A[1],1], [B[0],B[1],1])
        line2 = np.cross([C[0],C[1],1], [D[0],D[1],1])
       #  print 'l1', line1
        # print 'l2', line2

        intersect_point = np.cross(line1, line2)
        #print 'inters', intersect_point
        return np.array([[intersect_point[0]/intersect_point[2], intersect_point[1]/intersect_point[2]]])
        
        
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
            self.window.drawLine(Line2D(P[:,0],P[:,1], color=colour))
        else:
            div1, div2 = self._subdivision(P)
            self._plot(div1, k-1, colour)
            self._plot(div2, k-1, colour)
            

#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
   
class Graphicalica:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, aspect=1)
        self.ax.set_xlim(-20,20)
        self.ax.set_ylim(-20,20)
        

    def init_interaction(self, bezier):
        self.bezier = bezier
        self.k = 3
        self.eps = 0.1

        plt.subplots_adjust(bottom=0.25)

        # Sliders
        epsAxes = plt.axes([0.20, 0.15, 0.4, 0.03])        
        kAxes = plt.axes([0.20, 0.1, 0.4, 0.03])

        self.epsSlider = Slider(epsAxes, 'eps: ', 0.001, 1.00, valinit=0.1, valfmt=u'%1.3f')
        self.kSlider   = Slider(kAxes, 'k: ', 0, 6, valinit=3, valfmt=u'%0.0f')

        self.epsSlider.on_changed(self._updateEps)        
        self.kSlider.on_changed(self._updateK)

        #Buttons
        calculateAxes = plt.axes([0.7, 0.15, 0.15, 0.03])
        resetAxes = plt.axes([0.7, 0.1, 0.15, 0.03])

        self.buttonCalculate = Button(calculateAxes, 'Calculate!')
        self.buttonReset = Button(resetAxes, 'Reset!')

        self.buttonCalculate.on_clicked(self._updatePlot)

    def _updateEps(self, val):
        print val
        self.eps = val
    def _updateK(self,val):
        print val
        self.k = int(val)

    def _updatePlot(self, event):
        cuts = np.array([])
        N = 5
        while (cuts.shape[0] != 3):
            P = np.random.uniform(-20, 20, (N + 1, 2))
            Q = np.random.uniform(-20, 20, (N + 1, 2))
            cuts = self.bezier(P, Q, self.eps) #Llamada al __call__ de la clase

        self.bezier.plot(k=self.k)


    def drawLine(self,line):
        self.ax.add_line(line)
        self.fig.canvas.draw()

    def drawPoints(self,points,colour):
        if points.shape[1] != 0:
            for p in points:
                self.ax.add_patch(Circle((p[0],p[1]),0.3))
        self.fig.canvas.draw()

    def show(self):
        plt.show()

    def clean(self):
        pass
        
if __name__ == '__main__':
    N = 5  
    epsilon = 0.001

    # Instancia de la clase
    intersect = IntersectionBezier()
    
    intersect.interactive();

    # # Puntos aleatorios para generar las curvas de Bezier
    # cuts = np.array([])
    # while (cuts.shape[0] < 3):
    #     P = np.random.uniform(-20, 20, (N + 1, 2))
    #     Q = np.random.uniform(-20, 20, (N + 1, 2))
    #     cuts = intersect(P, Q, epsilon) # Llamada al __call__ de la clase

    # intersect.plot()

