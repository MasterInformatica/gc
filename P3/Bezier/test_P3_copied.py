# -*- coding: utf-8 -*-
import numpy as np
from scipy.special import binom

 
def eval_bezier(degree, t):
    P = np.random.uniform(-20, 20, (degree + 1, 2))

    # Computamos la curva. Le pasamos True para computar
    # por Bernstein

    #curve_precomp = compute_bernstein_precomp(N, t, stuff_Bezier)
    #(curve_x, curve_y) = compute_curve_bernstein(degree-1, stuff_Bezier, P)

    curve_x = np.sum(np.multiply(P[:,0],stuff_Bezier),axis=1)
    curve_y = np.sum(np.multiply(P[:,1],stuff_Bezier),axis=1)

    #curve_x = np.copy(np.sum(np.multiply(P[:,0],stuff_Bezier.transpose()),axis=1))
    #curve_y = np.copy(np.sum(np.multiply(P[:,1],stuff_Bezier.transpose()),axis=1))
    
    #curve = np.array((curve_x, curve_y))
    return np.array((curve_x, curve_y)) #numpy array of size (num_points, 2)
    

def eval_deCasteljau(degree, t):
    P = np.random.uniform(-20, 20, (degree + 1, 2))
    N = degree
    stuff_deCasteljau[:,:N+1,:] = P
    
    for k in range(0, N):
        stuff_deCasteljau[:,0:N-k+2, :] = np.add(np.multiply((1-t),stuff_deCasteljau[:,0:N-k+2, :].transpose()), np.multiply(t,stuff_deCasteljau[:,1:N-k+3,:].transpose())).transpose()
        
    return np.array((stuff_deCasteljau[:,0, 0],stuff_deCasteljau[:,0, 1])) #numpy array of size (num_points, 2)

def compute_curve_bernstein(N, bernstein, polygon):
    curve_x = np.sum(np.multiply(polygon[:,0],bernstein),axis=1)
    curve_y = np.sum(np.multiply(polygon[:,1],bernstein),axis=1)
    #curve_x = sum(polygon[i, 0] * bernstein[i, :] for i in range(N + 1))
    #curve_y = sum(polygon[i, 1] * bernstein[i, :] for i in range(N + 1))
    return (curve_x, curve_y)
                                 
def compute_curve_stuff_deCasteljau(N, stuff_deCasteljau):
    curve_x = stuff_deCasteljau[:,0, 0]
    curve_y = stuff_deCasteljau[:,0, 1]
    return (curve_x, curve_y)

def compute_bernstein_precomp(N, t, bernstein):
    for i in range(N + 1):
        bernstein[ :,i] = binom(N, i) * t**i *(1-t)**(N-i)
    return bernstein
    
def compute_stuff_deCasteljau_precomp(N, t, stuff_deCasteljau, P):
    # Inicializamos la primera columna con los puntos del polinomio introducido
    #stuff_deCasteljau[0,:,:N+1,:] = P

    stuff_deCasteljau[0,:,:N+1,:] = np.copy(P)
    
    # Vamos rellenando el array por columnas, ya que cada b_i^k depende de la
    # columna anterior
##    for k in range(0, N):
##        stuff_deCasteljau[k+1,:,0:N-k+1, 0] = (1-t)*stuff_deCasteljau[k,:,0:N-k+1, 0] + t*stuff_deCasteljau[k,:,1:N-k+1,0]
##        stuff_deCasteljau[k+1,:,0:N-k+1, 1] = (1-t)*stuff_deCasteljau[k,:,0:N-k+1, 1] + t*stuff_deCasteljau[k,:,1:N-k+1,1]
##    return stuff_deCasteljau

    for k in range(0, N):
        stuff_deCasteljau[k+1,:,0:N-k+2, :] = ((1-t)*stuff_deCasteljau[k,:,0:N-k+2, :].transpose() + (t*stuff_deCasteljau[k,:,1:N-k+3,:].transpose())).transpose()
            #stuff_deCasteljau[k+1,:,i, 0] = (1-t)*stuff_deCasteljau[k,:,i, 0] + t*stuff_deCasteljau[k,:,i+1,0]
            #stuff_deCasteljau[k+1,:,i, 1] = (1-t)*stuff_deCasteljau[k,:,i, 1] + t*stuff_deCasteljau[k,:,i+1,1]  
    return stuff_deCasteljau

##    for k in range(0, N):
##        for i in range(0,N-k+1):
##            stuff_deCasteljau[k+1,:,i, :] = ((1-t)*stuff_deCasteljau[k,:,i, :].transpose() + (t*stuff_deCasteljau[k,:,i+1,:].transpose())).transpose()
##    return stuff_deCasteljau

    
if __name__ == '__main__':
    import timeit
    degree = 15
    num_points = 100    
    t = np.linspace(0, 1, num_points)
    #enter here stuff you want to precompute 
    stuff_Bezier = None
    stuff_deCasteljau = None

    # Precomputar para Bernstein
    stuff_Bezier = np.zeros(( num_points,degree+1))
    N = degree - 1;
    stuff_Bezier = compute_bernstein_precomp(N, t, stuff_Bezier)


    # Inicialización de array para Casteljau
    stuff_deCasteljau = np.zeros((num_points, num_points, 2))

    print(timeit.repeat("eval_bezier(degree, t)",
                        setup="from __main__ import eval_bezier, degree, t, stuff_Bezier",
                        number=10000))
    
    print(timeit.repeat("eval_deCasteljau(degree, t)",
                        setup="from __main__ import eval_deCasteljau, degree, t, stuff_deCasteljau",
                        number=10000))

