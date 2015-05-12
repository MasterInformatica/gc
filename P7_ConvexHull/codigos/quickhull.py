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
    return points[np.argmax(distance(a,b,points))]

def distance(A, B, P):
    """ segment line AB, point P, where each one is an array([x, y]) """

    if np.arccos(np.dot((P - A) / np.norm(P - A), (B - A) / np.norm(B - A))) > np.pi / 2:
        return np.norm(P - A)
    if np.arccos(np.dot((P - B) / np.norm(P - B), (A - B) / np.norm(A - B))) > np.pi / 2:
        return np.norm(P - B)
    return np.abs(np.dot(A - B, P[::-1]) + np.det([A, B])) / np.norm(A - B) 

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
        A,X = right_Points(a,c,points)
        B,X = right_Points(c,b,points)
        return _quickHull(a,c,A)+[c]+_quickHull(c,b,B)

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
    
def convex_hull(points):
    m,M =extremos(points)
    A,B = right_Points(m,M,points)
    return [m]+_quickHull(m,M,A)+[M]+_quickHull(M,m,B)+[m]


if __name__ == "__main__":
    points  = [[1,0],[-1,0],[1,1],[1,0],[-1,0],[1,1]]
    print convex_hull( points)
