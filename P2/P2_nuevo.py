# -*- coding: utf-8 -*-
# Luis Maria Costero Valero (lcostero@ucm.es)
# Jesus Javier Domenech Arellano (jdomenec@ucm.es)
# Jennifer Hernandez Becares (jennhern@ucm.es)

from __future__ import division

import numpy as np #para crear arrays de puntos
from scipy.integrate import odeint #resolutor de edo

import math #funciones matematicas

import sympy as sp  #calculo simbolico
from sympy.utilities.lambdify import lambdify

import matplotlib.pyplot as plt

from mayavi import mlab

def rhs_eqs(Y, _):
    u,v,du,dv = Y
    return [du,dv,ddU(u,v,du,dv)[0][0], ddU(u,v,du,dv)[0][1]]


if __name__ == '__main__':
    u,v,du,dv = sp.symbols('u v du dv')

    ## Caso (b). Entrada I, u0, v0, du0, dv0
    r, a = 2.0, 5.0 #radios del toro
    
    E = r**2
    F = 0.0
    G = (r*sp.cos(u)+a)**2

    #E=1.0/v**2
    #G=1.0/v**2
    #F=0
    I = sp.Matrix([[E, F], [F, G]])
    
    u0, v0 = np.pi, 0.0
    du0, dv0 = 0.0, 1.0
    init_cond = [u0, v0, du0, dv0]

    t = [0, 50*np.pi]
    delta = 0.05
    interval = np.arange(t[0], t[1]+delta, delta)
    #fin de la entrada

    dIu = I.diff(u)
    dIv = I.diff(v)

    dU = sp.Matrix([[du], [dv]]) 
    
    A1 = dU.transpose()*dIu*dU
    A2 = dU.transpose()*dIv*dU
    A = 0.5 * sp.Matrix([A1 ,A2]).transpose()
    B = dU.transpose() * (dIu*du+dIv*dv)

 
    ddU = lambdify((u, v, du, dv), (A - B)*I.inv(), [{'ImmutableMatrix': np.array}, 'numpy'])
    
    solu = odeint(rhs_eqs, init_cond, interval)
    x_coord2 = [x for [x,y,dx,dy] in solu]
    y_coord2 = [y for [x,y,dx,dy] in solu]
    plt.plot(x_coord2,y_coord2);
    plt.axis('equal')
    plt.show()






    #---------------------------------------------------------------------------
    X = lambdify((u,v), ((r*sp.cos(u)+a)*sp.cos(v), (r*sp.cos(u)+a)*sp.sin(v), r*sp.sin(u)),[{'ImmutableMatrix': np.array}, 'numpy'])

    x_coord =[]
    y_coord =[]
    z_coord =[]

    for s in solu:
        aux = X(s[0],s[1])
        x_coord.append(aux[0])
        y_coord.append(aux[1])
        z_coord.append(aux[2])
    

    mlab.plot3d(x_coord, y_coord, z_coord)    





    
    cu = np.linspace(0, 2*np.pi, 100)
    cv = np.linspace(0, 2*np.pi, 100)

    # Creamos la rejilla con la cual vamos a hacer las cuentas
    # meshgrid crea el reticulo para hacer operaciones con todo
    # el reticulo a al vez
    u_mesh, v_mesh = np.meshgrid(cu, cv)
    
    
    # Introducimos las formulas de nuetra superficie parametrizada
    # En este caso, un toro parametrizado
    cx = (r*np.cos(u_mesh)+a)*np.cos(v_mesh)
    cy = (r*np.cos(u_mesh)+a)*np.sin(v_mesh)
    cz = r*np.sin(u_mesh)
    
    #mlab.plot3d(x_curve, y_curve, z_curve)
    mlab.mesh(cx,cy,cz, colormap='spring')
    
    
    
    mlab.show()
