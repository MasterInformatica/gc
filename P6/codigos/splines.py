# -*- coding: utf-8 -*-

""" 
Práctica 6 de Geometría Computacional
Autores:
* Luis María Costero Valero       (lcostero@ucm.es)
* Jesús Javier Doménech Arellano  (jdomenec@ucm.es)
* Jennifer Hernández Bécares      (jennhern@ucm.es)
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
    # tau = np.linspace(a,b, num_dots)
    # sum_nu = sum(nu)
    # l = nu.shape[0]+1
    # t_i = np.zeros( k*(l+1)-sum_nu )
    
    # index=0
    # t_i[0:k] = a

    # index = k;
    # for i in range(0, l-1):
    #     t_i[index : index+(k-nu[i])] = xi[i] 
    #     index += (k-nu[i])    

    # t_i[index: index+k] = b

    var = Vars_spline(a, b, xi, k, nu, A, num_dots)
    s = np.zeros((num_dots))
    tau = var.get_tau()
    t = var.get_t()
    for i_tau in range(num_dots):
        s[i_tau] = 0
        acierto = False
        #suma condicional
        for i in range(k*(1+len(nu)+1)-sum(nu)-1):
            if (t[i] <= tau[i_tau] and tau[i_tau] < t[i+1]):
                acierto = True
                s[i_tau] += var.get_a(k-1,i)
            elif (acierto):
                break
                
    
    
    

class Vars_spline:
    def __init__(self, a, b, xi, k, nu, A, num_dots):
        self.tau = np.linspace(a, b, num_dots)
        self.w = {}
        self.t_i = np.zeros( k*(1+len(nu)+1)-sum(nu) )
        self.a = {}  #np.empty((A.shape[0],A.shape[0]))
        self.k = k
        #calc variables
        self._calc_t(a,b,xi,k,nu)

    def get_w(self,i,k):
        return self._calc_w(i,k)

    def get_tau(self):
        return self.tau

    def get_t(self):
        return self.t_i

    def get_a(self,r,i):
        return self._calc_a(r,i)

    def _calc_w(self,i,k):
        if( (i,k) in self.w):
            return self.w[(i,k)]
        else:
            if (t_i[i] == t_i[i+k-1]):
                self.w[(i,k)] = 0
            else:
                self.w[(i,k)] = ((self.tau - t_i[i])/(t_i[i+k-1]-t_i[i]))
            return self.w[(i,k)]

    def _calc_a(self,r,i):
        if ((r,i) in self.a):
            return self.a[(r,i)]
        
        wi = self.get_w(i,k-r-1)
        ai = self._calc_a(r-1,i)
        ai_1 = self._calc_a(r-1,i-1)
        self.a[(r,i)] = (1-wi)* ai_1+wi*ai
        return self.a[(r,i)]


    def _calc_t(self,a,b,xi,k,nu):
        l = len(nu)

        index=0
        self.t_i[0:k] = a

        index = k;
        for i in range(0, l):
            t_i[index : index+(k-nu[i])] = xi[i] 
            index += (k-nu[i])

        t_i[index: index+k] = b



    
    
if __name__=="__main__":
    spline1d(0, 4, [1,2,3], 3, [2,2,2], [0,1], 100)





    
