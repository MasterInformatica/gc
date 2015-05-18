# -*- coding: utf-8 -*-

""" 
Práctica 7 (alg. incremental) de Geometría Computacional
Autores:
* Luis María Costero Valero (lcostero@ucm.es)
* Jesús Javier Doménech Arellano (jdomenec@ucm.es)
* Jennifer Hernández Bécares (jennhern@ucm.es)
"""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
from matplotlib.path import Path
from matplotlib.widgets import Slider, Button
import matplotlib.patches as patches
from incremental import Incremental

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

        self.points = None
        self.convex_hull = None
        self.incremental = None


        # Controlador de Eventos
        self.cid_release_button = self.fig.canvas.mpl_connect('button_release_event', self.on_release)


    def init_interaction(self):
        """
        Se encarga de inicializar la ventana gráfica para ser interactiva. Añade los sliders y botones.
        """
        self.lib = False
        self.other_method = 'newton'
        self.method = 'least_squares'
        self.L = 6
        plt.subplots_adjust(bottom=0.25) # Ajustamos la gráfica para poner los controles debajo, texto encima
        self.fig.suptitle('Click introduce los puntos y puede moverlos.')

        #Buttons
        calculateAxes = plt.axes([0.7, 0.17, 0.15, 0.03])
        resetAxes = plt.axes([0.7, 0.05, 0.15, 0.03])

        self.buttonCalculate = Button(calculateAxes, 'Calculate!')
        self.buttonReset = Button(resetAxes, 'Reset!')

        self.buttonCalculate.on_clicked(self._updatePlot)
        self.buttonReset.on_clicked(self._clean)
        

    def _updatePlot(self):
        """
        Encarga de actualizar los dibujos, llamando a los métodos correspondientes
        """
        # Aquí habría que hacer:
        #  (0) Pintar el nuevo punto
        #  (a) Calcular la nueva convex hull
        #  (b) eliminar todas las lineas
        #  (c) pintar la nueva convex_hull
        self.ax.lines = []

        self.drawPoint(self.points[-1],'g')

        if self.incremental is None:
            self.incremental = Incremental()


        self.convex_hull = self.incremental(self.points[-1])
        self.drawPolygon(self.convex_hull,'-ob')

        
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
        self.ax.add_patch(Circle((p[0],p[1]), 0.3,color=colour))
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
        self.incremental = None

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


        if self.points is None:
            self.points = np.array([[event.xdata, event.ydata]])
        else:
            self.points = np.concatenate((self.points, [[event.xdata, event.ydata]]))

        self._updatePlot()
        self.fig.canvas.draw()


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
if __name__=="__main__":
    window = Graphics()
    window.init_interaction()
    window.show()
                
