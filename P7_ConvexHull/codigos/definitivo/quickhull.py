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

def maxDistancePoint(a,b,P):
    return P[np.argmax((b[0]-a[0])*(P[:,1]-a[1])-(b[1]-a[1])*(P[:,0]-a[0]))]

def _quickHull(a,b,P):
    if(P.shape[0]<=1):
        return P
    else:
        c = maxDistancePoint(a,b,P)
        A = left_points(a,c,P)
        B = left_points(c,b,P)
        return np.vstack((_quickHull(a,c,A),c,_quickHull(c,b,B)))

def left_points(a,b,P):
    dist = (b[0]-a[0])*(P[:,1]-a[1])-(b[1]-a[1])*(P[:,0]-a[0])
    return P[dist > 0]

def separar(a,b,P):
    dist = (b[0]-a[0])*(P[:,1]-a[1])-(b[1]-a[1])*(P[:,0]-a[0])
    return P[dist > 0],P[dist < 0]

def convex_hull(points):
    P = np.array(sorted(points))
    m,M = P[0],P[-1]
    L,R = separar(m,M,P)
    return np.vstack((m,_quickHull(m,M,L),M,_quickHull(M,m,R),m))
                
