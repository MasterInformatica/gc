import numpy as np
from _intersection_bezier_luisma import IntersectionBezier

intersection = IntersectionBezier()

# Pruebas con los ejemplos que ha puesto Antonio en el campus
P = np.array([[-10,-10],[0,20],[10,-10]])
Q = np.array([[10,10],[0,-20],[-10,10]])
cuts = intersection(P, Q, epsilon=0.01); print cuts

intersection.plot()


P = np.array([[-10,-10], [0,5], [10,-10]])
Q = np.array([[10,10],[0,-5], [-10,10]])
cuts = intersection(P,Q,epsilon=0.01)
print cuts
intersection.plot()
