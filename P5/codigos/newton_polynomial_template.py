import numpy as np
import matplotlib.pyplot as plt

def newton_polynomial(x, tau, num_points=50, libraries=False):
    #your code here
    if libraries == False:
        #your code here        
        return polynomial #np.array of size num_points
    else:
        #your code here
        return another_polynomial #np.array of size num_points
    
if __name__ == '__main__':
    n = 10  
    tau = np.arange(n)
    x = np.random.randint(-10, 10, size=n)
    num_points = 100
    poly_0 = newton_polynomial(x, tau, num_points, libraries=False)
    poly_1 = newton_polynomial(x, tau, num_points, libraries=True)
    print np.linalg.norm(poly_0 - poly_1)
    
    t = np.linspace(tau[0], tau[-1], num_points)    
    plt.plot(t, poly_0)
    plt.plot(tau, x, 'o')
    plt.show()
    
    
    import timeit
    
    print(timeit.repeat("x = np.random.randint(-10, 10, size=n); newton_polynomial(x, tau, libraries=False)",
                        setup="from __main__ import newton_polynomial, n,  tau, np",
                        number=10000))
    print(timeit.repeat("x = np.random.randint(-10, 10, size=n); newton_polynomial(x, tau, libraries=True)",
                        setup="from __main__ import newton_polynomial, n,  tau, np",
                        number=10000))
