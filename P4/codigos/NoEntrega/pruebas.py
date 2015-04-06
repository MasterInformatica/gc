import numpy as np
from _intersection_bezier_luisma import IntersectionBezier


# Pruebas con los ejemplos que ha puesto Antonio en el campus
intersection = IntersectionBezier()
P = np.array([[-10,-10],[0,20],[10,-10]])
Q = np.array([[10,10],[0,-20],[-10,10]])
cuts = intersection(P, Q, epsilon=0.01); 
print "Prueba 1: ", cuts

intersection.plot()



intersection = IntersectionBezier()
P = np.array([[-10,-10], [0,5], [10,-10]])
Q = np.array([[10,10],[0,-5], [-10,10]])
cuts = intersection(P,Q,epsilon=0.01)
print "Prueba 2: ", cuts

intersection.plot()



intersection = IntersectionBezier()
P = np.array([[-10,-10], [0,10], [10,-10]])
Q = np.array([[10,10], [0,-10], [-10, 10]])
cuts = intersection(P,Q, epsilon=0.01)
print "Prueba 3: ",  cuts
intersection.plot()
