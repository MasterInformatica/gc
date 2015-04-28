# -*- coding: utf-8 -*-

""" 
Práctica 6 de Geometría Computacional
Autores:
* Luis María Costero Valero (lcostero@ucm.es)
* Jesús Javier Doménech Arellano (jdomenec@ucm.es)
* Jennifer Hernández Bécares (jennhern@ucm.es)
"""

from __future__ import division
import numpy as np



def spline2d(a, b, xi, k, nu, A, num_dots):
    '''Computes a plane spline curve of order k
       defined on the interval [a, b] with knots psi,
       multiplicities nu and coefficiets A.
       Parameters:
       a, b -- ends of the interval, real numbers
       xi -- list of breakpoints, a < xi[0] < .. < xi[-1] < b
       k -- order of the curve, the degree is <= k - 1
       nu -- list of integer multiplicities of each breakpoint,
             len(psi) = len(nu), 1 <= nu[i] < k
       A -- list of coefficients of the B-spline basis,
            A = [[x0, y0], [x1, y1],..., [x[N], y[N]]
       num_dots -- number of dots of the spline to be plotted,
                   uniformly spaced alogn the interval [a, b]
       Returns:
       the spline curve as a numpy array of size (2, num_dots) <'''

    sol = np.zeros((2, num_dots))
    sol[:,0] = spline1d(a, b, xi, k, nu, A[0], num_dots)
    sol[:,1] = spline1d(a, b, xi, k, nu, A[1], num_dots)
    return sol




def spline1d(a, b, xi, k, nu, A, num_dots):
    tau = np.linespace(a,b, num_dots)
    sum_nu = sum(nu)
    l = nu.shape[0]+1
    t_i = np.zeros( k*(l+1)-sum_nu )
    
    index=0
    t_i[0:k] = a

    index = k;
    for i in range(0, l):
        t_i[index : index+(k-nu[i])] = xi[i] 
        index += index+(k-nu[i])
    
    t_i[index: index+k] = b


    num = [i for i in range(t_i.shape[0]) if (tau>t_i[i] and tau < t_i[i+1])] 

    
