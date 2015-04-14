from newtdd import newtdd
from nest   import nest
import matplotlib.pyplot as plt
import numpy as np

#xdata = [0.0,1,2,3,3.4]
#ydata = [0.0,3,12,6,2]

n = 10  
tau = np.arange(n)
x = np.random.randint(-10, 10, size=n)

num_points = 100

print 'tau', tau
print 'x', x

plt.plot(tau,x)

interpolant = newtdd(tau,x)
print 'interpolant', interpolant


t = np.linspace(tau[0],tau[-1], num_points)
print 't',t


y = nest(interpolant,t,tau)
print 'y', y

plt.plot(t,y,'b')
plt.show()
