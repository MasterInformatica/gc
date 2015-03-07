# -*- coding: utf-8 -*-
# Luis Maria Costero Valero (lcostero@ucm.es)
# Jesus Javier Domenech Arellano (jdomenec@ucm.es)
# Jennifer Hernandez Becares (jennhern@ucm.es)

from __future__ import division

import numpy as np #para crear arrays de puntos
from scipy.integrate import odeint #resolutor de edo
import matplotlib.pyplot as pp
import math #funciones matematicas
import sympy as sp  #calculo simbolico
from sympy.utilities.lambdify import lambdify

import matplotlib.pyplot as plt

from mayavi import mlab


def rhs_eqs(Y, _):
    u,v,du,dv = Y

    return [du,dv,ddU(u,v,du,dv)[0][0], ddU(u,v,du,dv)[0][1]]


#Calcula primera forma fundamental
def calcfff(X): 
    dXu = X.diff(u)
    dXv = X.diff(v)
    E = dXu.dot(dXu)
    F = dXu.dot(dXv)
    G = dXv.dot(dXv)

    return E.simplify(), F.simplify(), G.simplify()



def plot_surface(X, solu, u_limits,v_limits):
    u_points = np.linspace(u_limits[0], u_limits[1], 100)
    v_points = np.linspace(v_limits[0], v_limits[1], 100)

    # Creamos la rejilla con la cual vamos a hacer las cuentas
    u_mesh, v_mesh = np.meshgrid(u_points, v_points)
    
    X_lmbf = lambdify((u,v), X, [{'ImmutableMatrix': np.array}, 'numpy'])
    surface = X_lmbf(u_mesh, v_mesh)
    
    mlab.mesh(surface[0][0], surface[1][0], surface[2][0], colormap='spring')

    x_coord =[]
    y_coord =[]
    z_coord =[]

    for s in solu:
        aux = X_lmbf(s[0],s[1])
        x_coord.append(aux[0])
        y_coord.append(aux[1])
        z_coord.append(aux[2])
        
    mlab.plot3d(x_coord, y_coord, z_coord)    
    
    mlab.show()


if __name__ == '__main__':
    u,v,du,dv = sp.symbols('u v du dv') 

    ##########################################
    #  Caso (a). Entrada x(u,v), intervalo_u, intervalo_v
    ##########################################
    caso = 0
    r, a = 2.0, 5.0

    x = (r*sp.cos(u)+a)*sp.cos(v)
    y = (r*sp.cos(u)+a)*sp.sin(v)
    z = r*sp.sin(u)

    # X(u,v) = (x(u,v),y(u,v),z(u,v))
    X = sp.Matrix([x, y, z])
    
    u_limits = [0,2.0*np.pi]
    v_limits = [0,2.0*np.pi]

    t0 = 10
    t_limits = [0,30*np.pi]

    u0, v0 = 0, 0
    du0, dv0 = 1., 0
    init_cond = [u0, v0, du0, dv0]

    E, F, G = calcfff(X)
    
    # Fin entrada caso (a)
    ########################################## 
    #  Caso (b). Entrada I, u0, v0, du0, dv0 #
    ##########################################    
    # caso = 1

    # r, a = 2.0, 5.0 #radios del toro
    # E = r**2
    # F = 0.0
    # G = (r*sp.cos(u)+a)**2

    # u_limits = [0,2.0*np.pi]
    # v_limits = [0,2.0*np.pi]

    # t0 = 1
    # t_limits = [0, 32*np.pi]

    # u0, v0 = np.pi, 0.0
    # du0, dv0 = 0.0, 1.0
    # init_cond = [u0, v0, du0, dv0]

    
    # Fin entrada caso (b)
    #---------------------------------------------------------------------------


    #Primera forma funfamental
    I = sp.Matrix([[E, F], [F, G]])
    dIu = I.diff(u)
    dIv = I.diff(v)

    #Matriz de coeficientes 
    dU = sp.Matrix([[du], [dv]]) 

    #Lado derecho del sistema
    A1 = dU.transpose()*dIu*dU
    A2 = dU.transpose()*dIv*dU
    A = 0.5 * sp.Matrix([A1 ,A2]).transpose()
    B = dU.transpose() * (dIu*du+dIv*dv)

    ddU = lambdify((u, v, du, dv), (A - B)*I.inv(), [{'ImmutableMatrix': np.array}, 'numpy'])



    #Puntos del intervalo
    delta = 0.005
    solu = None

    if t0 == t_limits[0]: #el punto es el limite inferior
        interval = np.arange(t0, t_limits[1]+delta, delta)
        solu = odeint(rhs_eqs, init_cond, interval)
    elif t0 == t_limits[1]: #el pto es el limite superior
        interval = np.arange(t0, t_limits[0]-delta, -delta)
        solu = odeint(rhs_eqs, init_cond, interval)
    else: #se encuentra en el interior
        interval1 = np.arange(t0, t_limits[0]-delta, -delta)
        interval2 = np.arange(t0, t_limits[1]+delta, delta)

        solu1 = odeint(rhs_eqs, init_cond, interval1)
        solu2 = odeint(rhs_eqs, init_cond, interval2)

        solu = np.concatenate((solu1, solu2))


    #mostramos la solucion en el intervalo de definicion
    x_coord2 = [x%(u_limits[1]-u_limits[0])+u_limits[0] for [x,y,dx,dy] in solu]
    y_coord2 = [y%(v_limits[1]-v_limits[0])+v_limits[0] for [x,y,dx,dy] in solu]

    plt.plot(x_coord2,y_coord2, ',')
    plt.axis('equal')
    plt.show()

    # si estamos en el caso (a), mostramos la geodesica sonre la superficie
    if caso == 0:
        plot_surface(X, solu, u_limits, v_limits)
