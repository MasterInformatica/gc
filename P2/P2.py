# Luis Maria Costero Valero (lcostero@ucm.es)
# Jesus Javier Domenech Arellano (jdomenec@ucm.es)
# Jennifer Hernandez Becares (jennhern@ucm.es)

from __future__ import division

import numpy as np #para crear arrays de puntos
from scipy.integrate import odeint #resolutor de edo
import matplotlib.pyplot as plt #para imprimir la grafica
import math #funciones matematicas

import sympy as sp  #calculo simbolico
from sympy.utilities.lambdify import lambdify
from sympy.interactive import printing
from sympy.plotting import plot_parametric

from scipy.spatial.distance import cdist


t,u,v,dvdt,dudt = sp.symbols('t u v dvdt dudt')
u0,v0,du0,dv0 = 5,0,0,2
init_cond = [u0,v0,du0,dv0]
if __name__ == "__main__":
    X = sp.Matrix([u,v,0])
    E = 5.0**2
    F = 0
    G = (5.0*sp.cos(u)+2)**2
    I = sp.Matrix([[E, F],[ F, G]])
    print I
    dIdu= I.diff(u)
    dIdv= I.diff(v)
#    dudt= u_t.diff(t)
 #   dvdt= v_t.diff(t)
    U = sp.Matrix([[u],[v]])
    dUdt = sp.Matrix([[dudt],[dvdt]])
    print "dUdt",dUdt
    print "U", U
    A = sp.Matrix([0.5*dUdt.transpose()*dIdu*dUdt,0.5*dUdt.transpose()*dIdv*dUdt])
    B = dUdt.transpose()*(dIdu*dvdt+dIdv*dvdt)
    print "A",A
    print "B",B
    ddUddt = lambdify((u,v,dudt,dvdt),((A.transpose()-B)*I.inv()), [{'ImmutableMatrix': np.array}, 'numpy'])
    print ddUddt(1,2,2,2)[0] #TODO ARREGLAR!
            

def rhs_eqs(Y,t):
    u,v,du,dv = Y
    return [du,dv,ddUddt(u,v,du,dv)[0][0],ddUddt(u,v,du,dv)[0][1]]
interval = np.arange(0, 8*np.pi + 0.1, 0.1)
solu = odeint(rhs_eqs,init_cond,interval)


#Pintamos la curva
curve_x = [x for [x, y, dx, dy] in solu]
curve_y = [y for [x, y, dx, dy] in solu]

plt.plot(curve_x, curve_y)
plt.axis('equal')
plt.show()
