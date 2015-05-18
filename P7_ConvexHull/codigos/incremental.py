# -*- coding: utf-8 -*-

""" 
Práctica 7 (Alg. incremental) de Geometría Computacional
Autores:
* Luis María Costero Valero       (lcostero@ucm.es)
* Jesús Javier Doménech Arellano  (jdomenec@ucm.es)
* Jennifer Hernández Bécares      (jennhern@ucm.es)
"""

from __future__ import division
import numpy as np



class incremental:
    def __init__(self):
        self.covex_hull = []
        
    def __init__(self, points):
        assert len(points)<=3, "El construtor acepta como maximo 3 puntos"
        if(len(points<=2):
           self.convex_hull = np.array(sorted(points))
        else:
           p=np.array(sorted(points))
           self.convex_hull = np.concatenate((p, [p[0]]))
           

    def __call__(self, p):
        " inserta un punto en la concex hull, y la devuelve"
        # recorremos la convex hull para mirar si el punto esta dentro o fuera. 
        # Aprovechamos para buscar los puntos de tangencia a la vez.

        idx_sup = -1
        idx_inf = -1

        for i in range(0,self.convex_hull.shape[0]):
           # esta ordenado en sentido horario:
           # El punto de tng superior coresponde con:
           #   (i-1) -> (i)   a la dcha
           #   (i) -> (i+1)   a la izq

           # El pundo de tng inferior corresponde con:
           #  (i-1) -> (i)   a la izq
           #  (i) -> (i+1)   a la dcha
           




    def side(self, a, b, P):
           " Devuelve el signo del lado de P respecto a la recta formada
           por ab"
           return (b[0]-a[0])*(P[:,1]-a[1])-(b[1]-a[1])*(P[:,0]-a[0])

                
