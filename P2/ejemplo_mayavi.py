from mayavi import mlab
import numpy as np

import sympy as sym

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

# Para pintar una curva tambien
x_curve =  np.cosh(t) * np.cos(t)
y_curve =  np.cosh(t) * np.sin(t)
z_curve =  np.sinh(t) 

print x


mlab.plot3d(x_curve, y_curve, z_curve)
mlab.mesh(x,y,z, colormap='spring')
mlab.show()

u, v = sym.symbols('u v')
X = sym.Matrix([sym.cos(u), sym.sin(u)])

X.diff(u) # Derivada con respecto a u (evidente)
