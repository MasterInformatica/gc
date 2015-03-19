import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
import numpy as np

from casteljau import CurvaDeBezier as cb


class DrawPoints:
    def __init__(self, fig, ax): #, geodesica):
        self.fig = fig
        self.ax = ax
        self.exists_touched_circle = False
        self.points = []
        self.poly = None    
        self.last_curve = None
        self.touched_index = None
        self.touched_x0, self.touched_y0 = None,None
        self.cid_press = fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_move = fig.canvas.mpl_connect('motion_notify_event', self.on_move)
        self.cid_release_button = fig.canvas.mpl_connect('button_release_event', self.on_release)
        #####################
        # Poner a False este valor si queremos computar por Casteljau
        self.compute_bernstein = True 
        #####################

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
        self.curve=cb(self.poly, self.compute_bernstein, None)   
        # Comprobamos que no haya un solo punto. En caso de haberlo, solo se
        # pinta ese punto.
        if self.poly.shape[0] > 1:
            self.curve.plot_bezier()
            if self.last_curve != None:
                self.last_curve.set_data(self.curve.update_bezier())
            else:
                self.last_curve = self.ax.add_line(self.curve.plot_bezier())   
            self.fig.canvas.draw()  

         
        
    def on_move(self, event):
        if event.xdata == None or event.ydata == None: #press out of plot
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
            
            self.curve=cb(self.poly, self.compute_bernstein, None) # Recalculamos la curva
            self.last_curve.set_data(self.curve.update_bezier()) # Actualizamos los valores

            # Actualizamos el dibujo con la nueva curva
            self.fig.canvas.draw()
            
    def on_release(self, event):
        # Reseteamos la variable al soltar el boton del raton
        self.exists_touched_circle = False
        return

if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect=1) # aspect=1 no cambia las proporciones
    ax.set_xlim(-20,20) # Limites de los ejes
    ax.set_ylim(-20,20)
    draw_points = DrawPoints(fig, ax)
    plt.show()
  
