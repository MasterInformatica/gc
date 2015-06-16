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
    caso = "NULL"

    maxK = H1.max_key()
    minK = H1.min_key()
    if point > maxK:
        #D: point is OUT and right the convex hull
        H1 = insertR(point, H1, +1, maxK, minK)
        H2 = insertR(point, H2, -1, maxK, minK)
    elif point < minK:
        #D: point is OUT and left the convex hull
        H1 = insertL(point, H1, +1, maxK, minK)
        H2 = insertL(point, H2, -1, maxK, minK)
    else:
        a = H1.floor_key(point)
        b = H1.ceiling_key(point)
        if side(a,b,point) > 0:
            # B: point is OUT and above the convexhull
            H1 = insert(point, H1, +1, maxK, minK)
        else:
            a = H2.floor_key(point)
            b = H2.ceiling_key(point)
            if side(a,b,point) < 0:
                # C: point is OUT and below the convexhull
                H2 = insert(point, H2, -1, maxK, minK)
            #else:
                # A: point is IN or ON the convexhull
                # nothing to do

def insertR(point,H,orientation,maxK,minK):
    u = H.prev_key(maxK) # left neig maxK
    while(u > minK and side(u,maxK,point)*orientation > 0): 
        # point is at left of edge u->maxK
        H.remove(u) # remove u
        u = H.prev_key(maxK) # new left neighbor of maxK
    if side(u,maxK,point)*orientation > 0:
        H.remove(maxK)

    H.insert(point,0)
    return H

def insertL(point,H,orientation,maxK,minK):
     y = H.succ_key(minK) # right neighbor of minK
     while(y < maxK and side(minK,y,point)*orientation > 0):
         # point is at left of edge minK->y
         H.remove(y) # remove y
         y = H.succ_key(minK) # new right neighbor of minK
     if side(minK,y,point)*orientation > 0:
        H.remove(minK)
     H.insert(point,0)
     return H


def insert(point,H,orientation,maxK,minK):
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
    if v == minK or w == maxK:
        H.insert(point,0)
    else:
        u = H.prev_key(v) # left neig v
        while(u > minK and side(u,v,point)*orientation > 0): 
            # point is at left of edge u->v
            H.remove(u) # remove u
            u = H.prev_key(v) # new left neighbor of v
        
        y = H.succ_key(w) # right neighbor of w
        while(y < maxK and side(w,y,point)*orientation > 0):
            # point is at left of edge w->y
            H.remove(y) # remove y
            y = H.succ_key(w) # new right neighbor of w
        H.insert(point,0)
    return H

def addpoint(point, H1, H2):
    ''' 
    Algorimo incremental de coste O(n*log(n))
    '''
    if len(H1) < 2:
        H1.insert(point,0)
        H2.insert(point,0)
        return H1,H2
    
    locate(point,H1,H2)

    return H1, H2






if __name__ == "__main__":
    points = [(0,0),(1,2),(2,2),(3,0),(1,1),(2,1),(2,-2)]
    #points = [(0,0),(2,0),(1,1)]
    H1 = bintrees.AVLTree()
    H2 = bintrees.AVLTree()
    for p in points:
        H1,H2 = addpoint(p,H1,H2)
        print "->",H1
        print H2
        print "-------------------------------"
