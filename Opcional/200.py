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
from functools import total_ordering

SWEEP = -9999 

@total_ordering
class Point:
    def __init__(self,A):
        self.point = A
        self.isL = None
        self.other = None
        self.numLine = -1
        self.corte = False
        self.nL1 = -1
        self.nL2 = -1
        self.pos = -1
    def __getitem__(self,i):
        return self.point[i]
    def setOther(self,B):
        self.other = B
        self.isL = (self.point<self.other.point)
        self.other.isL = not self.isL
        self.other.other = self
    def setPos(self,pos):
        self.pos = pos
    def setNum(self,num):
        self.numLine = num
        self.other.numLine = num
    def setCorte(self,numL1,numL2):
        self.corte = True
        self.nL1 = numL1
        self.nL2 = numL2
    def line(self):
        return self.numLine
    def otherPoint(self):
        return self.other.point
    def __repr__(self):
        return 'Point(%s, %s)'%(self.point[0], self.point[1])
    def __eq__(self, other):
        EPS = 0.00001
        return ((abs(self.point[0]-other.point[0]) < EPS and
                 abs(self.point[1]-other.point[1])) < EPS)
    def __lt__(self, other):
        if self.point[0] < other.point[0]: 
            return True
        elif self.point[0] == other.point[0]:
            return self.point[1] < other.point[1]
        else:
            return False

def doIntersect(L1,L2):
    '''
    p -------> q = p + r
    a -------> b = a + s  
    '''
    p = L1.A
    q = L1.B
    a = L2.A
    b = L2.B

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
        return None
    elif rxs == 0:
        return None
    else:
        t = a_pxs / rxs
        u = a_pxr / rxs
        if (t <= 1 and t >= 0 and u <= 1 and u >= 0):
            return Point((p[0]+t*rx,p[1]+t*ry))
    return None

def notEmpty(T):
    return len(T)<>0
def insertNoRep(List,E):
    insert = True
    for l in List:
        if abs(l[0]*l[0]+l[1]*l[1] - E[0]*E[0]+E[1]*E[1])< 0.000000001:
            insert = False
            break
    if insert:
        return List+[E]
    else:
        return List

def insertNoRepP(List,E):
    print "--------------------------------------------------"
    print "Cola de eventos:", List,E
    print "--------------------------------------------------"

    insert = False
    result = []
    idx = 0
    if E < List[0]:
        return List
    for i in List:
        if E == i:
            return List

        if i > E:
            break;
        else:
            idx = idx+1

    result = List[0:idx] + [E] + List[idx:]

    print "--------------------------------------------------"
    print "Cola de eventos:", result
    print "--------------------------------------------------"

    return result



@total_ordering
class Segment:
    def __init__(self,P=None,maxi=False):
        self.A = None
        self.B = None
        self.epsilon = 0
        self.max = maxi
        if P is None:
            self.vacio = True
            return

        self.vacio=False
        A = P[0]
        B = P[1]
        if B < A:
            aux = B
            B = A
            A = aux
        self.A = A
        self.B = B
    def setepsilon(self,eps):
        self.epsilon = eps
    def __repr__(self):
        return "Seg(%s,%s,%s)"%(self.A,self.B,self.max)

    def _cmp(self,oth):
        global SWEEP
        if ((self is None) and (oth is None)):
            return 0
        if (self is None):
            return -1 
        if (oth is None):
            return 1

        if self.vacio and oth.vacio:
            if self.max == oth.max:
                return 0
            if self.max:
                return 1
            if oth.max:
                return -1

        if self.vacio:
            if self.max:
                return 1
            return -1
        if oth.vacio:
            if oth.max:
                return -1
            return 1
        
        print "A",self.A,"B",self.B
        print "A",oth.A,"B",oth.B
        if (self.A == oth.A and self.B == oth.B):
            print "no queda otra"
            return 0

        maxY1 = max(self.A[1],self.B[1])
        maxY2 = max(oth.A[1],oth.B[1])
        minY1 = min(self.A[1],self.B[1])
        minY2 = min(oth.A[1],oth.B[1])

        eps = self.epsilon
        
        S1 = Segment([Point([SWEEP+eps,minY1-10]),Point([SWEEP+eps,maxY1+10])])
        S2 = Segment([Point([SWEEP+eps,minY2-10]),Point([SWEEP+eps,maxY2+10])])

        corte1 = doIntersect(S1,self)
        corte2 = doIntersect(S2,oth)

        if (corte1 is None or corte2 is None):
            print "aqui"
            return 0

        if (corte1[1] < corte2[1]):
            return -1
        elif (corte1[1] > corte2[1]):
            return 1
        else:
            print "HOLA"
            return 0

    def __eq__(self,oth):
        r= self._cmp(oth) == 0
        print self,"EQ",oth,"?",r
        return r

    def __lt__(self,oth):
        r= self._cmp(oth) < 0
        print self,"LT",oth,"?",r
        return r
    def __gt__(self,oth):
        r= self._cmp(oth) > 0
        print self,"GT",oth,"?",r
        return r

    def __ne__(self,oth):
        r= self._cmp(oth) <> 0
        print self,"NE",oth,"?",r
        return r

def ppp(v,k):
    print v

def intersection(lines,Points):
    print "-------------------------START-----------------------------"
    global SWEEP
    intersec = []
    T = bintrees.AVLTree()
    # add to prevent prev and succ item ever exists
    Sm = Segment()
    SM = Segment(None,True)
    T.insert(Sm,0)
    T.insert(SM,0)

    k = 0
    while notEmpty(Points):
        print "\n\n\n\n\n\n\n\n"
        P = Points[0]
        SWEEP = P.point[0]
        print "SWW",SWEEP
        print T
        if P.corte: #intersec
            print "corte",P.point
            ## add P a intersec
            intersec = insertNoRep(intersec,P.point)
            L1 = P.nL1
            L2 = P.nL2
            # swap segments

            L1.setepsilon(-0.0001)
            L2.setepsilon(-0.0001)

            T.remove(L2)
            T.remove(L1)


            L1.setepsilon(0.0001)
            L2.setepsilon(0.0001)
            T.insert(L1,0)
            T.insert(L2,0)

            #check_intersect
            prev = T.prev_key(L2)
            if not ( prev.vacio):
                corte = doIntersect(L2, prev)
                if not (corte is None):
                    corte.setCorte(prev,L2)
                    Points = insertNoRepP(Points,corte)
            succ = T.succ_key(L1)
            if not (succ.vacio or succ==L2):
                corte = doIntersect(L1, succ)
                if not (corte is None):
                    corte.setCorte(L1,succ)
                    Points = insertNoRepP(Points,corte)
        elif P.isL: #left
            print "left",P.point

            lineNum = P.line()
            key = lines[lineNum]
            print "Voy a meter la clave: ", key
            T.insert(key,0)
            print "Ya he metido la clave"
            prev = T.prev_key(key)
            if not ( prev.vacio):
                corte = doIntersect(lines[lineNum], prev)
                if not (corte is None):
                    corte.setCorte(prev,key)
                    Points = insertNoRepP(Points,corte)
            succ = T.succ_key(key)
            if not (succ.vacio):
                corte = doIntersect(lines[lineNum], succ)
                if not (corte is None): 
                    corte.setCorte(key,succ)
                    Points = insertNoRepP(Points,corte)
        else: #right
            print "right",P.point
            lineNum = P.line()
            key = lines[lineNum]
            key.setepsilon(0)
            prev = T.prev_key(key)
            succ = T.succ_key(key)
            if not (prev.vacio or succ.vacio):
                corte = doIntersect(prev, succ)
                if not (corte is None or corte < P):
                    corte.setCorte(prev,succ)
                    Points = insertNoRepP(Points,corte)
            T.remove(key)           
        Points.pop(0)
        print "Eventos FIN:",Points
        print T
    return intersec


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
        segm = segm + [Segment([P,Q])]
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
#        self.ax.lines = []
        for c in self.inter_circle:
            c.remove()
        self.inter_circle = []
        self.fig.canvas.draw()

        if(self.pair and len(self.points_P)>0):
            ls,ps = makeSegments(self.points_P)
            Ps = sorted(ps)
            cortes = intersection(ls,Ps)

#            for p in self.pointList_P:
 #               ax.add_patch(Circle((p[0],p[1]), 0.35,color='b'))
                
            for i in range(0,len(self.points_P),2):
                x = [self.points_P[i][0]]+[self.points_P[i+1][0]]
                y = [self.points_P[i][1]]+[self.points_P[i+1][1]]
                self.ax.plot(x,y,'b')
            for p in cortes:
                c = Circle((p[0],p[1]), 0.5,color='r')
                self.inter_circle = self.inter_circle + [c]
                self.ax.add_patch(c)

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
        self.pair = True
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
    List_P = [[-1,1],[1,1],[0,0],[2,10],[-1,3],[3,3]]
    lines,points = makeSegments(List_P)
    P = sorted(points)

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
        ax.add_patch(Circle((p[0],p[1]), 0.5,color='b'))
    
    for i in range(0,len(List_P),2):
        x = [List_P[i][0]]+[List_P[i+1][0]]
        y = [List_P[i][1]]+[List_P[i+1][1]]
        ax.plot(x,y)
    for p in cort:
        ax.add_patch(Circle((p[0],p[1]), 0.5,color='r'))
    plt.show()

    
    

if __name__ == '__main__':
    men()

