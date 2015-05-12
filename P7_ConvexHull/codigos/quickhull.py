# -*- coding: utf-8 -*-

""" 
Práctica 7 de Geometría Computacional
Autores:
* Luis María Costero Valero       (lcostero@ucm.es)
* Jesús Javier Doménech Arellano  (jdomenec@ucm.es)
* Jennifer Hernández Bécares      (jennhern@ucm.es)
"""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

def maxDistancePoint(a,b,points):
    return points[0]

def right_turn(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    
def right_Points(a,b,points):
    R = []
    L = []
    for p in points:
        # v = right_turn(a,b,p)
        v = (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
        if(v<0):
            R.append(p)
        elif(v>0):
            L.append(p)
    return R,L

def _quickHull(a,b,points):
    if(len(points)<=1):
        return points
    else:
        c = maxDistancePoint(a,b,points)
        print c
        A,_ = right_Points(a,c,points)
        B,_ = right_Points(c,b,points)
        return _quickHull(a,c,A)+c+_quickHull(c,b,B)

def extremos(points):
    maxp = points[0]
    minp = points[0]
    for p in points:
        # calculo maximo
        if p[0] > maxp[0] or (p[0]==maxp[0] and p[1] < maxp[1]):
            maxp = p
            continue
        # calculo minimo
        if p[0] < minp[0] or (p[0]==minp[0] and p[1] > minp[1]):
            minp = p
    return (minp,maxp)
    
def quickHull(points):
    m,M =extremos(points)
    A,B = right_Points(m,M,points)
    print m, M
    return [m]+_quickHull(m,M,A)+[M]+_quickHull(M,m,B)

if __name__ == '__main__':
    # print right_Points([0,0],[4,0],[[1,1],[2,1],[1,-1],[2,-1],[2,0]])
    print quickHull( [[-1, 0], [1, 0], [1, 1], [-1, 0], [1, 0], [1, 1]])
