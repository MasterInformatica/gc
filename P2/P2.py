# Luis Maria Costero Valero (lcostero@ucm.es)
# Jesus Javier Domenech Arellano (jdomenec@ucm.es)
# Jennifer Hernandez Becares (jennhern@ucm.es)

import numpy as np #para crear arrays de puntos
from scipy.integrate import odeint #resolutor de edo
import matplotlib.pyplot as plt #para imprimir la grafica
import math #funciones matematicas

import sympy as sp  #calculo simbolico
from sympy.utilities.lambdify import lambdify
from sympy.interactive import printing
from sympy.plotting import plot_parametric

from scipy.spatial.distance import cdist
printing.init_printing(use_latex=True)


t,u,v = sp.symbols('t u v')

if __name__ == "__main__":
    X = sp.matrix([u,v,0])
    E = 
    F =
    G = 
    I = sp.matrix([E, F],[ F, G])
    dIdu= I.diff(u)
    dIdv= I.diff(v)
    dudt= u_t.diff(t)
    dvdt= v_t.diff(t)
    U = sp.matrix([u_t],[v_t])
    dUdt = U.diff(t)
    geod = [0.5*(sp.matrix([[dUdt.transpose()*dIdu*dUdt],[dUdt.transpose()*dIdv*dUdt]])).traspose()-dUdt.transpose()*(dIdu)


