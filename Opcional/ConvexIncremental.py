# -*- coding: utf-8 -*-

""" 
Práctica Opcional de Geometría Computacional
ConvexHull Incremental algorithm with cost nlogn
Autores:
* Luis María Costero Valero       (lcostero@ucm.es)
* Jesús Javier Doménech Arellano  (jdomenec@ucm.es)
* Jennifer Hernández Bécares      (jennhern@ucm.es)
"""

from __future__ import division
import bintrees

def locate(point, H1, H2):
    ''' 
    determine the position of point respect the convex
    and return the case and the segment
    '''
    pass

def insert(point,H,orientation):
    '''
    insert point in H.
    orientation is -1 or +1, depends on H being the upper tree or the other respectively
    '''
    get the edge E or vertex V whose horizontal span includes point of H
    v = left point of edge E or vertex V
    u = left neighbor of v
    while(side(u,v,point)*orientation > 0): # point is at left of edge u->v
        remove u
        u = new left neighbor of v
        
    w = right point of edge E or vertex V
    y = right neighbor of w
    while(side(w,y,point)*orientation > 0): # point is at left of edge w->y
        remove y
        y = new right neighbor of w
    H.add(point)
    return H

def addpoint(point, H1, H2):
    ''' 
    Algorimo incremental de coste O(n*log(n))
    '''
    caso = locate(point,H1,H2)
    
    # if caso == A: # point is IN or ON the convexhull
    # nothing to do
    # caso == D: point is OUT and left or right the convex hull
    if caso == B or caso == D: # B: point is OUT and above the convexhull
        H1 = insert(point, H1, -1)
    if caso == C or caso == D: # C: point is OUT and below the convexhull
        H2 = insert(point, H2, +1)
    return H1, H2
