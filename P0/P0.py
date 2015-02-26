# Luis María Costero Valero (lcostero@ucm.es)
# Jesús Javier Doménech Arellano (jdomenec@ucm.es)
# Jennifer Hernández Bécares (jennhern@ucm.es)

import numpy as np #para crear arrays de puntos
from scipy.integrate import odeint #resolutor de edo
import matplotlib.pyplot as plt #para imprimir la grafica
import math #funciones matematicas


if __name__ == "__main__" :
    #curvatura
    def k(s) :
        #recta    return 0
        #circunferencia return 1
        #polinomio
        return (math.atan(-s*s*s)/math.pi)+0.5

    # condiciones iniciales
    x0, y0 = -2,0 
    dx0, dy0 = 1 , 0
    init_cond = [x0, y0, dx0, dy0]
    
    #intervalo de  definicion
    delta = 1
    #recta interval = np.arange(0, 1 + delta, delta)
    #circunferencia interval = np.arange(0, 2* np.pi + delta, delta)
    #polinomio
    interval = np.arange(-50, 50 + delta, delta)





# Resolver el sistema.
def rhs_eqs(Y,s):
    x, y, dx, dy = Y
    return [dx, dy, -k(s)*dy, k(s)*dx]

solu = odeint(rhs_eqs, init_cond, interval)


#Pintamos la curva
curve_x = [x for [x, y, dx, dy] in solu]
curve_y = [y for [x, y, dx, dy] in solu]

plt.plot(curve_x, curve_y)
plt.axis('equal')
plt.show()


