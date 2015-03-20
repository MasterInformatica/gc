# -*- coding: utf-8 -*-
import numpy as np
from scipy.special import binom

 
def eval_bezier(degree, t, stuff_Bezier):
    P = np.random.uniform(-20, 20, (degree + 1, 2))

    # Computamos la curva. Le pasamos True para computar
    # por Bernstein

    #curve_precomp = compute_bernstein_precomp(N, t, stuff_Bezier)
    (curve_x, curve_y) = compute_curve_bernstein(degree-1, stuff_Bezier, P)
    curve = np.array((curve_x, curve_y))
    return curve #numpy array of size (num_points, 2)
    

def eval_deCasteljau(degree, t, stuff_deCasteljau):
    P = np.random.uniform(-20, 20, (degree + 1, 2))
    
    # Computamos la curva. Le pasamos un False para computar
    # por Casteljau
    curve_precomp = compute_casteljau_precomp(degree, t, stuff_deCasteljau, P)
    (curve_x, curve_y) = compute_curve_casteljau(N, curve_precomp)
    curve = np.array((curve_x, curve_y))
    return curve #numpy array of size (num_points, 2)

def compute_curve_bernstein(N, bernstein, polygon):
    curve_x = sum(polygon[i, 0] * bernstein[i, :] for i in range(N + 1))
    curve_y = sum(polygon[i, 1] * bernstein[i, :] for i in range(N + 1))
    return (curve_x, curve_y)
                                 
def compute_curve_casteljau(N, casteljau):
    curve_x = casteljau[N,:,0, 0]
    curve_y = casteljau[N,:,0, 1]
    return (curve_x, curve_y)

def compute_bernstein_precomp(N, t, bernstein):
    for i in range(N + 1):
        bernstein[i, :] = binom(N, i) * t**i *(1-t)**(N-i)
    return bernstein
    
def compute_casteljau_precomp(N, t, casteljau, P):
    # Inicializamos la primera columna con los puntos del polinomio introducido
    casteljau[0,:,:N+1,:] = P
        
    # Vamos rellenando el array por columnas, ya que cada b_i^k depende de la
    # columna anterior
    for k in range(0, N):
        for i in range(0,N-k+1):
            casteljau[k+1,:,i, 0] = (1-t)*casteljau[k,:,i, 0] + t*casteljau[k,:,i+1,0]
            casteljau[k+1,:,i, 1] = (1-t)*casteljau[k,:,i, 1] + t*casteljau[k,:,i+1,1]
    return casteljau
  

    
if __name__ == '__main__':
    import timeit
    degree = 15
    num_points = 100    
    t = np.linspace(0, 1, num_points)
    #enter here stuff you want to precompute 
    stuff_Bezier = None
    stuff_deCasteljau = None

    # Precomputar para Bernstein
    stuff_Bezier = np.zeros((degree+1, num_points))
    N = degree - 1;
    stuff_Bezier = compute_bernstein_precomp(N, t, stuff_Bezier)

    # Inicialización de array para casteljau
    stuff_deCasteljau = np.zeros((num_points, num_points, num_points, 2))

    print(timeit.repeat("eval_bezier(degree, t, stuff_Bezier)",
                        setup="from __main__ import eval_bezier, degree, t, stuff_Bezier",
                        number=1000))
    
    print(timeit.repeat("eval_deCasteljau(degree, t, stuff_deCasteljau)",
                        setup="from __main__ import eval_deCasteljau, degree, t, stuff_deCasteljau",
                        number=1000))

