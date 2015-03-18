import numpy as np


 
def eval_bezier(degree, t):
    P = np.random.uniform(-20, 20, (degree + 1, 2))
    
    #enter here your computations
    curve = None #delete this line
    return curve #numpy array of size (num_points, 2)
    

def eval_deCasteljau(degree, t):
    P = np.random.uniform(-20, 20, (degree + 1, 2))
    
    #enter here your computations
    curve = None #delete this line
    return curve #numpy array of size (num_points, 2)


    
if __name__ == '__main__':
    import timeit
    degree = 15
    num_points = 100    
    t = np.linspace(0, 1, num_points)
    #enter here stuff you want to precompute 
    stuff_Bezier = None
    stuff_deCasteljau = None
    
    print(timeit.repeat("eval_bezier(degree, t)",
                        setup="from __main__ import eval_bezier, degree, t, stuff_Bezier",
                        number=10000))
    
    print(timeit.repeat("eval_deCasteljau(degree, t)",
                        setup="from __main__ import eval_deCasteljau, degree, t, stuff_deCasteljau",
                        number=10000))

    
    
