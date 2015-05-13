# -*- coding: utf-8 -*-

""" 
Práctica 7 de Geometría Computacional
Autores:
* Luis María Costero Valero       (lcostero@ucm.es)
* Jesús Javier Doménech Arellano  (jdomenec@ucm.es)
* Jennifer Hernández Bécares      (jennhern@ucm.es)
"""

from __future__ import division
import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.lines import Line2D
# from matplotlib.patches import Circle
# from matplotlib.path import Path
# from matplotlib.widgets import Slider, Button
# import matplotlib.patches as patches
# from scipy.spatial.distance import cdist

def maxDistancePoint(a,b,points):
    #if(points.shape[0]<=1):
    b_a = b-a
    p_a = points-a
    norma = np.linalg.norm(b_a)
    dist = ((b_a[0]*p_a[:,1])-(p_a[:,0]*b_a[0]))*1.0/norma
    return points[np.argmax(dist)]


def _quickHull(a,b,points):
    if(points.shape[0]<=1):
        return points
    else:
        c = maxDistancePoint(a,b,points)
        A,_ = separate(a,c,points)
        B,_ = separate(c,b,points)
        return np.vstack((_quickHull(a,c,A),c,_quickHull(c,b,B)))

def separate(a,b,P):
    dist = (b[0]-a[0])*(P[:,1]-a[1])-(b[1]-a[1])*(P[:,0]-a[0])
    return P[dist > 0],P[dist < 0]

def extremos(points):
    return points[0],points[-1]

def convex_hull(points):
    points = np.array(sorted(points))
    m,M = extremos(points)
    L,R = separate(m,M,points)
    aux = np.vstack((m,_quickHull(m,M,L),M,_quickHull(M,m,R),m))
    return aux
# #--------------------------------------------------------------------------
# #--------------------------------------------------------------------------
   
# class Graphics:
#     """
#     Contiene los componentes de la ventana gráfica.
#     Tiene métodos para pintar elementos en la ventana gráfica. 
#     En el método interactivo también se encarga de la gestión de los eventos con el 
#     ratón y los widgets de matplotlib
#     """
    
#     def __init__(self):
#         self.fig = plt.figure()
#         self.ax = self.fig.add_subplot(111, aspect=1)
#         self.ax.autoscale(False)
#         self.ax.set_xlim(-20,20)
#         self.ax.set_ylim(-20,20)
#         self.points_P = []
#         self.inter_circle = []
#         # Variables para Mover puntos
#         self.exists_touched_circle = False
#         self.touched_P = True
#         self.touched_index = None
#         self.touched_x0, self.touched_y0 = None,None
#         # Controlador de Eventos
#         self.cid_press = self.fig.canvas.mpl_connect('button_press_event', self.on_press)        
#         self.cid_move = self.fig.canvas.mpl_connect('motion_notify_event', self.on_move)
#         self.cid_release_button = self.fig.canvas.mpl_connect('button_release_event', self.on_release)


#     def init_interaction(self):
#         """
#         Se encarga de inicializar la ventana gráfica para ser interactiva. Añade los sliders y botones.
#         """
       
#         plt.subplots_adjust(bottom=0.25) # Ajustamos la gráfica para poner los controles debajo, texto encima
#         self.fig.suptitle('Click introduce los puntos y puede moverlos.')

#         #Buttons
#         calculateAxes = plt.axes([0.7, 0.17, 0.15, 0.03])
#         resetAxes = plt.axes([0.7, 0.05, 0.15, 0.03])

#         self.buttonCalculate = Button(calculateAxes, 'Calculate!')
#         self.buttonReset = Button(resetAxes, 'Reset!')

#         self.buttonCalculate.on_clicked(self._updatePlot)
#         self.buttonReset.on_clicked(self._clean)
        

#         #self.points_P = [[-3, 3], [8, 2], [-4, 8], [0, 8], [-1, 0]]
#         self.points_P = [[1,2],[3,3],[5,6],[0,10],[3,5],[6,5],[0,9]]
#         for p in self.points_P:
#             c = Circle((p[0], p[1]), 0.5,color='b')
#             self.ax.add_patch(c)
#         self._updatePlot(None)

#     def _updatePlot(self, event):
#         """
#         Encarga de actualizar los dibujos, llamando a los métodos correspondientes
#         """
#         #self.drawPoints(np.array(self.points_P), 'g')
#         #self.drawPolygon(np.array(self.points_P))
#         self.ax.lines = []
#         convex = convex_hull(self.points_P)
#         if (convex == []):
#             return
#         self.drawPolygon(np.array(convex))

#     def drawLine(self,line):
#         """ 
#         Dada una 2Dline por parámetro, la muestra en la figura
#         """
#         self.ax.add_line(line)
#         self.fig.canvas.draw()


#     def drawPolygon(self, Pol, colour=None):
#         """ 
#         Pinta los poligonos definido en Pol
#         """
#         #plt.plot(Pol[:,0], Pol[:,1], 'bo-')

#         x = Pol[:,0]#[k[0] for k in Pol]
#         y = Pol[:,1]#[k[1] for k in Pol]
#         if colour is None:
#             self.ax.plot(x,y)
#         else:
#             self.ax.plot(x,y,colour)
#         self.fig.canvas.draw()
        
#     def drawPoints(self, points, colour):
#         """
#         Dado un punto y un color, muestra este con ese color en la figura
#         """
#         if points.shape[0] != 0:
#             for p in points:
#                 c = Circle((p[0],p[1]),0.3,color=colour)
#                 self.inter_circle.append(c)
#                 self.ax.add_patch(c)

#         self.fig.canvas.draw()

        
#     def show(self):
#         """
#         realiza el show del plot
#         """
#         plt.show()

#     def clean(self):
#         """
#         Borra todos los elementos de la gráfica. Lineas y circulos
#         """
#         self.points_P = []
#         for c in self.inter_circle:
#             c.remove()
#         self.inter_circle = []
#         self.ax.cla()
#         self.ax.autoscale(False)
#         self.ax.set_xlim(-20,20)
#         self.ax.set_ylim(-20,20)
#         for p in self.points_P:
#             c = Circle((p[0], p[1]), 0.5,color='b')
#             self.ax.add_patch(c)
#         #self._updatePlot(None)
#         self.fig.canvas.draw()


#     def _clean(self, event):
#         self.clean()

#     def on_press(self, event):
#         """ 
#         Controlador del evento asociado a pinchar en la gráfica.
#         """
#         if not self.ax.contains(event)[0]: #press out of plot
#             return
#         for circle in self.ax.patches:
#             contains, attr = circle.contains(event)
#             if contains:
#                 self.touched_circle = circle
#                 self.exists_touched_circle = True
#                 self.pressed_event = event
#                 self.touched_x0, self.touched_y0 = circle.center
#                 punto = [self.touched_x0, self.touched_y0]
#                 if punto in self.points_P:
#                     self.touched_index = self.points_P.index(punto)
#                     self.touched_P = True
#                 return

#         if event.button == 1:
#             self.points_P.append([event.xdata, event.ydata])
#             c = Circle((event.xdata, event.ydata), 0.5,color='b')
#         else:
#             return
#         self.ax.add_patch(c)
#         self.fig.canvas.draw()


#     def on_release(self, event):
#         if not self.ax.contains(event)[0]: #press out of plot
#             return
#         # Reseteamos la variable al soltar el boton del raton
#         self.exists_touched_circle = False
#         self._updatePlot(event)
#         self.fig.canvas.draw()
#         return

#     def on_move(self, event):
#         if not self.ax.contains(event)[0]: #press out of plot
#             return
#         # Si habiamos pinchado encima de un circulo existente y lo intentamos
#         # mover, se actualiza el poligono en consecuencia, se modifican los
#         # valores
#         if self.exists_touched_circle:
#             dx = event.xdata - self.pressed_event.xdata
#             dy = event.ydata - self.pressed_event.ydata
#             x0, y0 = self.touched_circle.center
#             self.touched_circle.center = self.touched_x0+dx, self.touched_y0+dy
#             #Actualizar arrays
#             if self.touched_P:
#                 self.points_P[self.touched_index] = [self.touched_x0+dx, self.touched_y0+dy]
#             self._updatePlot(event)
#             self.fig.canvas.draw()

# # ---------------------------------------------------------------------------
# # ---------------------------------------------------------------------------


# if __name__ == '__main__':
#     # print right_Points([0,0],[4,0],[[1,1],[2,1],[1,-1],[2,-1],[2,0]])
#     print convex_hull( [[-1, 0], [1, 0], [1, 1], [-1, 0], [1, 0], [1, 1],[-10,-5],[10,5],[-10,0],[-10,-10],[10,0],[10,10]])

# if __name__ == '__main__':
#     """
#     Si iniciamos la aplicación de manera directa, inicilizamos la ventana
#     gráfica para ser interactiva
#     """
#     window = Graphics()
#     window.init_interaction()
#     window.show()

                
