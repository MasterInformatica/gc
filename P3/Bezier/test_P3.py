import numpy as np
from casteljau import CurvaDeBezier as cb
from casteljau import compute_bernstein_precomp
 
def eval_bezier(degree, t, stuff_Bezier):
    P = np.random.uniform(-20, 20, (degree + 1, 2))

    # Computamos la curva. Le pasamos True para computar
    # por Bernstein
    curve = cb(P, True, stuff_Bezier)
    return curve #numpy array of size (num_points, 2)
    

def eval_deCasteljau(degree, t, stuff_deCasteljau):
    P = np.random.uniform(-20, 20, (degree + 1, 2))
    
    # Computamos la curva. Le pasamos un False para computar
    # por Casteljau
    curve = cb(P, False, stuff_deCasteljau)
    return curve #numpy array of size (num_points, 2)


    
if __name__ == '__main__':
    import timeit
    degree = 15
    num_points = 100    
    t = np.linspace(0, 1, num_points)
    #enter here stuff you want to precompute 
    stuff_Bezier = None
    stuff_deCasteljau = None

    stuff_Bezier = np.zeros((degree+1, num_points))
    N = degree - 1;
    stuff_Bezier = compute_bernstein_precomp(N, t, stuff_Bezier)

    print(timeit.repeat("eval_bezier(degree, t, stuff_Bezier)",
                        setup="from __main__ import eval_bezier, degree, t, stuff_Bezier",
                        number=10000))
    
    print(timeit.repeat("eval_deCasteljau(degree, t, stuff_deCasteljau)",
                        setup="from __main__ import eval_deCasteljau, degree, t, stuff_deCasteljau",
                        number=10000))

    
    
