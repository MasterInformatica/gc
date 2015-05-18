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


class Incremental:
    def __init__(self):
        self.convex_hull = None
           

    def __call__(self, p):
        ''' inserta un punto en la concex hull, y la devuelve'''
        if self.convex_hull is None:
            self.convex_hull = np.array([p,p])
            return self.convex_hull
        elif self.convex_hull.shape[0] <=3: # 2 ptos + 1 duplicado
            self.convex_hull = self.convex_hull[1:] #eliminamos el primer punto que está duplicado
            self.convex_hull = np.concatenate((self.convex_hull,[p]))
            self.convex_hull = np.array(sorted(self.convex_hull.tolist()))
            self.convex_hull = np.concatenate((self.convex_hull, [self.convex_hull[0]]))
            return self.convex_hull
                                              
        # El algoritmo está formado por dos partes:
        #  (a) Detectar si el punto se encuentra dentro de la convex hull o
        #       fuera. A la vez se puede detectar (en el caso de estar fuera), los
        #       puntos de tangencia (los que cambia el signo del lado).
        #  (b) En el caso de estar el punto en el exterior de la convex hull, añadir 
        #       los segmentos de tangencia con el nuevo punto, y eliminar el trozo de
        #       convex hull que sobra
        
        
        #eliminar el ultimo punto que está repetido
        self.convex_hull = self.convex_hull[1:] #eliminamos el primer punto que está duplicado

        print "CH: ", self.convex_hull
        # (a) Detectar dentro/fuera + puntos de tangencia
        idx_inf = -1
        idx_sup = -1
        
        tam = self.convex_hull.shape[0]
        for i in range(0, tam):
            # esta ordenado en sentido horario:
            # El punto de tng superior coresponde con:
            #   (i-1) -> (i)   a la dcha
            #   (i) -> (i+1)   a la izq
        
            # El pundo de tng inferior corresponde con:
            #  (i-1) -> (i)   a la izq
            #  (i) -> (i+1)   a la dcha
            
            print ".........."
            print self.convex_hull[i-1], self.convex_hull[i]
            print self.convex_hull[i], self.convex_hull[(i+1)%tam]
            print "----------"

            side1 = self._side(self.convex_hull[i-1], self.convex_hull[i], p)
            side2 = self._side(self.convex_hull[i], self.convex_hull[(i+1)%tam], p)

            print "sides: ", side1, side2
            if side1*side2 < 0: #son distintos
                if side1 > 0: 
                    idx_sup = i
                elif side1 < 0:
                    idx_inf = i

        print "idxs:", idx_sup, idx_inf
            
        # (b) Si hay puntos de tangencia, formar la nueva convex hull
        if idx_sup >= 0:
            print "AAA"
            if idx_inf > idx_sup: #se llega al final en mitad
                self.convex_hull=np.concatenate((self.convex_hull[idx_sup:idx_inf+1], [p]))
            else:
                self.convex_hull=np.concatenate((self.convex_hull[0:idx_inf+1], [p], self.convex_hull[idx_sup:tam]))
                

        self.convex_hull = np.concatenate((self.convex_hull, [self.convex_hull[0]]))
        return self.convex_hull

    def _side(self, a, b, P):
        " Devuelve el signo del lado de P respecto a la recta por ab"
        return (b[0]-a[0])*(P[1]-a[1])-(b[1]-a[1])*(P[0]-a[0])
            
            
                

