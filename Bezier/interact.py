import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
import numpy as np

from bezier import CurvaDeBezier as cb

# from geodesicas import Geodesica

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


    def on_press(self, event):
        if event.xdata == None or event.ydata == None: #press out of plot
            return
        for circle in self.ax.patches:
            contains, attr = circle.contains(event)
            if contains:
                self.touched_circle = circle
                self.exists_touched_circle = True
                self.pressed_event = event
                self.touched_x0, self.touched_y0 = circle.center
                punto = [self.touched_x0, self.touched_y0]
                self.touched_index = self.points.index(punto)
                return
        self.points.append([event.xdata, event.ydata])       
        self.poly = np.array(self.points)
        print self.poly
        c = Circle((event.xdata, event.ydata), 0.5)
        self.ax.add_patch(c)
        self.fig.canvas.draw() 
         
        self.curve=cb(self.poly)   
        self.curve.plot_bezier()
        if self.last_curve != None:
            self.last_curve.set_data(self.curve.update_bezier())
        else:
            self.last_curve = self.ax.add_line(self.curve.plot_bezier())   
        self.fig.canvas.draw()  
        

         
        
    def on_move(self, event):
        if event.xdata == None or event.ydata == None: #press out of plot
            return
        if self.exists_touched_circle:
            dx = event.xdata - self.pressed_event.xdata
            dy = event.ydata - self.pressed_event.ydata
            x0, y0 = self.touched_circle.center
            self.touched_circle.center = self.touched_x0+dx, self.touched_y0+dy
            # Calculos
            self.points[self.touched_index] = [self.touched_x0+dx, self.touched_y0+dy]
            self.poly = np.array(self.points)
            print self.poly
            self.curve=cb(self.poly) 
            self.last_curve.set_data(self.curve.update_bezier())
            # Deberia actualizar la curva
            self.fig.canvas.draw()
            
    def on_release(self, event):
        self.exists_touched_circle = False
        return

if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect=1) # aspect=1 no cambia las proporciones
    ax.set_xlim(-20,20) #Limites de los ejes
    ax.set_ylim(-20,20)
    # geodesica = Geodesica()
    draw_points = DrawPoints(fig, ax)
    plt.show()
#
