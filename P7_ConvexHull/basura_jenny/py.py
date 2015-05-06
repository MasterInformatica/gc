from __future__ import division
import numpy as np

def right_turn(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    
    

def menu(points):
    # Sort the points by x-coordinate, resulting in a sequence
    # p1,...,pn
    ordered_points = sorted(points)
    n = len(ordered_points)
    # Put the points p1 and p2 in a list Lupper, with p1 as the first
    # point
    Lupper = [ordered_points[0], ordered_points[1]]
    
    for i in range(2,n):
        Lupper.append(ordered_points[i])
        # while Lupper contains more than two points and the last
        # three points in Lupper do not make a right turn: delete the
        # middle of the last three points from Lupper
        while len(Lupper) > 2 and right_turn(Lupper[-3],
                                             Lupper[-2], Lupper[-1])<=0:
            Lupper.pop(-2) # We delete the middle of the last three
                           # points put the points pn and pn-1 in a
                           # list Llower, with pn as the first point
    print 'Lupper', Lupper
    Llower = [Lupper[-1], Lupper[-2]]
    for i in range(n-3, -1, -1): # for i<- n-2 downto 1 Append pi to
                                # Llower
        Llower.append(ordered_points[i])
        
        # while Llower contains more than 2 points and the last three
        # points in Llower do not make a right turn, deletethe middle
        # of the last three points from Llower.
        while len(Llower)>2 and right_turn(Llower[-3], Llower[-2],
                                           Llower[-1]) <= 0:
            Llower.pop(-2)
    Llower.pop(0) 
    Llower.pop(-1)
    print 'Llower', Llower
    list = Lupper + Llower
    return list

if __name__ == '__main__':
    points = [(1,2),(3,3),(5,6),(0,10),(3,5),(6,5),(0,9)]
    convex_hull = menu(points)
    print convex_hull
