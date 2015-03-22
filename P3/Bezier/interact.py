import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
import numpy as np

from curvasBezier import CurvaDeBezier as Bezier


class DrawPoints:
    def __init__(self, fig, ax, bernstein):
        self.fig = fig
        self.ax = ax
        # Variables de la curva
        self.points = []
        self.poly = None # numpy array con los puntos
        self.curve_ploted = None # Guarda la curva pintada
        self.compute_bernstein = bernstein # Bernstein o De Casteljau
        # Variables para Mover puntos
        self.exists_touched_circle = False
        self.touched_index = None
        self.touched_x0, self.touched_y0 = None,None
        # Controlador de Eventos
        self.cid_press = fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_move = fig.canvas.mpl_connect('motion_notify_event', self.on_move)
        self.cid_release_button = fig.canvas.mpl_connect('button_release_event', self.on_release)




    def on_press(self, event):
        if event.xdata == None or event.ydata == None: #press out of plot
            return
        for circle in self.ax.patches:
            contains, attr = circle.contains(event)
            # Si estamos pinchando en un punto que ya existia, ponemos la variable
            # exists_touched_circle a True. Esto nos servira en la funcion on_move.
            if contains:
                self.touched_circle = circle
                self.exists_touched_circle = True
                self.pressed_event = event
                self.touched_x0, self.touched_y0 = circle.center
                punto = [self.touched_x0, self.touched_y0]
                self.touched_index = self.points.index(punto)
                return
            
        # Anyadimos el nuevo punto que hemos pintado y lo dibujamos
        self.points.append([event.xdata, event.ydata])       
        self.poly = np.array(self.points)
        c = Circle((event.xdata, event.ydata), 0.5)
        self.ax.add_patch(c)
        self.fig.canvas.draw() 
         
        # Calculamos nuestra curva en funcion del poligono que hemos pintado
        if self.curve_ploted != None:
            self.curve.set_polygon(self.poly)
            self.curve_ploted.set_data(self.curve.update_bezier())
        else: # primera vez
            self.curve=Bezier(self.poly, self.compute_bernstein)
            self.curve_ploted = self.ax.add_line(self.curve.plot_bezier())   
        self.fig.canvas.draw()  

         
        
    def on_move(self, event):
        if event.xdata == None or event.ydata == None: #move out of plot
            return
        # Si habiamos pinchado encima de un circulo existente y lo intentamos
        # mover, se actualiza el poligono en consecuencia, se modifican los
        # valores, se calcula la nueva curva de Bezier y se pinta de nuevo
        if self.exists_touched_circle:
            dx = event.xdata - self.pressed_event.xdata
            dy = event.ydata - self.pressed_event.ydata
            x0, y0 = self.touched_circle.center
            self.touched_circle.center = self.touched_x0+dx, self.touched_y0+dy
           
            # Calculos
            self.points[self.touched_index] = [self.touched_x0+dx, self.touched_y0+dy]
            self.poly = np.array(self.points)
            
            self.curve.set_polygon(self.poly) # Cambiamos el poligono
            self.curve_ploted.set_data(self.curve.update_bezier()) # Actualizamos los valores

            # Actualizamos el dibujo con la nueva curva
            self.fig.canvas.draw()
            
    def on_release(self, event):
        # Reseteamos la variable al soltar el boton del raton
        self.exists_touched_circle = False
        return


if __name__ == '__main__':
    ######################################
    # Si True => Bernstein.              #
    #    False => De Casteljau           #
    ######################################
    calcular_bernstein = True
    if calcular_bernstein:
        print "Calculando con Berstein..."
    else:
        print "Calculando con Casteljau..."
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect=1) # aspect=1 no cambia las proporciones
    ax.set_xlim(-20,20) # Limites de los ejes
    ax.set_ylim(-20,20)
    draw_points = DrawPoints(fig, ax, calcular_bernstein)
    plt.show()
  
