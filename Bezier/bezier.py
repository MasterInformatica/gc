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
        
        self.curve_x = None
        self.curve_y = None
        
        self._bernstein = np.zeros((self.N, self.num_points))
        self._compute_bernstein()
        self.plot_bezier()
        
    def _compute_bernstein(self):
        for i in range(self.N + 1):
            self._bernstein[i, :] = binom(self.N, i) * self.t**i *(1-self.t)**(self.N-i)
    
    def compute_curve(self):
        self.curve_x = sum(self.polygon[:, 0] * self._bernstein[i, :] for i in range(self.N + 1))
        self.curve_y = sum(self.polygon[:, 1] * self._bernstein[i, :] for i in range(self.N + 1))
        
    def plot_bezier(self):
        self.curve = Line2D(self.curve_x, self.curve_y)
        
        return self.curve        
        #self.ax.add_line(self.curve)
        #self.fig.canvas.draw()
        
        
