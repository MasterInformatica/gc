# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import binom
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D

class CurvaDeBezier:
    def __init__(self, polygon):
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
        self.compute_bernstein = True ########## CAMBIAR VALOR a False para computar por Casteljau ##########

        # Inicializamos _bernstein y _casteljau como arrays de numpy. 
        # Estas variables seran las que guarden los valores computados
        #   por cada uno de los algoritmos respectivamente
        if self.compute_bernstein == True:
            self._bernstein = np.zeros((self.N + 1, self.num_points))
            self._compute_bernstein() 
        else: 
            self._casteljau = np.zeros((self.num_points,self.num_points,self.num_points,2)) 
            self._compute_casteljau()
        
        # Calculamos la curva de Bezier
        self.compute_curve() 
        
    # Calculos de los polinomios de Bernstein
    def _compute_bernstein(self):
        for i in range(self.N + 1):
            self._bernstein[i, :] = binom(self.N, i) * self.t**i *(1-self.t)**(self.N-i)

    # Calculos mediante el algoritmo de Casteljau
    def _compute_casteljau(self):
        # Inicializamos la primera columna con los puntos del polinomio introducido
        self._casteljau[0,:,:self.N+1,:] = self.polygon
        
        # Vamos rellenando el array por columnas, ya que cada b_i^k depende de la
        # columna anterior
        for k in range(0, self.N):
            for i in range(0,self.N-k+1):
                self._casteljau[k+1,:,i, 0] = (1-self.t)*self._casteljau[k,:,i, 0] + self.t*self._casteljau[k,:,i+1,0]
                self._casteljau[k+1,:,i, 1] = (1-self.t)*self._casteljau[k,:,i, 1] + self.t*self._casteljau[k,:,i+1,1]
        
    
    # Realizamos los calculos de (x,y) de la curva. 
    # Si compute_bernstein es False, asignamos a nuestra curva las soluciones dadas
    # por Casteljau.
    def compute_curve(self):
        if self.compute_bernstein == True:
            self.curve_x = sum(self.polygon[i, 0] * self._bernstein[i, :] for i in range(self.N + 1))
            self.curve_y = sum(self.polygon[i, 1] * self._bernstein[i, :] for i in range(self.N + 1))
        else:
            self.curve_x = self._casteljau[self.N,:,0, 0]
            self.curve_y = self._casteljau[self.N,:,0, 1]
        
    
    def plot_bezier(self):
        self.curve = Line2D(self.curve_x, self.curve_y)
        return self.curve        

    # Computamos la nueva curva y devolvemos (x,y) actualizadas
    def update_bezier(self):
        self.compute_curve()
        return (self.curve_x,self.curve_y)
        
        
