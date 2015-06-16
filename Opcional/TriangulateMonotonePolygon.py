# -*- coding: utf-8 -*-

""" 
Práctica Opcional de Geometría Computacional
Triangulación de poligonos Y-monotonos
Autores:
* Luis María Costero Valero       (lcostero@ucm.es)
* Jesús Javier Doménech Arellano  (jdomenec@ucm.es)
* Jennifer Hernández Bécares      (jennhern@ucm.es)
"""

from __future__ import division
import bintrees
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
from matplotlib.path import Path
from matplotlib.widgets import Slider, Button
import matplotlib.patches as patches
import numpy as np


class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def top(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

@total_ordering
class Point:
    def __init__(self,x,y,chain):
        self.x = x
        self.y = y
        self.chain = chain
    
    def __eq__(self,P):
        return self.x == P.x and self.y == P.y

    def __lt__(self,P):
        return self.x < P.x or (self.x == P.x and self.y < P.y)

def triangulateMonotonePolygon(points):
    '''
    Triangulate Y-Monotone Polygons
    '''
    #Meger all vertices of P into one seq sorted on decreasing y
    Ps= sorted(points)
    diags = []
    #init an stack with u1 and u2
    S = Stack()
    S.push(Ps[0])
    S.push(Ps[1])
    n = len(Ps)
    for j in range(2,n-1):
        if Ps[j].chain == S.top().chain:
            v = S.pop()
            while not S.isEmpty() and visible(S.top(),Ps[j]):
                v = S.pop()
                diags = diags + [(Ps[j],v)]
            S.push(v)
        else:
            v = S.pop()
            while not S.isEmpty():
                diags = diags + [(Ps[j],v)]
                v = S.pop()
            S.push(Ps[j-1])
        S.push(Ps[j])
    while not S.isEmpty():
        diags = diags + [(Ps[-1],S.pop())]

    return diags
