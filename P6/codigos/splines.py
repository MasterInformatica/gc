# -*- coding: utf-8 -*-


# QUITAR LA F


""" 
Práctica 6 de Geometría Computacional
Autores:
* Luis María Costero Valero       (lcostero@ucm.es)
* Jesús Javier Doménech Arellano  (jdomenec@ucm.es)
* Jennifer Hernández Bécares      (jennhern@ucm.es)
"""

from __future__ import division
import numpy as np
import time


def spline2d(a, b, xi, k, nu, A, num_dots,F):
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
    A = np.array(A)
    sol = np.zeros((2, num_dots))
    sol[0] = spline1d(a, b, np.array(xi), k, np.array(nu), A[:,0], num_dots,F)
    sol[1] = spline1d(a, b, np.array(xi), k, np.array(nu), A[:,1], num_dots,F)
    return sol




def spline1d(a, b, xi, k, nu, A, num_dots,F):

    var = Vars_spline(a, b, xi, k, nu, A, num_dots)
    n_ts = k*(1+nu.shape[0]+1)-np.sum(nu)
    s = np.zeros(num_dots)
    tau = var.get_tau()
    t = var.get_t()
    index = 0
    for i_tau in range(num_dots):
        # Paso 1: Avanzar el indice hasta que se pueda operar
        while (index < n_ts-2 and t[index+1] <= tau[i_tau]):
            index += 1
        
        # Paso 2: Sumamos a(k-1,index,tau)
        if (t[index] <= tau[i_tau] and tau[i_tau] < t[index+1]):
            if (F):
                z =  (var.get_a(k-1,index))[i_tau]
            else:
                z =  (var.get_a_tau(k-1,index,tau[i_tau]))
            s[i_tau] = z
        # Caso especial: si es igual al ultimo t_i
        elif (index == n_ts-2 and t[index] <= tau[i_tau] and tau[i_tau] <= t[index+1]):
            if (F):
                z =  (var.get_a(k-1,index))[i_tau]
            else:
                z =  (var.get_a_tau(k-1,index,tau[i_tau]))
            s[i_tau] = z
    return s
   
    
    

class Vars_spline:
    def __init__(self, a, b, xi, k, nu, A, num_dots):
        self.tau = np.linspace(a, b, num_dots)
        self.w = {}
        self.t_i = np.zeros( k*(1+nu.shape[0]+1)-sum(nu))
        self.a = {}  #np.empty((A.shape[0],A.shape[0]))
        self.k = k
        #calc variables
        self._calc_t(a,b,xi,k,nu)
        
        for i in range(A.shape[0]):
            self.a[(0,i)] = np.full(num_dots,A[i])
            
            for j in range(self.tau.shape[0]):
                self.a[(0,i,self.tau[j])]=A[i]

    def get_w(self,i,k):
        return self._calc_w(i,k)

    def get_tau(self):
        return self.tau

    def get_t(self):
        return self.t_i

    def get_a(self,r,i):
        return self._calc_a(r,i)

    def get_a_tau(self,r,i,tau):
        return self._calc_a_tau(r,i,tau)

    def _calc_w(self,i,k):
        print "Calc w, las variables valen i:", i, " p:", k
        if( (i,k) in self.w):
            return self.w[(i,k)]
        else:
            if (self.t_i[i] == self.t_i[i+k-1]):
                self.w[(i,k)] = np.zeros(self.tau.shape[0])
            else:
                self.w[(i,k)] = ((self.tau - self.t_i[i])/(self.t_i[i+k-1]-self.t_i[i]))
            return self.w[(i,k)]

    def _calc_a(self,r,i):
        if ((r,i) in self.a):
            return self.a[(r,i)]
        wi = self._calc_w(i,self.k-r+1)
        ai_1 = self._calc_a(r-1,i-1)
        ai = self._calc_a(r-1,i)
        self.a[(r,i)] = (1-wi)*ai_1+wi*ai
        return self.a[(r,i)]

    def _calc_w_tau(self,i,k,tau):
        if( (i,k,tau) in self.w):
            return self.w[(i,k,tau)]
        else:
            if (self.t_i[i] == self.t_i[i+k-1]):
                self.w[(i,k,tau)] = 0
            else:
                self.w[(i,k,tau)] = ((tau - self.t_i[i])/(self.t_i[i+k-1]-self.t_i[i]))
            return self.w[(i,k,tau)]

    def _calc_a_tau(self,r,i,tau):
        if ((r,i,tau) in self.a):
            return self.a[(r,i,tau)]
        
        wi = self._calc_w_tau(i,self.k-r+1,tau)
        ai = self._calc_a_tau(r-1,i,tau)
        ai_1 = self._calc_a_tau(r-1,i-1,tau)
        self.a[(r,i,tau)] = (1-wi)*ai_1+wi*ai
        return self.a[(r,i,tau)]

    def _calc_t(self,a,b,xi,k,nu):
        l = nu.shape[0]

        index=0
        self.t_i[0:k] = a
        index = k;
        for i in range(0, l):
            self.t_i[index : index+(k-nu[i])] = xi[i] 
            index += (k-nu[i])

        self.t_i[index: index+k] = b



    
    
if __name__=="__main__":
    # N = 1000
    # start = time.time()
    # for i in range(N):
    #     spline2d(0, 4, [1,2,3], 3, [2,2,2], [[-3, 3], [-3, 3], [-3, 3], [8, 2], [-4, 8], [0, 8], [-1, 0], [-1, 0], [-1, 0]], 100,False)
    # print "Suelto: ", time.time()-start
    # print "***********************---------------------------------------******************"
    # start = time.time()
    # for i in range(N):
    #     spline2d(0, 4, [1,2,3], 3, [2,2,2], [[-3, 3], [-3, 3], [-3, 3], [8, 2], [-4, 8], [0, 8], [-1, 0], [-1, 0], [-1, 0]], 100,True)
    # print "Matriz: ", time.time()-start
    print spline2d(0, 4, [1,2,3], 3, [2,2,2], [[-3, 3], [-3, 3], [-3, 3], [8, 2], [-4, 8], [0, 8], [-1, 0], [-1, 0], [-1, 0]], 100, True)

    
