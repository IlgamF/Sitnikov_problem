# coding: utf-8
# license: GPLv3

"""
Visualization module. Describes main screen processes
"""

import ctypes
from items import *
from graphics import *


views = [['Oxy', 3*np.pi/2, np.pi, 'off'],  # surface Oxy
         ['Oxz', 3*np.pi/2, 'off', np.pi],  # surface Oxz
         ['Oyz', 'off', 3*np.pi/2, np.pi],  # surface Oyz
         ['Xyz', np.pi/4, 3*np.pi/2, np.pi],  # x looks at us and surface Oyz
         ['Yxz', 3*np.pi/2, np.pi/4, np.pi],  # y looks at us and surface Oxz
         ['Zxy', 3*np.pi/2, np.pi, np.pi/4],  # Z looks at us and surface Oxy
         ['XYz', np.pi/3, 5*np.pi/3, np.pi]]  # X, Y look at us and axis Z - up


class Window:
    """
    Window class: carries parameters:
    self.root - window
    self.space - canvas
    self.color - canvas color
    """
    def __init__(self, title, o):
        user32 = ctypes.windll.user32
        self.in_w = round(user32.GetSystemMetrics(0) / 16 * 10.8)
        self.in_h = round(user32.GetSystemMetrics(1) / 9 * 8.1)

        self.root = Tk()  # create window
        self.root.geometry('%ix%i' % (self.in_w, self.in_h))
        self.root.title(title)  # window top-left title
        self.root.minsize()

        self.light = 0  # defines color of canvas (black or white)
        self.colours = ('#161a1e', '#dcecf5')

        self.space = Canvas(self.root, bg=self.colours[self.light])
        self.space.pack(side=TOP, fill="both", expand=True)
        self.space.configure(scrollregion=(-self.in_w / 2, -self.in_h / 2,
                                           self.in_w / 2, self.in_h / 2))
        self.space.xview_moveto(.5)
        self.space.yview_moveto(.5)

        self.process = False

        self.view = 0
        self.axes_alive = [True, True, False]
        self.axes = Axis(self)
        self.angles = [(0, 0), (0, 0), (0, 0)]
        self.reorganize_axes()

        self.buttons = self.init_buttons()

        self.r_panel = RightPanel(self)
        self.l_panel = LeftPanel(self)

        self.additional = 0  # defines new windows
        self.o = o
        pass

    def init_buttons(self):
        buttons = []
        for i in (1, 2, 3, 4, -2, -1):
            but = RoundButton(self.space, self.in_w, self.in_h, i)
            buttons.append(but)
        return buttons

    def resize(self, event):
        w, h = self.root.winfo_width(), self.root.winfo_height()

        self.space.configure(scrollregion=(- w / 2, - h / 2, w / 2, h / 2))

        for i in range(len(self.buttons)):
            self.buttons[i].resize(self.space)

        self.axes.resize(self)

        self.r_panel.resize(self)
        self.l_panel.resize(self)

        self.in_w, self.in_h = w, h
        pass

    def repaint(self, event):
        self.light = abs(self.light - 1)

        self.space.configure(bg=self.colours[self.light])

        for i in self.buttons:
            i.repaint(self)
        self.buttons[5].change_img(self)

        self.axes.repaint(self)
        pass

    def reorganize_axes(self):
        view = views[self.view]
        self.axes_alive = [True, True, True]
        self.angles = [(0, 0), (0, 0), (0, 0)]
        for i in range(len(view)):
            if i == 0:
                continue
            if view[i] == 'off':  # switches off the axis, if it is not used
                self.axes_alive[i - 1] = False
                self.angles[i - 1] = (0, 0)
            else:
                phi = view[i]
                self.angles[i-1] = (np.sin(phi), np.cos(phi))
        self.axes.redraw(self)
        pass

    def push(self, event):
        a = 0
        for i in self.buttons:
            a += i.push(event)
        if a == 1:
            self.additional = InfoWindow('teor.txt')
            self.additional.file_reading('teor.txt')
            self.process = False
        if a == 2:
            self.process = False
            draw_graph(self.o, 'output.txt')
        if a == 3:
            self.additional = InfoWindow('info.txt')
            self.additional.file_reading('info.txt')
            self.process = False
        if a == 4:
            self.additional = InfoWindow('help.txt')
            self.additional.file_reading('help.txt')
            self.process = False
        if a == 5:
            self.view = (self.view + 1) % len(views)
            self.reorganize_axes()
        if a == 6:
            self.process = not self.process
        if a != 0:
            self.buttons[5].change_img(self)
        pass


class InfoWindow:
    """
    Window class: carries parameters:
    self.root - window
    self.space - canvas
    self.color - canvas color
    """
    def __init__(self, filename):
        user32 = ctypes.windll.user32
        self.in_w = round(user32.GetSystemMetrics(0) / 16 * 6)
        self.in_h = round(user32.GetSystemMetrics(1) / 9 * 4.5)

        self.close = False

        self.root = Tk()  # create window
        self.root.geometry('%ix%i' % (self.in_w, self.in_h))
        self.root.title(filename)  # window top-left title
        self.root.minsize()
        
        self.space = Canvas(self.root, bg='white')
        self.space.pack(side=TOP, fill="both", expand=True)
        self.space.configure(scrollregion=(-self.in_w / 2, -self.in_h / 2,
                                           self.in_w / 2, self.in_h / 2))

        pass

    def file_reading(self, filename):
        inp = open(filename, 'r', encoding='utf-8')
        s = inp.readlines()
        for i in range(len(s)):
            st = Label(self.root, text=s[i], font="TimesNewRoman 12", bg="white", fg="black")
            st.place(x=50, y=5+20*i)
        pass


class Point:
    """Класс, описывающий точки траектории тел"""
    def __init__(self):
        self.x = 0
        self.y = 0
        self.r = 1
        pass

    def draw_point(self, objects, w):
        for body in objects:
            self.x = body.x
            self.y = body.y
            w.space.create_oval([self.x - self.r, self.y - self.r],
                                [self.x + self.r, self.y + self.r],
                                fill="white")
        pass


def reorganize_coordinates(w, body):
    axes, angles = w.axes_alive, w.angles
    phi_x, phi_y, phi_z = angles[0], angles[1], angles[2]
    da, db, dc = (0, 0), (0, 0), (0, 0)
    if axes[0]:  # if x exists
        da = (-body.a * phi_x[0], body.a * phi_x[1])
    if axes[1]:
        db = (-body.b * phi_y[0], body.b * phi_y[1])
    if axes[2]:
        dc = (-body.c * phi_z[0], body.c * phi_z[1])
    body.x, body.y = da[0] + db[0] + dc[0], da[1] + db[1] + dc[1]
    pass


def create_body_image(w, body):
    reorganize_coordinates(w, body)
    body.image = w.space.create_oval([body.x - body.R, body.y - body.R],
                                     [body.x + body.R, body.y + body.R],
                                     fill=body.color)
    return


def update_object_position(w, body):
    reorganize_coordinates(w, body)
    w.space.coords(body.image,
                   body.x - body.R, body.y - body.R,
                   body.x + body.R, body.y + body.R)
    w.space.update()
    return


if __name__ == "__main__":
    print("This module is not for direct call!")
