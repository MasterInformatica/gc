from mayavi import mlab
import numpy as np

import sympy as sym
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



theta = np.linspace(0, 2*np.pi, 100)
t = np.linspace(-1, 1, 100)

# Creamos la rejilla con la cual vamos a hacer las cuentas
# meshgrid crea el reticulo para hacer operaciones con todo
# el reticulo a al vez
theta_mesh, t_mesh = np.meshgrid(theta, t)

# Con el coseno lo giramos
# Para las expresiones mirar la clase del dia 4 de marzo,
# que tiene hechas las cuentecillas
x = np.cosh(t_mesh) * np.cos(theta_mesh)
y = np.cosh(t_mesh) * np.sin(theta_mesh)
z = np.sinh(t_mesh)
u = np.linspace(0, 2*np.pi, 100)
v = np.linspace(0, 2*np.pi, 100)

# Creamos la rejilla con la cual vamos a hacer las cuentas
# meshgrid crea el reticulo para hacer operaciones con todo
# el reticulo a al vez
u_mesh, v_mesh = np.meshgrid(u, v)
x = (5.0*np.cos(u_mesh)+4)*np.cos(v_mesh)
y = (5.0*np.cos(u_mesh)+4)*np.sin(v_mesh)
z = 5.0*np.sin(u_mesh)

print (5.0*math.cos(0)+4)*math.cos(0)
print (5.0*math.cos(0)+4)*math.sin(0)
print (5.0*math.sin(0))

t,u,v,dvdt,dudt = sp.symbols('t u v dvdt dudt')
u0,v0,du0,dv0 = 9,0,0,2
init_cond = [u0,v0,du0,dv0]

X = sp.Matrix([u,v,0])
E = 5.0**2
F = 0
G = 5.0*sp.cos(u)+2
I = sp.Matrix([[E, F],[ F, G]])

dIdu= I.diff(u)
dIdv= I.diff(v)
U = sp.Matrix([[u],[v]])
dUdt = sp.Matrix([[dudt],[dvdt]])

A = sp.Matrix([0.5*dUdt.transpose()*dIdu*dUdt,0.5*dUdt.transpose()*dIdv*dUdt])
B = dUdt.transpose()*(dIdu*dudt+dIdv*dvdt)

ddUddt = lambdify((u,v,dudt,dvdt),((A.transpose()-B)*I.inv()), [{'ImmutableMatrix': np.array}, 'numpy'])
print ddUddt(1,2,2,2)[0] #TODO ARREGLAR!


def rhs_eqs(Y,_):
    u,v,du,dv = Y
    return [du,dv,ddUddt(u,v,du,dv)[0][0],ddUddt(u,v,du,dv)[0][1]]

interval = np.arange(0, 2*np.pi + 0.1, 0.1)
solu = odeint(rhs_eqs,init_cond,interval)


#Pintamos la curva
curve_x = [a for [a,b, dx, dy] in solu]
curve_y = [b for [a,b, dx, dy] in solu]
curve_z = interval


# Para pintar una curva tambien
#x_curve =  np.cosh(t) * np.cos(t)
#y_curve =  np.cosh(t) * np.sin(t)
#z_curve =  np.sinh(t) 

mlab.plot3d(curve_x,curve_y,curve_z)
mlab.mesh(x,y,z, colormap='spring')
mlab.show()

u, v = sym.symbols('u v')
X = sym.Matrix([sym.cos(u), sym.sin(u)])

X.diff(u) # Derivada con respecto a u (evidente)
