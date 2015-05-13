# -*- coding: utf-8 -*-

""" 
Práctica 6 de Geometría Computacional
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


def right_turn(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    
    

def convex_hull(points):
    # Sort the points by x-coordinate, resulting in a sequence
    # p1,...,pn
    ordered_points = sorted(points)
    n = len(ordered_points)

    if n <= 1:
        return []
    # Put the points p1 and p2 in a list Lupper, with p1 as the first
    # point
    Lupper = [ordered_points[0], ordered_points[1]]
    p=ordered_points
    for i in range(2,n):
        Lupper.append(ordered_points[i])
        # while Lupper contains more than two points and the last
        # three points in Lupper do not make a right turn: delete the
        # middle of the last three points from Lupper
        while len(Lupper) > 2 and right_turn(Lupper[-3],
                                             Lupper[-2], Lupper[-1])<=0:
            Lupper.pop(-2) # We delete the middle of the last three
                           # points put the points pn and pn-1 in a
                           # list Llower, with pn as the first point
    Llower = [Lupper[-1], Lupper[-2]]
    for i in range(n-2, -1, -1): # for i<- n-2 downto 1 Append pi to
                                # Llower
        #print i, p[i], Llower
        Llower.append(ordered_points[i])
        
        # while Llower contains more than 2 points and the last three
        # points in Llower do not make a right turn, deletethe middle
        # of the last three points from Llower.
        while len(Llower)>2 and right_turn(Llower[-3], Llower[-2],
                                           Llower[-1]) <= 0:
            Llower.pop(-2)
    Llower.pop(0) 
    Llower.pop(-1)
    list = Lupper + Llower
    list = [list[0]]+ list[::-1]
    return list




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
        

        #self.points_P = [[-3, 3], [8, 2], [-4, 8], [0, 8], [-1, 0]]
        self.points_P = [[1,2],[3,3],[5,6],[0,10],[3,5],[6,5],[0,9]]
        for p in self.points_P:
            c = Circle((p[0], p[1]), 0.5,color='b')
            self.ax.add_patch(c)
        self._updatePlot(None)

    def _updatePlot(self, event):
        """
        Encarga de actualizar los dibujos, llamando a los métodos correspondientes
        """
        #self.drawPoints(np.array(self.points_P), 'g')
        #self.drawPolygon(np.array(self.points_P))
        self.ax.lines = []
        convex = convex_hull(self.points_P)
        if (convex == []):
            return
        self.drawPolygon(np.array(convex))

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
        #plt.plot(Pol[:,0], Pol[:,1], 'bo-')

        x = Pol[:,0]#[k[0] for k in Pol]
        y = Pol[:,1]#[k[1] for k in Pol]
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

if __name__ == '__main__':
    """
    Si iniciamos la aplicación de manera directa, inicilizamos la ventana
    gráfica para ser interactiva
    """
    window = Graphics()
    window.init_interaction()
    window.show()

                
