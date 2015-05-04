# -*- coding: utf-8 -*-

""" 
Práctica 5 de Geometría Computacional
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




def spline2d(a, b, xi, k, nu, A, num_dots):
    '''Computes a plane spline curve of order k
       defined on the interval [a, b] with knots psi,
       multiplicities nu and coefficiets A.
       Parameters:
       a, b -- ends of the interval, real numbers
       xi -- list of breakpoints, a < xi[0] < .. < xi[-1] < b
       k -- order of the curve, the degree is <= k - 1
       nu -- list of integer multiplicities of each breakpoint,
             len(psi) = len(nu), 1 <= nu[i] < k
       A -- list of coefficients of the B-spline basis,
            A = [[x0, y0], [x1, y1],..., [x[N], y[N]]
       num_dots -- number of dots of the spline to be plotted,
                   uniformly spaced alogn the interval [a, b]
       Returns:
       the spline curve as a numpy array of size (2, num_dots) <'''
    A = np.array(A)
    xi = np.array(xi)
    nu = np.array(nu)

    var = Vars_spline(a, b, xi, k, nu, A, num_dots)
    n_ts = k*(1+nu.shape[0]+1)-np.sum(nu)
    s = np.zeros((2,num_dots))
    tau = var.get_tau()
    t = var.get_t()
    index = 0

    for i_tau in range(num_dots):
        # Paso 1: Avanzar el indice hasta que se pueda operar
        while (index < n_ts-2 and t[index+1] <= tau[i_tau]):
            index += 1
        
        # Paso 2: Sumamos a(k-1,index,tau)
        if (t[index] <= tau[i_tau] and tau[i_tau] <= t[index+1]):
            s[:,i_tau] =  (var._calc_a(k-1,index))[:,i_tau]

    return s
    

class Vars_spline:
    def __init__(self, a, b, xi, k, nu, A, num_dots):
        self.tau = np.linspace(a, b, num_dots)
        self.w = {}
        self.t_i = np.zeros( k*(1+nu.shape[0]+1)-sum(nu)+1)
        self.a = {}  #np.empty((A.shape[0],A.shape[0]))
        self.k = k
        #calc variables
        self._calc_t(a,b,xi,k,nu)
        self.A = A
        self.num_dots = num_dots
#        for i in range(A.shape[0]):
#            self.a[(0,i)] = np.full(num_dots,A[i])

    def get_tau(self):
        return self.tau

    def get_t(self):
        return self.t_i

    def _calc_w(self,i,k):
        if( (i,k) in self.w):
            return self.w[(i,k)]
        if (i>=self.t_i.shape[0] or i+k-1>= self.t_i.shape[0] or self.t_i[i] == self.t_i[i+k-1]):
            self.w[(i,k)] = np.zeros(self.tau.shape[0])
        else:
            self.w[(i,k)] = ((self.tau - self.t_i[i])*1.0/(self.t_i[i+k-1]-self.t_i[i])*1.0)
        return self.w[(i,k)]

    def _calc_a(self,r,i):
        if ((r,i) in self.a):
            return self.a[(r,i)]
        if (r==0):
            self.a[(r,i)]=self.A[i]
            return self.a[(r,i)]
        wi = self._calc_w(i,self.k-r+1)
        ai_1 = self._calc_a(r-1,i-1)
        ai = self._calc_a(r-1,i)
        aux = np.zeros((2,self.num_dots))
        aux[0] = (1-wi)*ai_1[0] + wi*ai[0]
        aux[1] = (1-wi)*ai_1[1] + wi*ai[1]

        self.a[(r,i)] = aux
        return self.a[(r,i)]

   
    # Segun la formula para cada t entre tj y tj+1 
    # usamos una combinacion de puntos aj-k+r+1 hasta aj


    def _calc_t(self,a,b,xi,k,nu):
        l = nu.shape[0]
        index=0
        self.t_i[0:k] = a
        index = k+1
        for i in range(0, l):
            self.t_i[index : index+(k-nu[i])] = xi[i] 
            index += (k-nu[i])
        self.t_i[index: index+k] = b


                                 
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
        self.lib = False
        self.other_method = 'newton'
        self.method = 'least_squares'
        self.L = 6
        plt.subplots_adjust(bottom=0.25) # Ajustamos la gráfica para poner los controles debajo, texto encima
        self.fig.suptitle('Click introduce los puntos.\n La consola muestra informacion sobre la ejecucion actual.')

        #Buttons
        calculateAxes = plt.axes([0.7, 0.17, 0.15, 0.03])
#        randomAxes = plt.axes([0.7, 0.11, 0.15, 0.03])
        resetAxes = plt.axes([0.7, 0.05, 0.15, 0.03])

        self.buttonCalculate = Button(calculateAxes, 'Calculate!')
        self.buttonReset = Button(resetAxes, 'Reset!')
#        self.buttonRandom = Button(randomAxes, 'Random!')

        self.buttonCalculate.on_clicked(self._updatePlot)
        self.buttonReset.on_clicked(self._clean)
        

        self.points_P = [[-3, 3], [8, 2], [-4, 8], [0, 8], [-1, 0]]
        for p in self.points_P:
            c = Circle((p[0], p[1]), 0.5,color='b')
            self.ax.add_patch(c)
        self._updatePlot(None)

    def _updatePlot(self, event):
        """
        Encarga de actualizar los dibujos, llamando a los métodos correspondientes
        """
        
        P = np.array(self.points_P)
        if P.shape[0] < 2:# no hay puntos suficientes
            return
        self.ax.lines = []
 
        for c in self.inter_circle:
            c.remove()
        self.inter_circle = []
        # COMPUTAR
        Poin = self.points_P
        nu = []
        k = len(self.points_P)-1
        for i in range(k):
            Poin = [self.points_P[0]]+Poin +[self.points_P[-1]]
            nu += [k-1]
        xi = np.linspace(0,4,k+2)
 
        #curve = spline2d(0, 4,xi , P.shape[0], nu, Poin, 100)
        curve = spline2d(0, 4, xi[1:-1].tolist(),k , nu, Poin, 200)
        self.drawPolygon(curve,"-r")
        X = [[],[]]
        X[0] = [k[0] for k in Poin]
        X[1] = [k[1] for k in Poin]
        self.drawPolygon(X,"-b")
        

    def drawLine(self,line):
        """ 
        Dada una 2Dline por parámetro, la muestra en la figura
        """
        self.ax.add_line(line)
        self.fig.canvas.draw()


    def drawPolygon(self, Pol,colour=None):
        """ 
        Pinta los poligonos definido en Pol
        """
        x = Pol[0]#[k[0] for k in Pol]
        y = Pol[1]#[k[1] for k in Pol]
        if colour is None:
            self.ax.plot(x,y)
        else:
            self.ax.plot(x,y,colour)
        self.fig.canvas.draw()
        
    def drawPoints(self,points,colour):
        """
        Dado un punto y un color, muestra este con ese color en la figura
        """
        if points.shape[0] != 0:
            for p in points:
                c = Circle((p[0],p[1]),0.3,color='g')
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
        self.points_P = [[-3, 3], [8, 2], [-4, 8], [0, 8], [-1, 0]]
        for p in self.points_P:
            c = Circle((p[0], p[1]), 0.5,color='b')
            self.ax.add_patch(c)
        self._updatePlot(None)
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

                
