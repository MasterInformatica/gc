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
import matplotlib.pyplot as plt
import time


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
    A = np.array(A)
    xi = np.array(xi)
    nu = np.array(nu)

    var = Vars_spline(a, b, xi, k, nu, A, num_dots)
    n_ts = k*(1+nu.shape[0]+1)-np.sum(nu)
    s = np.zeros((2,num_dots))
    tau = var.get_tau()
    t = var.get_t()
    index = 0

    for i_tau in range(num_dots):
        # Paso 1: Avanzar el indice hasta que se pueda operar
        while (index < n_ts-2 and t[index+1] <= tau[i_tau]):
            index += 1
        
        # Paso 2: Sumamos a(k-1,index,tau)
        if (t[index] <= tau[i_tau] and tau[i_tau] <= t[index+1]):
            s[:,i_tau] =  (var._calc_a(k-1,index))[:,i_tau]

    return s
    

class Vars_spline:
    def __init__(self, a, b, xi, k, nu, A, num_dots):
        self.tau = np.linspace(a, b, num_dots)
        self.w = {}
        self.t_i = np.zeros( k*(1+nu.shape[0]+1)-sum(nu)+1)
        self.a = {}  #np.empty((A.shape[0],A.shape[0]))
        self.k = k
        #calc variables
        self._calc_t(a,b,xi,k,nu)
        self.A = A
        self.num_dots = num_dots
#        for i in range(A.shape[0]):
#            self.a[(0,i)] = np.full(num_dots,A[i])

    def get_tau(self):
        return self.tau

    def get_t(self):
        return self.t_i

    def _calc_w(self,i,k):
        if( (i,k) in self.w):
            return self.w[(i,k)]
        if (self.t_i[i] == self.t_i[i+k-1]):
            self.w[(i,k)] = np.zeros(self.tau.shape[0])
        else:
            self.w[(i,k)] = ((self.tau - self.t_i[i])*1.0/(self.t_i[i+k-1]-self.t_i[i])*1.0)
        return self.w[(i,k)]

    def _calc_a(self,r,i):
        if ((r,i) in self.a):
            return self.a[(r,i)]
        if (r==0):
            self.a[(r,i)]=self.A[i]
            return self.a[(r,i)]
        wi = self._calc_w(i,self.k-r+1)
        ai_1 = self._calc_a(r-1,i-1)
        ai = self._calc_a(r-1,i)
        aux = np.zeros((2,self.num_dots))
        aux[0] = (1-wi)*ai_1[0] + wi*ai[0]
        aux[1] = (1-wi)*ai_1[1] + wi*ai[1]

        self.a[(r,i)] = aux
        return self.a[(r,i)]

   
    # Segun la formula para cada t entre tj y tj+1 
    # usamos una combinacion de puntos aj-k+r+1 hasta aj


    def _calc_t(self,a,b,xi,k,nu):
        l = nu.shape[0]
        index=0
        self.t_i[0:k] = a
        index = k+1
        for i in range(0, l):
            self.t_i[index : index+(k-nu[i])] = xi[i] 
            index += (k-nu[i])
        self.t_i[index: index+k] = b



    

def menu1():
    A = [[-3, 3], [-3, 3], [-3, 3], [8, 2], [-4, 8], [0, 8], [-1, 0], [-1, 0], [-1, 0]]
    s = spline2d(0, 4, [1,2,3], 3, [2,2,2], A, 100)
    print s[0]
    print s[1]
    nA = np.array(A)
    plt.plot(nA[:,0],nA[:,1],'-o')
    plt.plot(s[0],s[1])
    plt.show()

def menu2():
    A = [[5, -4], [5, -4], [8, -1], [-9, -8], [7, 7], [5, 7], [5, 7]]
    s = spline2d(0, 4, [1,2,3], 2, [1,1,1], A, 10000)
    print s[0]
    print s[1]
    nA = np.array(A)
    plt.plot(nA[:,0],nA[:,1],'-o')
    plt.plot(s[0],s[1])
    plt.show()

    
#if __name__=="__main__":
#    menu1()
#    menu2()
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

    
