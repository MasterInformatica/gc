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

####################################
# Clase para dar verctor init_cond #
####################################
class GenInitConds:
    def __init__ (self):
        self.init_cond = None
        self.manual = True # Poner false para no sacar la ventana
        self.u0 = None
        self.v0 = None
        self.dv0 = None
        self.du0 = None
        self.una = False # ya se ha pinchado una vez
        self.fin = False # ya se ha pinchado dos veces
        self.fig = None
        self.ax = None
        self.E = None
        self.F = None
        self.G = None
        self.u_limits = None
        self.v_limits = None
        self.t_limits = None
        self.solu = None
 
      
    def setVars(self,E,F,G,u_limits,v_limits,t_limits):
        self.E = E
        self.F = F
        self.G = G
        self.u_limits = u_limits
        self.v_limits = v_limits
        self.t_limits = t_limits
        self.fig = plt.figure()
        self.ax = plt.subplot(111)
        self.ax.set_xlim(u_limits[0],u_limits[1])
        self.ax.set_ylim(v_limits[0],v_limits[1])
        self.ax.set_title('Pincha dos puntos para dibujar la geodesica con ese vector.')
        self.evento_click = self.fig.canvas.mpl_connect(
            'button_press_event', self.on_clk)
        
    def on_clk(self,evt):
        if self.fin:
            self.fin = False
            self.una = False

        if self.una: 
            self.du0 = self.du0 + float(evt.xdata)
            self.dv0 = self.dv0 + float(evt.ydata)
            self.fin = True
            self.init_cond = [self.u0,self.v0,self.du0,self.dv0]
            self.solu = plot_geodesic(self.E,self.F,self.G,self.init_cond,self.u_limits,self.v_limits,self.t_limits)
            return 

        self.u0 = float(evt.xdata)
        self.v0 = float(evt.ydata)
        self.du0 = -1.0*self.u0
        self.dv0 = -1.0*self.v0
        self.una = True

ddU = None

def rhs_eqs(Y, _):
    global ddU
    u,v,du,dv = Y
    return [du,dv,ddU(u,v,du,dv)[0][0], ddU(u,v,du,dv)[0][1]]

# calcula y dibuja una geodesica con init_cond
def plot_geodesic(E,F,G,init_cond,u_limits,v_limits,t_limits): 
    global ddU
    delta = 0.005
    interval = np.arange(t_limits[0], t_limits[1]+delta, delta)

    I = sp.Matrix([[E, F], [F, G]])
    dIu = I.diff(u)
    dIv = I.diff(v)

    dU = sp.Matrix([[du], [dv]]) 
    
    A1 = dU.transpose()*dIu*dU
    A2 = dU.transpose()*dIv*dU
    A = 0.5 * sp.Matrix([A1 ,A2]).transpose()
    B = dU.transpose() * (dIu*du+dIv*dv)

    ddU = lambdify((u, v, du, dv), (A - B)*I.inv(), [{'ImmutableMatrix': np.array}, 'numpy'])
    
    solu = odeint(rhs_eqs, init_cond, interval)
    x_coord2 = [(x%(u_limits[1]-u_limits[0])+u_limits[0]) for [x,y,dx,dy] in solu]
    y_coord2 = [(y%(v_limits[1]-v_limits[0])+v_limits[0]) for [x,y,dx,dy] in solu]
    fig = plt.plot(x_coord2,y_coord2,',')
    plt.show()

    return solu

def calculaff(X): #Calcula primera forma fundamental
 
    dXu = X.diff(u)
    dXv = X.diff(v)
    E = dXu.dot(dXu)
    F = dXu.dot(dXv)
    G = dXv.dot(dXv)

    return E,F,G

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
    # Si quieres introducir las condiciones iniciales graficamente
    # pon esta variable a True, para dar [u0,v0,du0,dv0] desde plot
    init_cond_plot = True
    ##########################################
    #  Caso (a). Entrada x(u,v), intervalo_u, intervalo_v
    ##########################################
    caso = 0
    r, a = 2.0, 5.0

    x = (r*sp.cos(u)+a)*sp.cos(v)
    y = (r*sp.cos(u)+a)*sp.sin(v)
    z = r*sp.sin(u)

    # X(u,v) = (x(u,v),y(u,v),z(u,v))
    X = sp.Matrix([x,y,z])

    E,F,G = calculaff(X)
    
    # Fin entrada caso (a)

    ########################################## 
    #  Caso (b). Entrada I, u0, v0, du0, dv0 #
    ##########################################
    #caso = 1

    # r, a = 2.0, 5.0 #radios del toro
    # E = r**2
    # F = 0.0
    # G = (r*sp.cos(u)+a)**2

    #E=1.0/v**2
    #G=1.0/v**2
    #F=0
    
    # Fin entrada caso (b)
    #---------------------------------------------------------------------------

    u_limits = [0,2.0*np.pi]
    v_limits = [0,2.0*np.pi]
    t_limits = [0, 16*np.pi]

    if not init_cond_plot:
        u0, v0 = np.pi, 0.0
        du0, dv0 = 1.0, 1.0
        init_cond = [u0, v0, du0, dv0]
        solu = plot_geodesic(E,F,G,init_cond,u_limits,v_limits,t_limits)
    else:
        gen = GenInitConds()
        gen.setVars(E,F,G,u_limits,v_limits,t_limits)
        plt.show()
        init_cond = gen.init_cond
        solu = gen.solu
    print init_cond


    

    if caso == 0:
        plot_surface(X,solu,u_limits,v_limits)


    


    # x_coord =[]
    # y_coord =[]
    # z_coord =[]

    # for s in solu:
    #     aux = X(s[0],s[1])
    #     x_coord.append(aux[0])
    #     y_coord.append(aux[1])
    #     z_coord.append(aux[2])
    

    # mlab.plot3d(x_coord, y_coord, z_coord)    





    
    # cu = np.linspace(0, 2*np.pi, 100)
    # cv = np.linspace(0, 2*np.pi, 100)

    # # Creamos la rejilla con la cual vamos a hacer las cuentas
    # # meshgrid crea el reticulo para hacer operaciones con todo
    # # el reticulo a al vez
    # u_mesh, v_mesh = np.meshgrid(cu, cv)
    
    
    # # Introducimos las formulas de nuetra superficie parametrizada
    # # En este caso, un toro parametrizado
    # cx = (r*np.cos(u_mesh)+a)*np.cos(v_mesh)
    # cy = (r*np.cos(u_mesh)+a)*np.sin(v_mesh)
    # cz = r*np.sin(u_mesh)
    
    # #mlab.plot3d(x_curve, y_curve, z_curve)
    # mlab.mesh(cx,cy,cz, colormap='spring')
    
    
    
    # mlab.show()
