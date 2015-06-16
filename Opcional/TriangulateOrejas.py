# -*- coding: utf-8 -*-

""" 
Práctica Opcional de Geometría Computacional
Triangulación de poligonos Y-monotonos
Autores:
* Luis María Costero Valero       (lcostero@ucm.es)
* Jesús Javier Doménech Arellano  (jdomenec@ucm.es)
* Jennifer Hernández Bécares      (jennhern@ucm.es)
"""

from __future__ import division
import bintrees
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
from matplotlib.path import Path
from matplotlib.widgets import Slider, Button
import matplotlib.patches as patches
import numpy as np

def side(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def nextOreja(P,orient):
    #P is clockwise
    oreja = False
    i = -1
    n = len(P)
    while i < n and not oreja:
        i += 1
        a = P[(i-1)%n]
        b = P[(i+1)%n]
        if side(a,b,P[i])*orient > 0:
            oreja = True
            for j in range(n):
                if not(j == i) and not(j == ((i-1)%n)) and not(j == ((i+1)%n)) and side(a,b,P[j])*orient >= 0:
                    oreja = False
                    break
    return (a,b),i

def triangulate(points,clock):
    P = points[:]
    ccl = 1
    if not clock:
        ccl = -1
    diags = []
    while len(P) > 3:
        diag,idx = nextOreja(P,ccl)
        diags = diags + [diag]
        P.pop(idx)
    return diags

def clockwise(p):
    n = len(p)
    count = 0
    for i in range(n):
        j = (i + 1) % n
        k = (i + 2) % n
        sidee = side(p[i],p[j],p[k])
        if (sidee < 0):
            count-=1
        elif (sidee > 0):
            count+=1
    return count < 0
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

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
        self.H1 = bintrees.AVLTree()
        self.H2 = bintrees.AVLTree()
        self.points = None
        self.newpoint = None
        # Controlador de Eventos
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
        

    def _updatePlot(self,event):
        """
        Encarga de actualizar los dibujos, llamando a los métodos correspondientes
        """
        self.ax.lines = []
        diags = triangulate(self.points,clockwise(self.points))
        print diags
        for d in diags:
            self.drawPolygon(d,'-g')
        self.drawPolygon(self.points+[self.points[0]],'-b')

        
    def drawPolygon(self, Pol,colour=None):
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


        
    def drawPoint(self,p,colour):
        """
        Dado un punto y un color, muestra este con ese color en la figura
        """
        self.ax.add_patch(Circle((p[0],p[1]), 0.5,color=colour))
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
        self.points = None
        self.ax.cla()
        self.ax.autoscale(False)
        self.ax.set_xlim(-20,20)
        self.ax.set_ylim(-20,20)
        self.fig.canvas.draw()


    def _clean(self, event):
        self.clean()

    def on_release(self, event):
        if not self.ax.contains(event)[0]: #press out of plot
            return

        self.newpoint = (event.xdata, event.ydata)
        if self.points is None:
            self.points = [self.newpoint]

        else:
            self.points = self.points + [self.newpoint]
        self.drawPoint(self.newpoint,'b')
        #self._updatePlot(event)
        #self.fig.canvas.draw()


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------





def menu():
    poligono = [(0,0),(1,3),(2,2),(3,0),(2,0)]
    print triangulate(poligono)
def men():
    window = Graphics()
    window.init_interaction()
    window.show()


if __name__ == "__main__":
    men()
