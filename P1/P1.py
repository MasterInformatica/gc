import sympy as sp  #calculo simbolico
from sympy.utilities.lambdify import lambdify
from sympy.interactive import printing
import numpy as np
printing.init_printing(use_latex=True)


t0,t1 = sp.symbols('t0, t1')

if __name__ == "__main__":
    #curvas: 
    #  Gamma=c(t0)=(x0(t0), y0(t0))
    x0, y0 = 2*sp.cos(t0), 3*sp.sin(t0)
    #  Gamma=c(t1)=(x1(t1), y1(t1))
    x1, y1 = 3*sp.cos(t1), 2*sp.sin(t1)

    intervalo0 = [0, 2*sp.pi]
    intervalo1 = [0, 2*sp.pi]

    # Porcentaje para calcular el numero de 0
    porcentaje = 0.05
    # Numero de puntos a tomar en el intervalo
    puntos_intervalo = 100
    # eps: Error al comparar los puntos
    eps = 10**(-9)



# calcula la signatura de c(t)=(x(t), y(t)) en funcion de t
# Devuelve el par ( K(s), dK/ds )
def sig(x, y, t):
    #primeras derivadas
    dx = sp.diff(x,t)
    dy = sp.diff(y,t)

    #segundas derivadas
    d2x = sp.diff(dx, t)
    d2y = sp.diff(dy, t)

    determinante = (dx * d2y) - (dy * d2x)
    norma = sp.sqrt(dx**2 + dy**2)

    K = determinante / norma**3
    dKdt = sp.diff(K, t)
    dKds = (1 / norma) * dKdt

    return (K.simplify(), dKds.simplify())



#obtenemos las signaturas y las convertimos a numpy
sig0 = sig(x0, y0, t0)
sig1 = sig(x1, y1, t1)

num_sig0 = lambdify(t0, sig0, [{'ImmutableMatrix': np.array}, 'numpy'])
num_sig1 = lambdify(t1, sig1, [{'ImmutableMatrix': np.array}, 'numpy'])


#puntos a evaluar
paso0 = (intervalo0[1] - intervalo0[0]) / puntos_intervalo
paso1 = (intervalo1[1] - intervalo1[0]) / puntos_intervalo

puntos0 = np.arange(intervalo0[0], intervalo0[1]+paso0, paso0)
puntos1 = np.arange(intervalo1[0], intervalo1[1]+paso1, paso1)

evaluacion0=[]; evaluacion1=[];
#evaluacion de la signatura
for i in range(puntos_intervalo):
    evaluacion0.append(num_sig0(puntos0[i]))
    evaluacion1.append(num_sig1(puntos1[i]))

distancias = scipy.spatial.distance.cdist(evaluacion0, evaluacion1, 'euclidean')

print distancias

