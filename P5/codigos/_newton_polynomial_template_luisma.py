from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

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
    
    #your code here
    if libraries == False:
        return polynomial #np.array of size num_points
    else:
        return interp_with_library(x,tau,num_points) #np.array of size num_points
    

def interp_with_library(x, tau, num_points):
    '''
    Interpola resolviendo el sistema con la matriz de Vandermonde
    '''

    #A = np.fliplr(np.vander(tau))
#    A = np.vander(tau)
    coeffs = np.linalg.solve(A, x)

    #coeffs = np.flipud(coeffs)

    times = np.linspace(tau[0], tau[-1], num_points)
    return np.polyval(coeffs, times)




def eval_pol(a, tau, num_points):
    N = a.shape[0]-1; # ultimo indice accesible

    x = np.linspace(tau[0], tau[-1], num_points)

    sol = a[N] * np.ones(num_points)
    for k in range(N-1, -1, -1):
        sol = a[k]  + (x-tau[k])*sol
        

    return sol



if __name__ == '__main__':
    #ONLY FOR TESTING PURPOSES
    n = 10
    tau = np.arange(n)       
    x = np.random.randint(-10, 10, size=n)
    num_points = 100 

    poly_0 = newton_polynomial(x, tau, num_points, libraries=True)

    t = np.linspace(tau[0], tau[-1], num_points)

    plt.plot(t, poly_0)
    plt.plot(tau, x, 'o')
    plt.show()


    
    n = 10                                                                                                    #
    tau = np.arange(n)                                                                                        #
    x = np.random.randint(-10, 10, size=n)                                                                    #
    num_points = 100                                                                                          #
    # poly_0 = newton_polynomial(x, tau, num_points, libraries=False)                                           #
    # poly_1 = newton_polynomial(x, tau, num_points, libraries=True)                                            #
    # print np.linalg.norm(poly_0 - poly_1)                                                                     #
    #                                                                                                           #
    # t = np.linspace(tau[0], tau[-1], num_points)                                                              #
    # plt.plot(t, poly_0)                                                                                       #
    # plt.plot(tau, x, 'o')                                                                                     #
    # plt.show()                                                                                                #
                                                                                                              #
                                                                                                              #
    import timeit                                                                                             #
    #                                                                                                           #
    # print(timeit.repeat("x = np.random.randint(-10, 10, size=n); newton_polynomial(x, tau, libraries=False)", #
    #                     setup="from __main__ import newton_polynomial, n,  tau, np",                          #
    #                     number=10000))                                                                        #
    print(timeit.repeat("x = np.random.randint(-10, 10, size=n); newton_polynomial(x, tau, libraries=True)",  #
                        setup="from __main__ import newton_polynomial, n,  tau, np",                          #
                        number=10000))                                                                        #
    
