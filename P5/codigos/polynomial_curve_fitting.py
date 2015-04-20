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


def polynomial_curve_fitting(points, knots, method, L=0, libraries=False,
                             num_points=100, degree=None):    
    '''
       Fits planar curve to points at given knots. 

       Arguments:
           points -- coordinates of points to adjust (x_i, y_i) given by a numpy array of shape (N, 2)
           knots -- strictly increasing sequence at which the curve will fit the points, tau_i
               It is given by a np.array of shape M, unless knots='chebyshev', in this case
                   N Chebyshev's nodes between 0 and 1 will be used instead of tau.
           method -- one of the following: 
               'newton' computes the interpolating polynomial curve using Newton's method.
                   returns error if N!=M. 
               'least_squares' computes the best adjusting curve in the least square sense,
                   i.e., min_a ||Ca - b||**2 + L/2 ||a||**2
           L -- regularization parameter
           libraries -- If False, only numpy linear algebra operations are allowed. 
               If True, any module can be used. In this case, a very short and fast code is expected
           num_points -- number of points to plot between tau[0] and tau[-1]
           degree -- degree of the polynomial. Needed only if method='least_squares'.
                     If degree=None, the function will return the interpolating polynomial.

       Returns:
           numpy array of shape (num_points, 2) given by the evaluation of the polynomial
           at the evenly spaced num_points between tau[0] and tau[-1]
    '''
    if knots == 'chebyshev':
        knots = chebyshev_knots(0,1,points.shape[0])
    
    sol = np.zeros((num_points,2))
    sol[:,0]=polynomial_curve_fitting1d(points[:,0], knots, method, L, libraries, num_points)
    sol[:,1]=polynomial_curve_fitting1d(points[:,1], knots, method, L, libraries, num_points)
    return sol

def polynomial_curve_fitting1d(points, knots, method, L=0, libraries=False,
                             num_points=100):
    degree = knots.shape[0] # hay que cambiarlo
    if method == 'newton':
        if points.shape[0] != degree:
            raise Exception("M!=N") 
        return newton_polynomial(points,knots,num_points,libraries)
    else:
        return least_squares_fitting(points,knots,degree,num_points,L,libraries)
    pass


def newton_polynomial(x, tau, num_points=100, libraries=False):    
    '''
    Computes de Newton's polynomial interpolating values x at knots tau
    x: numpy array of size n; points to interpolate
    tau: numpy array of size n; knots tau[0] < tau[1] < ... < tau[n-1]
    num_points: number of points at which the polynomial will be
                evaluated

    libraries: False means only linear algebra can be used
               True means every module can be used.

    returns:
       numpy array of size num_points given by the polynomial 
       evaluated at np.linspace(tau[0], tau[1], num_points)

    Maximum cost allowed: 5,43 s at lab III computers
            degree = n - 1 = 9
            num_points = 100
    '''
    
    if libraries:
        return interp_with_library(x,tau,num_points) #np.array of size num_points
    else:
        interpolant = newtondd(tau,x)
        t = np.linspace(tau[0],tau[-1], num_points)
        y = eval_poly(t,interpolant, tau)
        return y #np.array of size num_points
    

def interp_with_library(x, tau, num_points):
    '''
    Interpola resolviendo el sistema con la matriz de Vandermonde
    '''
    coeffs = np.linalg.solve(np.vander(tau, increasing=True), x)
    times = np.linspace(tau[0], tau[-1], num_points)
    return np.polyval(np.flipud(coeffs),times)

def newtondd(x,y):
	n = len(x)
	v = np.zeros((n,n))
        v[:,0] = y		# Fill in y column of Newton triangle
	for i in range(1,n):		# For column i,
		for j in range(n-i):	# 1:n+1-i		# fill in column from top to bottom
#			print j,i," ",j+1,i-1," ", j,i-1," ",j+i," ",j
			v[j,i] = (v[j+1,i-1]-v[j,i-1])/(x[j+i]-x[j])
	c = v[0,:].copy()			# Read along top of triangle for output coefficients
	return c



def eval_poly(t, coefs, tau=None):    
    N = coefs.shape[0]-1; # ultimo indice accesible
    if tau is None:
        tau = np.zeros(N)
    sol = coefs[N] * np.ones(t.shape[0])
    for k in range(N-1, -1, -1):
        sol = coefs[k]  + (t-tau[k])*sol

    return sol

        
def least_squares_fitting(points, knots, degree, num_points, L=0, libraries=True):    
    #I've used np.linalg.lstsq and np.polyval if libraries==True
    if libraries:
        C = np.vander(knots,N=degree, increasing=True)
        F = np.dot(C.transpose(),C)+L/2.0*np.eye(degree)
        coeffs = np.linalg.lstsq(F, np.dot(C.transpose(),points))[0]
        #coeffs = np.linalg.lstsq(np.vander(knots, increasing=True), points)[0]
        times = np.linspace(knots[0], knots[-1], num_points)
        return np.polyval(np.flipud(coeffs),times)
    else:
        C = np.vander(knots,N=degree, increasing=True)
        F = np.dot(C.transpose(),C)+L/2.0*np.eye(degree)
        coeffs = np.linalg.solve(F, np.dot(C.transpose(),points))
        times = np.linspace(knots[0], knots[-1], num_points)
        return  eval_poly(times,coeffs)
        
def chebyshev_knots(a, b, n):
    j = np.arange(1,n+1) # j = 1, ..., n    
    return (a+b-((a-b)*np.cos(((2*j-1)*np.pi)/(2.0*n))))/2.0

def calcuteVander(knots,N):
    pass

                                 
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
        self.fig.suptitle('Click izquierdo introduce una curva, click derecho la otra.\n Los vertices de los poligonos se pueden mover con ambos clicks.')

        # Sliders
#        epsAxes = plt.axes([0.20, 0.15, 0.4, 0.03])        
#        kAxes = plt.axes([0.20, 0.1, 0.4, 0.03])

#        self.epsSlider = Slider(epsAxes, 'eps: ', 0.001, 1.00, valinit=0.1, valfmt=u'%1.3f')
#        self.kSlider   = Slider(kAxes, 'k: ', 0, 6, valinit=3, valfmt=u'%0.0f')

#        self.epsSlider.on_changed(self._updateEps)        
#        self.kSlider.on_changed(self._updateK)

        #Buttons
        calculateAxes = plt.axes([0.7, 0.17, 0.15, 0.03])
        randomAxes = plt.axes([0.7, 0.11, 0.15, 0.03])
        resetAxes = plt.axes([0.7, 0.05, 0.15, 0.03])
        method = plt.axes([0.3, 0.17, 0.15, 0.03])
        libs = plt.axes([0.3, 0.11, 0.15, 0.03])
        subL = plt.axes([0.3, 0.05, 0.07, 0.03])
        addL = plt.axes([0.38, 0.05, 0.07, 0.03])

        self.buttonCalculate = Button(calculateAxes, 'Calculate!')
        self.buttonReset = Button(resetAxes, 'Reset!')
        self.buttonRandom = Button(randomAxes, 'Random!')
        self.buttonMethod = Button(method, 'Change Method')
        self.buttonLibs = Button(libs, 'Change Libs')
        self.buttonAddL = Button(addL, 'L+=1')
        self.buttonSubL = Button(subL, 'L-=1')

        self.buttonCalculate.on_clicked(self._updatePlot)
        self.buttonReset.on_clicked(self._clean)
        self.buttonRandom.on_clicked(self._randomPlot)
        self.buttonMethod.on_clicked(self._changeMethod)
        self.buttonLibs.on_clicked(self._changeLibs)
        self.buttonAddL.on_clicked(self._changeAddL)
        self.buttonSubL.on_clicked(self._changeSubL)

    def _changeMethod(self,event):
        aux = self.method
        self.method = self.other_method
        self.other_method = aux
        self._updatePlot(event)
        self.fig.canvas.draw()
    def _changeLibs(self,event):
        self.lib = not self.lib
        self._updatePlot(event)
        self.fig.canvas.draw()
    def _changeAddL(self,event): 
        if(self.L ==10):
            return       
        self.L += 1
        self._updatePlot(event)
        self.fig.canvas.draw()
    def _changeSubL(self,event):        
        if(self.L ==0):
            return
        self.L -= 1
        self._updatePlot(event)
        self.fig.canvas.draw()
    def _updatePlot(self, event):
        """
        Encarga de actualizar los dibujos, llamando a los métodos correspondientes
        """
        
        P = np.array(self.points_P)
        if P.shape[0] < 1:# no hay puntos suficientes
            return
        self.ax.lines = []
 

        #Imprimimos los polígonos de control
        #self.drawPolygon(self.points_P, 'mediumblue')

        for c in self.inter_circle: #reset intersection Points
            c.remove()
        self.inter_circle = []
        # COMPUTAR
        knots = np.linspace(0, 1, P.shape[0])
        colores = ['b','g','r','c','m','y','k','burlywood','orange','chartreuse','mediumgreen','salmon']
        print "Using: method=%s, num_L=%d, libreries=%s" % (self.method, self.L, self.lib)
        if self.method == 'newton':
            curve = polynomial_curve_fitting(P, knots, self.method, 0, self.lib,200)
            self.drawPolygon(curve,colores[0])
        else:
            list_L = [10**k for k in range(-5-self.L, -5)]
            col = 0
            for L in list_L:
                curve = polynomial_curve_fitting(P, knots, self.method, L, self.lib,200)
                self.drawPolygon(curve,colores[col])
                col+=1

        
    def _randomPlot(self, event):
        """
        Genera puntos aleatorios y los dibuja.
        """

        self._clean(event)
        P = np.random.uniform(-20, 20, (5 + 1, 2))

        # Para poder mover los puntos
        for p in P:
            self.points_P.append([p[0],p[1]])       
            c = Circle((p[0],p[1]), 0.5,color='b')
            self.ax.add_patch(c)
        self._updatePlot(event)
        self.fig.canvas.draw()
        

    def drawLine(self,line):
        """ 
        Dada una linea por parámetro, la muestra en la figura
        """
        self.ax.add_line(line)
        self.fig.canvas.draw()


    def drawPolygon(self, Pol,colour=None):
        """ 
        Pinta los poligonos de control self.points_P y self.points_Q con los colores b y r
        """
        x = [k[0] for k in Pol]
        y = [k[1] for k in Pol]
        if colour is None:
            self.ax.plot(x,y)
        else:
            self.ax.plot(x,y,colour)
        self.fig.canvas.draw()
        
    def drawPoints(self,points,colour):
        """
        Dado un punto y un color, muestra este con ese color en la figura, y su poligono de control
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
        for c in self.inter_circle: #reset intersection Points
            c.remove()
        self.inter_circle = []
        self.ax.cla()
        self.ax.autoscale(False)
        self.ax.set_xlim(-20,20)
        self.ax.set_ylim(-20,20)
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

                
