#######################################################################################################
# Comentario super tocho de por qué no funciona este método.                                          #
#                                                                                                     #
#   La idea de que este método no funciona es que según el orden en el                                #
#   que se calculen los puntos, y en el que se comparen, dará como resultado                          #
#   puntos distintos, incluso un número distinto de puntos dependiendo del caso.                      #
#   Esto hace que si Antonio quiere eliminar duplicados para pasar el test,                           #
#   ni siquiera vamos a tener el mismo número de puntos en algunas ocasiones.                         #
#                                                                                                     #
#   A lo mejor se refiere a eliminar duplicados tal cual, no a una distancia eps.                     #
#   Por ejemplo, el hecho de coger los polinomios en el _subdivision con uno u otro orden             #
#   ya producirá puntos distintos.                                                                    #
#                                                                                                     #
# Y para muestra un botón:                                                                            #
#                                                                                                     #
#   Sea epsilon = 1. Imaginemos los puntos (0,0), (1,0) y (2,0). Que están a distancia eps.           #
#                                                                                                     #
#   Si empezamos con el (1,0). Intentamos añadir el (0,0), pero como está a distancia eps, no se      #
#      añade. Igual pasa con el (2,0). Por lo que el resutlado final es el {(1,0)}                    #
#                                                                                                     #
#   Empecemos ahora con el (0,0). Intentamos añadir el (1,0), pero no podemos porque está a distancia #
#      eps. Pero ahora al añadir el punto (2,0), como está a 2*eps del (0,0), podemos añadirlo,       #
#      quedando como resultado el {(0,0),(2,0)}                                                       #
#######################################################################################################



import numpy as np


eps = 0.1
A = np.array([[1,2],[3,4]])
B = np.array([[5,6],[7,8],[9,2]])

for point in B:
    if not (np.amin(np.linalg.norm(A-point)) < eps):
        A = np.append(  A ,  [point], axis=0)

print A
