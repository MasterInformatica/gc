# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon

class CreatePolygon:
    
    def __init__(self):
        self.circle_list = []
        self.x0 = None
        self.y0 = None
        self.fig = plt.figure()
        self.ax = plt.subplot(111)
        self.ax.set_xlim(-20, 20)
        self.ax.set_ylim(-20, 20)
        self.ax.set_title('Bot' + u'Ã³' + 'n izq. para poner puntos y moverlos, derecho para cerrar y terminar')
        self.cidpress = self.fig.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.fig.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmove = self.fig.canvas.mpl_connect(
            'motion_notify_event', self.on_move)
        self.press_event = None
        self.current_circle = None
        self.points = None
        self.poly = None
    
    
    def on_press(self, event):
        if event.button == 3: #Cerrar y desconectar
            self.poly.set_closed(True)
            self.fig.canvas.draw()
            self.fig.canvas.mpl_disconnect(self.cidpress)
            self.fig.canvas.mpl_disconnect(self.cidrelease)
            self.fig.canvas.mpl_disconnect(self.cidmove)
            self.points = [list(circle.center) for circle in self.circle_list]
            return self.points
    
        x0, y0 = int(event.xdata), int(event.ydata)
        #Buscamos el circulo que contiene al evento, si lo hay
        for circle in self.circle_list:
            contains, attr = circle.contains(event)
            if contains:
                self.press_event = event
                self.current_circle = circle
                self.x0, self.y0 = self.current_circle.center
                return
        #Si no hemos encontrado ningun circulo:
        c = Circle((x0,y0), 0.5)
        self.ax.add_patch(c)
        self.circle_list.append(c)
        self.current_circle = None
        num_circles = len(self.circle_list) 
        if num_circles == 1:
            self.fig.canvas.draw()
        else:
            self.points = [list(circle.center) for circle in self.circle_list]
            if self.poly == None:
                self.poly = Polygon(np.array(self.points), fill=False, closed=False)
                self.ax.add_patch(self.poly)
                self.fig.canvas.draw()
            else:
                self.poly.set_xy(np.array(self.points))
                print self.poly.get_xy()
                self.fig.canvas.draw()
                self.fig.canvas.draw()
                
    def on_release(self, event):
        self.press_event = None
        self.current_circle = None
        
    def on_move(self, event):
        if (self.press_event is None or
             event.inaxes != self.press_event.inaxes or
              self.current_circle == None): 
            return
        dx = event.xdata - self.press_event.xdata
        dy = event.ydata - self.press_event.ydata
        self.current_circle.center = int(self.x0 + dx), int(self.y0 + dy)
        self.points = [list(circle.center) for circle in self.circle_list]
        self.poly.set_xy(np.array(self.points))
        self.fig.canvas.draw()
        
    
    
        

        
if __name__=='__main__':

    
    
    start = CreatePolygon()
    plt.show()
    print start.points
