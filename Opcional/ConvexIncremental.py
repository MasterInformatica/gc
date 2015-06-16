# -*- coding: utf-8 -*-

""" 
Práctica Opcional de Geometría Computacional
ConvexHull Incremental algorithm with cost nlogn
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

def locate(point, H1, H2):
    ''' 
    determine the position of point respect the convex
    and return the case and the segment
    '''
    caso = "NULL"

    maxK = H1.max_key()
    minK = H1.min_key()
    if point > maxK:
        #D: point is OUT and right the convex hull
        insertR(point, H1, +1, maxK, minK)
        insertR(point, H2, -1, maxK, minK)
    elif point < minK:
        #D: point is OUT and left the convex hull
        insertL(point, H1, +1, maxK, minK)
        insertL(point, H2, -1, maxK, minK)
    else:
        a = H1.floor_key(point)
        b = H1.ceiling_key(point)
        if side(a,b,point) > 0:
            # B: point is OUT and above the convexhull
            insert(point, H1, +1, maxK, minK)
        else:
            a = H2.floor_key(point)
            b = H2.ceiling_key(point)
            if side(a,b,point) < 0:
                # C: point is OUT and below the convexhull
                insert(point, H2, -1, maxK, minK)
            #else:
                # A: point is IN or ON the convexhull
                # nothing to do

def insertR(point,H,orientation,maxK,minK):
    u = H.prev_key(maxK) # left neig maxK
    while(u > minK and side(u,maxK,point)*orientation > 0): 
        # point is at left of edge u->maxK
        H.remove(maxK) # remove u
        maxK = u
        u = H.prev_key(maxK) # new left neighbor of maxK
    if side(u,maxK,point)*orientation > 0:
        H.remove(maxK)

    H.insert(point,0)
    #return H

def insertL(point,H,orientation,maxK,minK):
     y = H.succ_key(minK) # right neighbor of minK
     while(y < maxK and side(minK,y,point)*orientation > 0):
         # point is at left of edge minK->y
         H.remove(minK) # remove 
         minK = y
         y = H.succ_key(minK) # new right neighbor of minK
     if side(minK,y,point)*orientation > 0:
         H.remove(minK)
     H.insert(point,0)
     #return H


def insert(point,H,orientation,maxK,minK):
    '''
    insert point in H.
    orientation is -1 or +1, depends on H being the upper tree or the other respectively
    '''
    #get the edge E or vertex V whose horizontal span includes point 
    v = H.floor_key(point) # left point of edge E or vertex V
    w = H.ceiling_key(point)  # right point of edge E or vertex V
    if not (v == minK):
        u = H.prev_key(v) # left neig v
        while(u > minK and side(u,v,point)*orientation > 0): 
            # point is at left of edge u->v    
            H.remove(v) # remove v
            v = u
            u = H.prev_key(v) # new left neighbor of v
        if u == minK and side(u,v,point)*orientation > 0:
            H.remove(v)
            maxK = H.max_key()
    if not (w == maxK):
        y = H.succ_key(w) # right neighbor of w
        while(y < maxK and side(w,y,point)*orientation > 0):
            # point is at left of edge w->y
            H.remove(w) # remove w
            w = y
            y = H.succ_key(w) # new right neighbor of w
        if y==maxK and side(w,y,point)*orientation > 0:
            H.remove(w)
    H.insert(point,0)
    #return H

def addpoint(point, H1, H2):
    ''' 
    Algorimo incremental de coste O(n*log(n))
    '''
    if len(H1) < 2:
        H1.insert(point,0)
        H2.insert(point,0)
        return #H1,H2
    
    locate(point,H1,H2)

    return #H1, H2




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

        self.drawPoint(self.newpoint ,'g')

        addpoint(self.newpoint,self.H1,self.H2)
        
        print "->",self.H1
        print self.H2
        print "-------------------------------"

        self.drawPolygon(self.H1,'-ob')
        self.drawPolygon(self.H2,'-ob')

        
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
        self.H1 = bintrees.AVLTree()
        self.H2 = bintrees.AVLTree()
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
        self._updatePlot()
        self.fig.canvas.draw()


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
def men():
    points = [(0,0),(1,2),(2,2),(3,0),(1,3)]
    #points = [(0,0),(2,0),(1,1)]
    H1 = bintrees.AVLTree()
    H2 = bintrees.AVLTree()
    for p in points:
        addpoint(p,H1,H2)
        print "->",H1
        print H2
        print "-------------------------------"
def menu():
    window = Graphics()
    window.init_interaction()
    window.show()

if __name__== "__main__":
    menu()
