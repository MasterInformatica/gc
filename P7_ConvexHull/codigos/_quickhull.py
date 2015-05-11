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

def maxDistancePoint(a,b,points):
#    P = np.array(points)
    maxP = [0,0]
    maxVal = -3

    #Nota: nos da igual la distancia, solamente el que esta mas alejado,
    #por eso no dividimos entre la norma
    for p in points:
        m = np.linalg.det([[b-a],[p-a]]) # / np.norm(a,b)
        if m > maxVal:
            maxP = p
            maxVal = m
            

    #    D = np.linalg.det(np.array([[b-a],[P-a]]))
    #    print D
    #    return np.max(D/np.norm(a,b))
    return maxP


def rigth_Points(a,b,points):
    pass

def _quickHull(a,b,points):
    if(len(points)<=1):
        return points
    else:
        c = maxDistancePoint(a,b,points)
        print c 
        A = right_Points(a,c,points)
        B = right_Points(c,b,points)
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
    A = right_Points(m,M,points)
    B = right_Points(M,m,points)
    return [m]+_quickHull(m,M,A)+[M]+_quickHull(M,m,B)

if __name__ == '__main__':
    quickHull( [[-1, 0], [1, 0], [1, 1], [-1, 0], [1, 0], [1, 1]])
