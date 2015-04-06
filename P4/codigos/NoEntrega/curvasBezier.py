# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import binom
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D

class CurvaDeBezier:
    def __init__(self, polygon, bernstein):
        self.polygon = None
        self.N = -1
        
        # Variables de la clase
        self.num_points = 100
        self.t = np.linspace(0, 1, self.num_points)
        self.curve_x = None
        self.curve_y = None
        self.curve = None
        self._berstein = None
        self._casteljau = None
        self.compuesto = None

        self.div1 = None
        self.div2 = None

        # Variable que usamos para saber si usar bernstein o casteljau
        # Si esta variable es True, se usa bernstein. En caso contrario, Casteljau
        self.compute_bernstein = bernstein
        # Incializamos el poligono y precomputa si es necesario
        self.set_polygon(polygon)
     
        # Calculamos la curva de Bezier
        self.compute_curve() 
     
    def precompute_curve(self):
        # Inicializamos _bernstein y _casteljau como arrays de numpy. 
        # Estas variables seran las que guarden los valores computados
        #   por cada uno de los algoritmos respectivamente
        if self.compute_bernstein == True:
            self._bernstein = np.zeros((self.num_points,self.N + 1 ))
            self._compute_bernstein()
        else: 
            self._casteljau = np.zeros((self.num_points,self.num_points,self.num_points,2)) 

   
    # Calculos de los polinomios de Bernstein
    def _compute_bernstein(self):
        for i in range(self.N + 1):
            self._bernstein[:,i] = binom(self.N, i) * self.t**i *(1-self.t)**(self.N-i)

    def subdivision(self,P):
        N = P.shape[0] - 1
        #                       k   N  xy
        compuesto =  np.zeros((N+1,N+1,2)) 
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



    # Calculos mediante el algoritmo de Casteljau
    def _compute_casteljau(self):
        # Inicializamos la columna con los puntos del polinomio introducido
        self._casteljau[0,:,:self.N+1,:] = self.polygon
 
        
        # Para cada k, recalculamos la columna con los valores anteriores de la misma  
        for k in range(0, self.N):
            self._casteljau[k+1,:,0:self.N-k+2, :] = np.add( np.multiply( (1-self.t) , self._casteljau[k,:,0:self.N-k+2, :].transpose()),
                                                             np.multiply(  self.t   , self._casteljau[k,:,1:self.N-k+3,:].transpose()) ).transpose()
  
            # La linea anterior equivale a:
            # self._casteljau[:,0:self.N-k+2, :] = ((1-self.t)*self._casteljau[:,0:self.N-k+2, :].transpose() 
            #                           + (self.t*self._casteljau[:,1:self.N-k+3,:].transpose())).transpose()

            
    # Realizamos los calculos de (x,y) de la curva. 
    def compute_curve(self):
        if self.compute_bernstein == True:
            curve = np.dot(self._bernstein, self.polygon);
            self.curve_x = curve[:,0]
            self.curve_y = curve[:,1]
        else:
            self._compute_casteljau()
            self.subdivision(self.polygon)
            print "------------------------------------------"
            print self.compuesto
            self.curve_x = self._casteljau[self.N,:,0, 0]
            self.curve_y = self._casteljau[self.N,:,0, 1]
        
    # Devuelve el elemento para ser pintado
    def plot_bezier(self):
        self.curve = Line2D(self.curve_x, self.curve_y)
        return self.curve        

    # Computamos la nueva curva y devolvemos (x,y) actualizadas
    def update_bezier(self):
        self.compute_curve()
        return (self.curve_x,self.curve_y)

    # Cambiamos el poligono
    def set_polygon(self,poly):
        self.polygon = poly
        N_old = self.N
        # N es el numero de puntos - 1, lo usaremos en los
        # bucles, que iran de 0 a N, con N incluida
        self.N = poly.shape[0] - 1
        if N_old <> self.N: 
            # Hay distinto numero de puntos --> hay que precomputar
            self.precompute_curve()


