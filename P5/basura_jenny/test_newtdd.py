#from newtdd import newtdd
from nest   import nest
import matplotlib.pyplot as plt
import numpy as np
from numpy import *

#xdata = [0.0,1,2,3,3.4]
#ydata = [0.0,3,12,6,2]

def newtdd(x,y):
	n = len(x)
	v = zeros((n,n))
	for j in range(n):
		v[j,0] = y[j]			# Fill in y column of Newton triangle
	for i in range(1,n):		# For column i,
		for j in range(n-i):	# 1:n+1-i		# fill in column from top to bottom
#			print j,i," ",j+1,i-1," ", j,i-1," ",j+i," ",j
			v[j,i] = (v[j+1,i-1]-v[j,i-1])/(x[j+i]-x[j])
	c = v[0,:].copy()			# Read along top of triangle for output coefficients
	return c


    
def interpolate(x, tau, num_points):

    interpolant = newtdd(tau,x)

    t = np.linspace(tau[0],tau[-1], num_points)
    y = eval_pol(interpolant, tau, num_points)

    #plt.plot(t,y,'b')
    #plt.show()

def eval_pol(a, tau, num_points):
    N = a.shape[0]-1; # ultimo indice accesible

    x = np.linspace(tau[0], tau[-1], num_points)

    sol = a[N] * np.ones(num_points)
    for k in range(N-1, -1, -1):
        sol = a[k]  + (x-tau[k])*sol

    return sol


n = 10  
tau = np.arange(n)
x = np.random.randint(-10, 10, size=n)

num_points = 100

import timeit
print(timeit.repeat("interpolate(x,tau,num_points)", setup="from __main__ import interpolate, x, n, tau, num_points,eval_pol, np", number=10000))


# Codigo tarda: [0.9688677787780762, 0.9725048542022705, 0.9821891784667969]
