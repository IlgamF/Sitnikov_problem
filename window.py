# coding: utf-8
# license: GPLv3

"""
Visualization module. Describes main screen processes
"""

import ctypes
from tkinter import *
import numpy as np
from PIL import ImageTk, Image

views = [['Oxy', 0, np.pi/2, 'off'],  # surface Oxy
         ['Oxz', np.pi/2, 'off', 0],  # surface Oxz
         ['Oyz', 'off', np.pi/2, 0],  # surface Oyz
         ['Xyz', np.pi/2, np.pi/2, 0],  # x looks at us and surface Oyz
         ['Yxz', np.pi/2, np.pi * 3/4, 0],  # y looks at us and surface Oxz
         ['Zxy', np.pi/2, 0, np.pi/4],  # Z looks at us and surface Oxy
         ['XYz', np.pi/3, np.pi * 5/3, 0]]  # X, Y look at us and axis Z - up


class Window:
    """
    Window class: carries parameters:
    self.root - window
    self.space - canvas
    self.color - canvas color
    """
    def __init__(self):
        user32 = ctypes.windll.user32
        self.in_w = round(user32.GetSystemMetrics(0) / 16 * 8)
        self.in_h = round(user32.GetSystemMetrics(1) / 9 * 6)

        self.root = Tk()  # create window
        self.root.geometry('%ix%i' % (self.in_w, self.in_h))
        self.root.title('Sitnikov problem')  # window top-left title
        self.root.minsize()

        self.light = 0  # defines color of canvas (black or white)
        self.colours = ('black', 'white')

        self.space = Canvas(self.root, bg='black')
        self.space.pack(side=TOP, fill="both", expand=True)
        self.space.configure(scrollregion=(-self.in_w / 2, -self.in_h / 2,
                                           self.in_w / 2, self.in_h / 2))
        self.space.xview_moveto(.5)
        self.space.yview_moveto(.5)

        self.view = 0
        self.xy = self.reorganize_axes()

        self.buttons = self.init_buttons()

        self.axes = self.init_axes()
        pass

    def init_buttons(self):
        buttons = []
        for i in (1, 2, 3, 4, -2, -1):
            but = RoundButton(self.space, self.in_w, self.in_h, i)
            buttons.append(but)
        return buttons

    def init_axes(self):
        axes = []
        for i in (1, 2, 3):
            a = Axis(self.space, self.in_w, self.in_h, i)
            axes.append(a)
        return axes

    def resize(self, event):
        w, h = self.root.winfo_width(), self.root.winfo_height()
        self.space.configure(scrollregion=(- w / 2, - h / 2, w / 2, h / 2))
        for i in range(len(self.buttons)):
            self.buttons[i].resize(self.space)
        for k in range(len(self.axes)):
            self.axes[k].resize(self.space)
        self.in_w, self.in_h = w, h
        pass

    def repaint(self, event):
        self.light = abs(self.light - 1)
        self.space.configure(bg=self.colours[self.light])
        for i in self.buttons:
            i.repaint(self.light, self.space)
        for t in self.axes:
            t.repaint(self.space, self.light)
        pass

    def push(self, event):
        a = 0
        for i in self.buttons:
            a += i.push(event)
        if a == 5:
            self.view = (self.view + 1) % len(views)
            self.xy = self.reorganize_axes()
        pass

    def reorganize_axes(self):
        """
        Switches axes on or off in dependence on w.view
        :param w: Window
        :return: x_axis, y_axis, z_axis
        """
        view = views[self.view]
        print(view[0])
        axes = [True, True, True]
        for i in range(len(view)):
            if i == 0:
                print(view[i])
            elif view[i] == 'off':  # switches off the axis, if it is not used
                axes[i - 1] = False
        return view, axes


class RightPanel:
    def __init__(self, canvas, root):
        w, h = root.winfo_width(), root.winfo_height()
        print(w, h)
        pass


class Axis:
    def __init__(self, canvas, width, height, i):
        self.in_w, self.in_h = width, height
        self.width, self.height = width, height
        self.colours = ['white', 'black']
        print(self.width, self.height)
        self.i = i
        if i == 1:  # axis X
            self.start_x, self.finish_x = -self.width//2, self.width//2
            self.start_y, self.finish_y = 0, 0
        elif i == 2:  # axis Y
            self.start_x, self.finish_x = 0, 0
            self.start_y, self.finish_y = -self.height // 2, self.height // 2
        else:  # axis Z
            self.start_x = self.start_y = self.finish_x = self.finish_y = 0
        self.id = canvas.create_line(self.start_x, self.start_y, self.finish_x, self.finish_y, fill='white')
        pass

    def resize(self, canvas):
        self.width, self.height = canvas.winfo_width(), canvas.winfo_height()
        rec_x, rec_y = self.width / self.in_w, self.height / self.in_h
        self.in_w, self.in_h = self.width, self.height
        self.start_x *= rec_x
        self.start_y *= rec_y
        self.finish_x *= rec_x
        self.finish_y *= rec_y
        canvas.coords(self.id, self.start_x, self.start_y, self.finish_x, self.finish_y)
        pass

    def repaint(self, canvas, light):
        canvas.itemconfigure(self.id, fill=self.colours[light])
        pass


class RoundButton:
    def __init__(self, canvas, width, height, i):
        self.width, self.height = width, height
        self.radius = 28
        self.i = i
        if i > 0:
            self.num = i  # button serial number
        else:
            self.num = 7 + i
        self.colours_dark = ['th1', 'gr1', 'in1', 'q1', 'ey1', 'pl1']
        self.colours_light = ['th2', 'gr2', 'in2', 'q2', 'ey2', 'pl2']
        if i > 0:
            self.point_x = -self.width // 2 + (self.i - 1) * 2 * self.radius + 10
        else:
            self.point_x = self.width // 2 + self.i * 2 * self.radius - 10
        self.point_y = self.height // 2 - 2 * self.radius - 5
        self.filename = self.colours_dark[self.num-1] + '.png'
        self.obj = ImageTk.PhotoImage(file=self.filename)
        self.id = canvas.create_image(self.point_x, self.point_y, anchor=NW, image=self.obj)
        pass

    def resize(self, canvas):
        self.width, self.height = canvas.winfo_width(), canvas.winfo_height()
        if self.i > 0:
            self.point_x = -self.width // 2 + (self.i - 1) * 2 * self.radius + 10
        else:
            self.point_x = self.width // 2 + self.i * 2 * self.radius - 5
        self.point_y = self.height // 2 - 2 * self.radius - 10
        canvas.coords(self.id, self.point_x, self.point_y)
        pass

    def repaint(self, light, canvas):
        if light == 1:
            self.filename = self.colours_light[self.num - 1] + '.png'
            self.obj = ImageTk.PhotoImage(file=self.filename)
            canvas.itemconfigure(self.id, image=self.obj)
        else:
            self.filename = self.colours_dark[self.num - 1] + '.png'
            self.obj = ImageTk.PhotoImage(file=self.filename)
            canvas.itemconfigure(self.id, image=self.obj)
        pass

    def push(self, event):
        center = (self.point_x + self.radius, self.point_y + self.radius)
        x, y = event.x - self.width//2, event.y - self.height//2
        if np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2) < self.radius - 3:
            print(self.num)
            return self.num
        else:
            return 0


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
    view, axes = w.xy
    da, db, dc = (0, 0), (0, 0), (0, 0)
    if axes[0]:  # if x exists
        da = (-body.a * np.sin(view[1]), body.a * np.cos(view[1]))
    if axes[1]:
        db = (body.b * np.sin(view[2]), body.b * np.cos(view[2]))
    if axes[2]:
        dc = (body.c * np.sin(view[3]), - body.c * np.cos(view[3]))
    body.x, body.y = da[0] + db[0] + dc[0], da[1] + db[1] + dc[1]
    pass


def create_body_image(w, body):
    reorganize_coordinates(w, body)
    x = body.x
    y = body.y
    r = body.R
    body.image = w.space.create_oval([x - r, y - r], [x + r, y + r], fill=body.color)
    return


def update_object_position(w, body):
    reorganize_coordinates(w, body)
    x = body.x
    y = body.y
    r = body.R
    w.space.coords(body.image, x - r, y - r, x + r, y + r)
    w.space.update()
    return


if __name__ == "__main__":
    print("This module is not for direct call!")
