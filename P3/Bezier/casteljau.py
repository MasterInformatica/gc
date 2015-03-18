# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import binom
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D

class CurvaDeBezier:
    def __init__(self, polygon):
        self.polygon = polygon
        self.N = polygon.shape[0] - 1
        
        self.num_points = 100
        self.t = np.linspace(0, 1, self.num_points)
        # quitar esto
        self.t2 = np.array(self.t)

        self.curve_x = None
        self.curve_y = None
        self.curve = None
        self._bernstein = np.zeros((self.N + 1, self.num_points))
        self._casteljau = np.zeros((self.N + 1, self.num_points, 2)) #FIXME
        #self._compute_bernstein() # 
        self._compute_casteljau()
        #self.compute_curve() # for Bernstein
        
        #self.plot_bezier()
        
    def _compute_bernstein(self):
        for i in range(self.N + 1):
            self._bernstein[i, :] = binom(self.N, i) * self.t**i *(1-self.t)**(self.N-i)

    def _compute_casteljau(self):
        print 'self.polygon', self.polygon
        self._casteljau[:, 0] = self.polygon
        print 'self.castel[:,0]',self._casteljau[:,0]
        for j in range(0, self.N):
            for i in range(0, self.N - j):
                self._casteljau[i,j+1] = (1-self.t2)*self._casteljau[i, j,:] + self.t2*self._casteljau[i+1, j,:]
        print self._casteljau
        
    
    def compute_curve(self):
        self.curve_x = sum(self.polygon[i, 0] * self._bernstein[i, :] for i in range(self.N + 1))
        self.curve_y = sum(self.polygon[i, 1] * self._bernstein[i, :] for i in range(self.N + 1))
        
    def plot_bezier(self):
        self.curve = Line2D(self.curve_x, self.curve_y)
         
        return self.curve        

    def update_bezier(self):
        self.compute_curve()
        return (self.curve_x,self.curve_y)
        #self.ax.add_line(self.curve)
        #self.fig.canvas.draw()
        
        
