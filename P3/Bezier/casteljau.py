# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import binom
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D

class CurvaDeBezier:
    def __init__(self, polygon, bernstein, stuff):
        self.polygon = polygon
        
        # Inicializamos N como el numero de puntos - 1, ya que lo usaremos en los
        # bucles, que iran de 0 a N, con N incluida
        self.N = polygon.shape[0] - 1
        
        # Inicializaciones varias
        self.num_points = 100
        self.t = np.linspace(0, 1, self.num_points)
        self.curve_x = None
        self.curve_y = None
        self.curve = None

        # Variable que usamos para saber si usar bernstein o casteljau
        # Si esta variable es True, se usa bernstein. En caso contrario, Casteljau
        self.compute_bernstein = bernstein

        # Inicializamos _bernstein y _casteljau como arrays de numpy. 
        # Estas variables seran las que guarden los valores computados
        #   por cada uno de los algoritmos respectivamente
        if self.compute_bernstein == True:
            if __name__ == '__main__' or stuff == None:
                self._bernstein = np.zeros((self.num_points,self.N + 1 ))
                self._compute_bernstein()
            else:
                # Si nos llaman desde test_P3, usamos los valores de 
                # bernstein que ya teniamos precalculados
                self._bernstein = np.zeros((self.N + 1, self.num_points))
                self._bernstein = stuff
        else: 
            self._casteljau = np.zeros((self.num_points,self.num_points,2)) 
            self._compute_casteljau()
        
        # Calculamos la curva de Bezier
        self.compute_curve() 
        
    # Calculos de los polinomios de Bernstein
    def _compute_bernstein(self):
        for i in range(self.N + 1):
            self._bernstein[:,i] = binom(self.N, i) * self.t**i *(1-self.t)**(self.N-i)



    # Calculos mediante el algoritmo de Casteljau
    def _compute_casteljau(self):
        # Inicializamos la primera columna con los puntos del polinomio introducido
        self._casteljau[:,:self.N+1,:] = self.polygon
        
        # Vamos rellenando el array por columnas, ya que cada b_i^k depende de la
        # columna anterior
        
        for k in range(0, self.N):
            self._casteljau[:,0:self.N-k+2, :] = ((1-self.t)*self._casteljau[:,0:self.N-k+2, :].transpose() + (self.t*self._casteljau[:,1:self.N-k+3,:].transpose())).transpose()
            
    # Realizamos los calculos de (x,y) de la curva. 
    # Si compute_bernstein es False, asignamos a nuestra curva las soluciones dadas
    # por Casteljau.
    def compute_curve(self):
        if self.compute_bernstein == True:
            curve = np.dot(self._bernstein, self.polygon);
            self.curve_x = curve[:,0]
            self.curve_y = curve[:,1]
            #self.curve_x = np.sum(np.multiply(self.polygon[:,0],(self._bernstein)),axis=1)
            #self.curve_y = np.sum(np.multiply(self.polygon[:,1],(self._bernstein)),axis=1)
        else:
            self.curve_x = self._casteljau[:,0, 0]
            self.curve_y = self._casteljau[:,0, 1]
        
    
    def plot_bezier(self):
        self.curve = Line2D(self.curve_x, self.curve_y)
        return self.curve        

    # Computamos la nueva curva y devolvemos (x,y) actualizadas
    def update_bezier(self):
        self.compute_curve()
        return (self.curve_x,self.curve_y)
        
# Funcion equivalente a _compute_bernstein, que se usa para llamarla 
# externamente sin una instancia de CurvaDeBezier.
# En nuestro caso, se llama desde el main de test_P3        
def compute_bernstein_precomp(N, t, bernstein):
    for i in range(N + 1):
        bernstein[:,i] = binom(N, i) * t**i *(1-t)**(N-i)
    return bernstein
