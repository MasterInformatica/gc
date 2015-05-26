# -*- coding: utf-8 -*-

""" 
Práctica Opcional de Geometría Computacional
Intersección de N Segmentos
Autores:
* Luis María Costero Valero       (lcostero@ucm.es)
* Jesús Javier Doménech Arellano  (jdomenec@ucm.es)
* Jennifer Hernández Bécares      (jennhern@ucm.es)
"""

from __future__ import division
import sys
import numpy as np
import matplotlib.tri
import time
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
from matplotlib.path import Path
from matplotlib.widgets import Slider, Button
import matplotlib.patches as patches
 
def circumcircle2(T):
    P1,P2,P3=T[:,0], T[:,1], T[:,2]
    b = P2 - P1
    c = P3 - P1
    d=2*(b[:,0]*c[:,1]-b[:,1]*c[:,0])
    center_x=(c[:,1]*(np.square(b[:,0])+np.square(b[:,1]))- b[:,1]*(np.square(c[:,0])+np.square(c[:,1])))/d + P1[:,0]
    center_y=(b[:,0]*(np.square(c[:,0])+np.square(c[:,1]))- c[:,0]*(np.square(b[:,0])+np.square(b[:,1])))/d + P1[:,1]
    return np.array((center_x, center_y)).T
 
def calc_shift(point, vector, bbox):
    c=None
    for l,m in enumerate(bbox):
        a=(m - point[l%2]) / vector[l%2]
        if  a>0:
            if c is None or abs(a)<abs(c):
                c=a
    return c
 
def voronoi2(P, bbox):
    P=np.array(P)

    bbox=np.round(bbox,4)
 
    D = matplotlib.tri.Triangulation(P[:,0],P[:,1])
    T = D.triangles
    n = T.shape[0]
    C = circumcircle2(P[T])
 
    segments = []
    for i in range(n):
        for j in range(3):
            k = D.neighbors[i][j]
            if k != -1:
                #cut segment to part in bbox
                start,end=C[i], C[k]

                segments.append( [start, end] )
            else:

                first, second, third=P[T[i,j]], P[T[i,(j+1)%3]], P[T[i,(j+2)%3]]
                edge=np.array([first, second])
                vector=np.array([[0,1], [-1,0]]).dot(edge[1]-edge[0])
                line=lambda p: (p[0]-first[0])*(second[1]-first[1])/(second[0]-first[0])  -p[1] + first[1]
                orientation=np.sign(line(third))*np.sign( line(first+vector))
                if orientation>0:
                    vector=-orientation*vector
                c=calc_shift(C[i], vector, bbox)
                if c is not None:    
                    segments.append([C[i],C[i]+c*vector])
    return segments



#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
   
class Graphics:
    """
    Contiene los componentes de la ventana gráfica.
    Tiene métodos para pintar elementos en la ventana gráfica. 
    En el método interactivo también se encarga de la gestión de los eventos con el 
    ratón y los widgets de matplotlib
    """
    
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, aspect=1)
        self.ax.autoscale(False)
        self.ax.set_xlim(-20,20)
        self.ax.set_ylim(-20,20)
        self.points_P = []
        self.inter_circle = []
        # Variables para Mover puntos
        self.exists_touched_circle = False
        self.touched_P = True
        self.touched_index = None
        self.touched_x0, self.touched_y0 = None,None
        # Controlador de Eventos
        self.cid_press = self.fig.canvas.mpl_connect('button_press_event', self.on_press)        
        self.cid_move = self.fig.canvas.mpl_connect('motion_notify_event', self.on_move)
        self.cid_release_button = self.fig.canvas.mpl_connect('button_release_event', self.on_release)

    def init_interaction(self):
        """
        Se encarga de inicializar la ventana gráfica para ser interactiva. Añade los sliders y botones.
        """
       
        plt.subplots_adjust(bottom=0.25) # Ajustamos la gráfica para poner los controles debajo, texto encima
        self.fig.suptitle('Click introduce los puntos y puede moverlos.')

        #Buttons
        calculateAxes = plt.axes([0.7, 0.17, 0.15, 0.03])
        resetAxes = plt.axes([0.7, 0.05, 0.15, 0.03])

        self.buttonCalculate = Button(calculateAxes, 'Calculate!')
        self.buttonReset = Button(resetAxes, 'Reset!')

        self.buttonCalculate.on_clicked(self._updatePlot)
        self.buttonReset.on_clicked(self._clean)
        

        for p in self.points_P:
            c = Circle((p[0], p[1]), 0.5,color='b')
            self.ax.add_patch(c)
        self._updatePlot(None)

    def _updatePlot(self, event):
        """
        Encarga de actualizar los dibujos, llamando a los métodos correspondientes
        """
        self.ax.lines = []
        if len(self.points_P)<3:
            return
        lines=voronoi2(self.points_P, (-20,-20, 100, 100))
        for l in lines:
            self.drawPolygon(l)

    def drawLine(self,line):
        """ 
        Dada una 2Dline por parámetro, la muestra en la figura
        """
        self.ax.add_line(line)
        self.fig.canvas.draw()


    def drawPolygon(self, Pol, colour=None):
        """ 
        Pinta los poligonos definido en Pol
        """

        x = [k[0] for k in Pol]
        y = [k[1] for k in Pol]
        if colour is None:
            self.ax.plot(x,y)
        else:
            self.ax.plot(x,y,colour)
        self.fig.canvas.draw()
        
    def drawPoints(self, points, colour):
        """
        Dado un punto y un color, muestra este con ese color en la figura
        """
        if points.shape[0] != 0:
            for p in points:
                c = Circle((p[0],p[1]),0.3,color=colour)
                self.inter_circle.append(c)
                self.ax.add_patch(c)

        self.fig.canvas.draw()

        
    def show(self):
        """
        realiza el show del plot
        """
        plt.show()

    def clean(self):
        """
        Borra todos los elementos de la gráfica. Lineas y circulos
        """
        self.points_P = []
        for c in self.inter_circle:
            c.remove()
        self.inter_circle = []
        self.ax.cla()
        self.ax.autoscale(False)
        self.ax.set_xlim(-20,20)
        self.ax.set_ylim(-20,20)
        for p in self.points_P:
            c = Circle((p[0], p[1]), 0.5,color='b')
            self.ax.add_patch(c)
        #self._updatePlot(None)
        self.fig.canvas.draw()

    def _clean(self, event):
        self.clean()

    def on_press(self, event):
        """ 
        Controlador del evento asociado a pinchar en la gráfica.
        """
        if not self.ax.contains(event)[0]: #press out of plot
            return
        for circle in self.ax.patches:
            contains, attr = circle.contains(event)
            if contains:
                self.touched_circle = circle
                self.exists_touched_circle = True
                self.pressed_event = event
                self.touched_x0, self.touched_y0 = circle.center
                punto = [self.touched_x0, self.touched_y0]
                if punto in self.points_P:
                    self.touched_index = self.points_P.index(punto)
                    self.touched_P = True
                return

        if event.button == 1:
            self.points_P.append([event.xdata, event.ydata])
            c = Circle((event.xdata, event.ydata), 0.5,color='b')
        else:
            return
        self.ax.add_patch(c)
        self.fig.canvas.draw()


    def on_release(self, event):
        if not self.ax.contains(event)[0]: #press out of plot
            return
        # Reseteamos la variable al soltar el boton del raton
        self.exists_touched_circle = False
        self._updatePlot(event)
        self.fig.canvas.draw()
        return

    def on_move(self, event):
        if not self.ax.contains(event)[0]: #press out of plot
            return
        # Si habiamos pinchado encima de un circulo existente y lo intentamos
        # mover, se actualiza el poligono en consecuencia, se modifican los
        # valores
        if self.exists_touched_circle:
            dx = event.xdata - self.pressed_event.xdata
            dy = event.ydata - self.pressed_event.ydata
            x0, y0 = self.touched_circle.center
            self.touched_circle.center = self.touched_x0+dx, self.touched_y0+dy
            #Actualizar arrays
            if self.touched_P:
                self.points_P[self.touched_index] = [self.touched_x0+dx, self.touched_y0+dy]
            self._updatePlot(event)
            self.fig.canvas.draw()

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

def men():
    """
    Si iniciamos la aplicación de manera directa, inicilizamos la ventana
    gráfica para ser interactiva
    """
    window = Graphics()
    window.init_interaction()
    window.show()

def menu():
    points=np.random.rand(100,2)*100  
    lines=voronoi2(points, (-20,-20, 10, 10))



    plt.scatter(points[:,0], points[:,1], color="blue")
    lines = matplotlib.collections.LineCollection(lines, color='red')
    plt.gca().add_collection(lines)
    plt.axis((-20,120, -20,120))
    plt.show()

if __name__ == "__main__":
    men()
