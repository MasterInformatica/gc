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
import numpy as np
import bintrees
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
from matplotlib.path import Path
from matplotlib.widgets import Slider, Button
import matplotlib.patches as patches

class Point:
    def __init__(self,A):
        self.point = A
        self.isL = None
        self.other = None
        self.numLine = -1

    def setOther(self,B):
        self.other = B
        self.isL = (self.point<self.other.point)
        self.other.isL = not self.isL
        self.other.other = self

    def setNum(self,num):
        self.numLine = num
        self.other.numLine = num

    def line(self):
        return self.numLine
    def otherPoint(self):
        return self.other.point

def doIntersect(L1,L2):
    '''
    p -------> q = p + r
    a -------> b = a + s
    
    '''

    p = L1[0].point
    q = L1[1].point
    a = L2[0].point
    b = L2[1].point

    rx = q[0]-p[0]
    ry = q[1]-p[1]
    sx = b[0]-a[0]
    sy = b[1]-a[1]
    a_px = a[0]-p[0]
    a_py = a[1]-p[1]
    
    rxs   = rx*sy-ry*sx
    a_pxs = a_px*sy-a_py*sx
    a_pxr = a_px*ry-a_py*rx

    if rxs == 0 and a_pxr == 0:
        print "colinear"
        return None
    elif rxs == 0:
        print "paralelas"
        return None
    else:
        t = a_pxs / rxs
        u = a_pxr / rxs
        print "uyyy", t,u
        if (t <= 1 and t >= -1 and u <= 1 and u >= -1):
            return (p[0]+t*rx,p[1]+t*ry)
    return None

def intersection(lines,Points):
#    Points = sort(P)
    intersec = []
    T = bintrees.AVLTree()
    # add to prevent prev and succ item ever exists
    T.insert((None,None),-1)
    T.insert(('Z','Z'),-1)
    for i in range(len(lines)):
        print "line: ",i, "-> (", lines[i][0].point,", ", lines[i][1].point, ")"

    for i in range(0,len(Points)):
        print T
        print "vuelta",i, " ", Points[i].point, Points[i].isL
        lineNum = Points[i].line()
        key = (Points[i].point[1],lineNum) #coordenada y del punto actual

        if (Points[i].isL):
            T.insert(key,lineNum)

            prev = T.prev_item(key)
            if not ( prev[1] < 0):
                corte = doIntersect(lines[lineNum], lines[prev[1]])
                if not (corte is None):
                    intersec = intersec+[corte]
            succ = T.succ_item(key)
            if not (succ[1] < 0):
                corte = doIntersect(lines[lineNum], lines[succ[1]])
                if not (corte is None):
                    intersec = intersec+[corte]

        else:
            key = (Points[i].other.point[1],lineNum)
            succ = T.succ_item(key)
            prev = T.prev_item(key)
            if (prev[1] < 0):
                prev = T.prev_item(('Z','Z'))
            if( succ[0] <0):
                succ = T.succ_item((None,None))
            if not (prev[1] < 0 or succ[0] <0):
                corte = doIntersect(lines[prev[1]], lines[succ[1]])
                if not (corte is None):
                    intersec = intersec+[corte]

            T.remove(key)
    print T
    return intersec

def sort(P):
    return quicksort(P,0,len(P)-1)

def quicksort(L, first, last):
    i = first
    j = last    
    # calcular el pivote para cada coordenada
    pivX = (L[i].point[0] + L[j].point[0]) / 2
    pivY = (L[i].point[1] + L[j].point[1]) / 2

    while i < j: #mientras tengamos elementos

        # hasta que dejen de estar desordenados
        while L[i].point[0] < pivX or (L[i].point[0] == pivX  and L[i].point[1]<pivY):
            i+=1
        while L[j].point[0] > pivX  or (L[j].point[0] == pivX  and L[j].point[1]>pivY):
            j-=1
        
        # si no se han cruzado los indices hay que hacer swap
        if i <= j:
            x = L[j]
            L[j] = L[i]
            L[i] = x
            i+=1
            j-=1

    # recursion
    if first < j:
        L = quicksort(L, first, j)
    if last > i:
        L = quicksort(L, i, last)

    return L


def makeSegments(points):
    ps = []
    segm = []
    for i in range(0,len(points),2):
        P = Point(points[i])
        Q = Point(points[i+1])
        P.setOther(Q)
        P.setNum(i//2)
        #Q.setOther(P)
        #Q.setNum(i//2)
        ps = ps + [P] + [Q]
        segm = segm + [(P,Q)]
    return segm,ps






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
        self.pair = True

    def init_interaction(self):
        """
        Se encarga de inicializar la ventana gráfica para ser interactiva. Añade los sliders y botones.
        """
       
        plt.subplots_adjust(bottom=0.25) # Ajustamos la gráfica para poner los controles debajo, texto encima
        self.fig.suptitle('Click introduce los puntos y puede moverlos.')

        #Buttons
        calculateAxes = plt.axes([0.7, 0.17, 0.15, 0.03])
        #changeMethod = plt.axes([0.7, 0.11, 0.15, 0.03])
        resetAxes = plt.axes([0.7, 0.05, 0.15, 0.03])

        self.buttonCalculate = Button(calculateAxes, 'Calculate!')
        #self.buttonMethod = Button(changeMethod, 'Change Method!')
        self.buttonReset = Button(resetAxes, 'Reset!')

        self.buttonCalculate.on_clicked(self._updatePlot)
        self.buttonReset.on_clicked(self._clean)
        #self.buttonMethod.on_clicked(self._changeMethod)

        

        #self.points_P = [[-3, 3], [8, 2], [-4, 8], [0, 8], [-1, 0]]
        #self.points_P = [[1,2],[3,3],[5,6],[0,10],[3,5],[6,5],[0,9]]
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

        if(self.pair and len(self.points_P)>0):
            ls,ps = makeSegments(self.points_P)
            Ps = sort(ps)
            cortes = intersection(ls,Ps)

#            for p in self.pointList_P:
 #               ax.add_patch(Circle((p[0],p[1]), 0.35,color='b'))
                
            for i in range(0,len(self.points_P),2):
                x = [self.points_P[i][0]]+[self.points_P[i+1][0]]
                y = [self.points_P[i][1]]+[self.points_P[i+1][1]]
                self.ax.plot(x,y,'b')
            for p in cortes:
                self.ax.add_patch(Circle((p[0],p[1]), 0.15,color='r'))



 
        
    def _changeMethod(self,event):
        self.methods = self.methods[1:]+[self.methods[0]]
        print "Metodo: ",self.methods[0]
        self._updatePlot(None)

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
            self.pair = not self.pair
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
        if self.pair:
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
    List_P = [[0,0],[0.1,10],[-1,1],[1,1],[-1,3],[2,3]]
    lines,points = makeSegments(List_P)
    P = sort(points)
    for p in P:
        print p.isL
        print p.point
        print p.line()
    cort = intersection(lines,P)
    print "Cortes: "
    for c in cort:
        print c

    fig = plt.figure()
    ax = fig.add_subplot(111, aspect=1)
    ax.autoscale(False)
    ax.set_xlim(-5,5)
    ax.set_ylim(-5,15)
    
    for p in List_P:
        ax.add_patch(Circle((p[0],p[1]), 0.35,color='b'))
    
    for i in range(0,len(List_P),2):
        x = [List_P[i][0]]+[List_P[i+1][0]]
        y = [List_P[i][1]]+[List_P[i+1][1]]
        ax.plot(x,y)
    for p in cort:
        ax.add_patch(Circle((p[0],p[1]), 0.15,color='r'))
    plt.show()

    
    

if __name__ == '__main__':
    men()
