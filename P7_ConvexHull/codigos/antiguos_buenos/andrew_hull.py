from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
def right_turn(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    
    

def convex_hull(points):

    
    ordered_points = sorted(points) # Ordenamos los puntos Construimos
    # el lower hull comprobando cada vez si tenemos un right turn
    # entre los ultimos tres puntos o no
    Llower = []
    for p in ordered_points:
        while len(Llower) >= 2 and right_turn(Llower[-2], Llower[-1], p) <= 0:
            Llower.pop() # Eliminamos el punto "del medio", el ultimo
                         # que habiamos anyadido al lower hull
        Llower.append(p) # Anyadimos el punto siguiente
 
    # Construimos el upper hull de la misma forma que el lower pero
    # recorriendo la lista en sentido inverso
    Lupper = []
    for p in reversed(ordered_points):
        while len(Lupper) >= 2 and right_turn(Lupper[-2], Lupper[-1], p) <= 0:
            Lupper.pop() # Eliminamos de nuevo el punto del medio 
        Lupper.append(p) # Anyadimos el punto siguiente

    
    convex = Llower[:-1] + Lupper[:-1] # Concatenamos ambas listas
    convex = [convex[0]]+convex[::-1]  # Duplicamos el punto inicial y
                                       # lo anyadimos a la lista de
                                       # puntos recorrida en sentido antihorario
    return convex
