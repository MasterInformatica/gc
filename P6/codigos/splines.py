def spline2d(a, b, xi, k, nu, A, num_dots):
    '''Computes a plane spline curve of order k
       defined on the interval [a, b] with knots psi,
       multiplicities nu and coefficiets A.
       Parameters:
       a, b -- ends of the interval, real numbers
       xi -- list of breakpoints, a < xi[0] < .. < xi[-1] < b
       k -- order of the curve, the degree is <= k-1
       nu -- list of inteer multiplicities of each breakpint,
             len(psi) = len(nu), 1 <= nu[i] < k
      A -- list of coefficients of the B-spline basis,
           A = [[x0, y0], [x1, y1],..., [x[N], y[N]]
      num_dots -- number of dots of the spline to be plotted,
                  uniformly spaced alogn the interval [1, b]
      Returns:
      the spline curve as a numpy array of size (2, num_dots) '''
