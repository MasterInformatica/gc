from mayavi import mlab
import numpy as np

import sympy as sym

u = np.linspace(0, 2*np.pi, 100)
v = np.linspace(0, 2*np.pi, 100)

# Creamos la rejilla con la cual vamos a hacer las cuentas
# meshgrid crea el reticulo para hacer operaciones con todo
# el reticulo a al vez
u_mesh, v_mesh = np.meshgrid(u, v)


# Introducimos las formulas de nuetra superficie parametrizada
# En este caso, un toro parametrizado
r = 1
a = 2
x = (r*np.cos(u_mesh)+a)*np.cos(v_mesh)
y = (r*np.cos(u_mesh)+a)*np.sin(v_mesh)
z = r*np.sin(u_mesh)

# Introducimos la superficie mediante su primera forma fundamental
E = r**2
F = 0
G = (r*np.cos(u_mesh)+a)**2


x_curve = r*np.cos(u)
y_curve = r*np.cos(u)
z_curve = r*np.sin(u)

#mlab.plot3d(x_curve, y_curve, z_curve)
mlab.mesh(x,y,z, colormap='spring')
mlab.show()

# if __name__ == '__main__':
#       u, v = sym.symbols('u v')
#       X = sym.Matrix([u, v, 0])
#        ... demas datos
#       compute_geodesic()

# tambien se puede hacer una clase y despues crear una instancia
u, v = sym.symbols('u v')








X = sym.Matrix([r**2, 0, 0, (r*sym.cos(u)+a)**2])
print X
diffu = X.diff(u)
print diffu
diffv = X.diff(v)
print diffv
#u, v = sym.symbols('u v')
#X = sym.Matrix([sym.cos(u), sym.sin(u)])

#X.diff(u) # Derivada con respecto a u (evidente)
