# -*- coding: utf-8 -*-
import numpy as np
from scipy.special import binom

#----------------------------------------------------------------------------------- 
def eval_bezier(degree, t):
    P = np.random.uniform(-20, 20, (degree + 1, 2))

    #producto escalar sobre dos coordenadas
    curve = np.dot(stuff_Bezier, P);
    return curve #numpy array of size (num_points, 2)

def compute_bernstein_precomp(N, t, bernstein):
    for i in range(N + 1):
        bernstein[:,i] = binom(N, i) * t**i *(1-t)**(N-i)
    return bernstein


#-----------------------------------------------------------------------------------

def eval_deCasteljau(degree, t):
    P = np.random.uniform(-20, 20, (degree + 1, 2))
    N = degree
    stuff_deCasteljau[:,:N+1,:] = P
    
    for k in range(0, N):
        stuff_deCasteljau[:,0:N-k+2, :] = np.add( np.multiply( (1-t) , stuff_deCasteljau[:,0:N-k+2, :].transpose()),
                                                  np.multiply(   t   , stuff_deCasteljau[:,1:N-k+3,:].transpose()) ).transpose()
        
    return np.array((stuff_deCasteljau[:,0, 0],stuff_deCasteljau[:,0, 1])) #numpy array of size (num_points, 2)

#-----------------------------------------------------------------------------------

    
if __name__ == '__main__':
    import timeit
    degree = 15
    num_points = 100    
    t = np.linspace(0, 1, num_points)

    #enter here stuff you want to precompute 
    stuff_Bezier = None
    stuff_deCasteljau = None

    # Precomputations for Bernstein's algorithm
    stuff_Bezier = np.zeros(( num_points,degree+1))
    N = degree - 1;
    stuff_Bezier = compute_bernstein_precomp(N, t, stuff_Bezier)
    
    # Precomputations for deCasteljau's algorithm
    stuff_deCasteljau = np.zeros((num_points, num_points, 2))


    print(timeit.repeat("eval_bezier(degree, t)",
                        setup="from __main__ import eval_bezier, degree, t, stuff_Bezier",
                        number=10000))
    
    print(timeit.repeat("eval_deCasteljau(degree, t)",
                        setup="from __main__ import eval_deCasteljau, degree, t, stuff_deCasteljau",
                        number=10000))

