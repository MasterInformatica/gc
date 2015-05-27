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

def side(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

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
    #get the edge E or vertex V whose horizontal span includes point 
    a = H.floor_key(point)
    b = H.ceiling_key(point)
    if a[0] == point[0]:
        b = a
    elif b[0] == point[0]:
        a = b
    v = a # left point of edge E or vertex V
    w = b # right point of edge E or vertex V

    u = H.prev_key(v) # left neig v
    while(side(u,v,point)*orientation > 0): # point is at left of edge u->v
        H.remove(u) # remove u
        u = H.prev_key(v) # new left neighbor of v
        
    y = H.succ_key(w) # right neighbor of w
    while(side(w,y,point)*orientation > 0): # point is at left of edge w->y
        H.remove(y) # remove y
        y = H.succ_key(w) # new right neighbor of w
    H.insert(point,0)
    return H

def addpoint(point, H1, H2):
    ''' 
    Algorimo incremental de coste O(n*log(n))
    '''
    caso = locate(point,H1,H2)
    
    # if caso == A:
        # A: point is IN or ON the convexhull
        # nothing to do
    if caso == "B" or caso == "D": 
        # B: point is OUT and above the convexhull
        # caso == D: point is OUT and left or right the convex hull
        H1 = insert(point, H1, -1)
    if caso == "C" or caso == "D":
        # C: point is OUT and below the convexhull
        # caso == D: point is OUT and left or right the convex hull
        H2 = insert(point, H2, +1)
    return H1, H2






if __name__ == "__name__":
    points = [(0,0),(1,2),(2,2),(3,0),(1,1),(2,1),(2,-2)]
    H1 = bintrees.AVLTree()
    H2 = bintrees.AVLTree()
    for p in points:
        H1,H2 = addpoint(p,H1,H2)
