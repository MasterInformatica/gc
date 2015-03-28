import unittest
import timeit
import numpy as np
from intersection_bezier import IntersectionBezier


 
def eval_intersect(N, epsilon):
    P = np.random.uniform(-20, 20, (N + 1, 2))
    Q = np.random.uniform(-20, 20, (N + 1, 2))
    return intersect(P, Q, epsilon)


    
if __name__ == '__main__':
    
    N = 15  
    epsilon = 0.1
    intersect = IntersectionBezier()
    
   # intersect(P, Q, epsilon)

    #unittest.main()
    print(timeit.repeat("eval_intersect(N, epsilon)",
                        setup="from __main__ import eval_intersect, intersect, N, epsilon",
                        number=10))



#tiempos obtenidos en el aula III
#[2.9526281356811523, 3.1017611026763916, 3.3952529430389404]
    
   
    
    
