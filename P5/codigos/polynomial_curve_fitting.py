from __future__ import division
import numpy as np
import matplotlib.pyplot as plt



def polynomial_curve_fitting(points, knots, method, L=0, libraries=False,
                             num_points=100):    
    '''
       Fits planar curve to points at given knots. 

       Arguments:
           points -- coordinates of points to adjust (x_i, y_i) given by a numpy array of shape (N, 2)
           knots -- strictly increasing sequence at which the curve will fit the points, tau_i
               It is given by a np.array of shape M, unless knots='chebyshev', in this case
                   N Chebyshev's nodes between 0 and 1 will be used instead of tau.
           method -- one of the following: 
               'newton' computes the interpolating polynomial curve using Newton's method.
                   returns error if N!=M. 
               'least_squares' computes the best adjusting curve in the least square sense,
                   i.e., min_a ||Ca - b||**2 + L/2 ||a||**2
           L -- regularization parameter
           libraries -- If False, only numpy linear algebra operations are allowed. 
               If True, any module can be used. In this case, a very short and fast code is expected
           num_points -- number of points to plot between tau[0] and tau[-1]

       Returns:
           numpy array of shape (num_points, 2) given by the evaluation of the polynomial
           at the evenly spaced num_points between tau[0] and tau[-1]
    '''
    return [polynomial_curve_fitting1d(points[:,0], knots, method, L, libraries, num_points),
            polynomial_curve_fitting1d(points[:,1], knots, method, L, libraries, num_points)]


def polynomial_curve_fitting1d(points, knots, method, L=0, libraries=False,
                             num_points=100):   
    degree = 0 # hay que cambiarlo
    if method == 'newton':
        return newton_polynomial(points,knots,num_points,libraries)
    else:
        return least_squares_fitting(points,knots,degree,num_points,L,libraries)
    pass


def newton_polynomial(x, tau, num_points=100, libraries=False):    
    '''
    Computes de Newton's polynomial interpolating values x at knots tau
    x: numpy array of size n; points to interpolate
    tau: numpy array of size n; knots tau[0] < tau[1] < ... < tau[n-1]
    num_points: number of points at which the polynomial will be
                evaluated

    libraries: False means only linear algebra can be used
               True means every module can be used.

    returns:
       numpy array of size num_points given by the polynomial 
       evaluated at np.linspace(tau[0], tau[1], num_points)

    Maximum cost allowed: 5,43 s at lab III computers
            degree = n - 1 = 9
            num_points = 100
    '''
    
    if libraries:
        return interp_with_library(x,tau,num_points) #np.array of size num_points
    else:
        interpolant = newtondd(tau,x)
        t = np.linspace(tau[0],tau[-1], num_points)
        y = eval_poly(t,interpolant, tau)
        return y #np.array of size num_points
    

def interp_with_library(x, tau, num_points):
    '''
    Interpola resolviendo el sistema con la matriz de Vandermonde
    '''
    coeffs = np.linalg.solve(np.vander(tau, increasing=True), x)
    times = np.linspace(tau[0], tau[-1], num_points)
    return np.polyval(coeffs,times)

def newtondd(x,y):
	n = len(x)
	v = np.zeros((n,n))
        v[:,0] = y[:]		# Fill in y column of Newton triangle
	for i in range(1,n):		# For column i,
		for j in range(n-i):	# 1:n+1-i		# fill in column from top to bottom
#			print j,i," ",j+1,i-1," ", j,i-1," ",j+i," ",j
			v[j,i] = (v[j+1,i-1]-v[j,i-1])/(x[j+i]-x[j])
	c = v[0,:].copy()			# Read along top of triangle for output coefficients
	return c



def eval_poly(t, coefs, tau=None):    
    N = coefs.shape[0]-1; # ultimo indice accesible

    sol = coefs[N] * np.ones(t.shape[0])
    for k in range(N-1, -1, -1):
        sol = coefs[k]  + (t-tau[k])*sol

    return sol

        
def least_squares_fitting(points, knots, degree, num_points, L=0, libraries=True):    
    #I've used np.linalg.lstsq and np.polyval if libraries==True
    if libraries:
        pass
    else:
        pass
        
def chebyshev_knots(a, b, n):
    pass
       



                                 
                
