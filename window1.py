# coding: utf-8
# license: GPLv3

"""
Visualization module. Describes main screen processes
"""

from tkinter import *
import numpy as np
from PIL import ImageTk, Image


class RightPanel:
    def __init__(self, w):
        width, height = w.in_w, w.in_h
        self.left_top = (width * 3/8, - height//2 + 15)
        self.right_bottom = (width // 2 - 15, height // 2 - 75)
        self.id = w.space.create_rectangle(self.left_top, self.right_bottom, fill='#ccc')
        pass

    def resize(self, w):
        width, height = w.space.winfo_width(), w.space.winfo_height()
        self.left_top = (width * 3/8, - height//2 + 15)
        self.right_bottom = (width // 2 - 15, height // 2 - 75)
        w.space.coords(self.id, self.left_top[0], self.left_top[1], self.right_bottom[0], self.right_bottom[1])
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

    def repaint(self, w):
        if w.light == 1:
            self.filename = self.colours_light[self.num - 1] + '.png'
            self.obj = ImageTk.PhotoImage(file=self.filename)
            w.space.itemconfigure(self.id, image=self.obj)
        else:
            self.filename = self.colours_dark[self.num - 1] + '.png'
            self.obj = ImageTk.PhotoImage(file=self.filename)
            w.space.itemconfigure(self.id, image=self.obj)
        pass

    def push(self, event):
        center = (self.point_x + self.radius, self.point_y + self.radius)
        x, y = event.x - self.width//2, event.y - self.height//2
        if np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2) < self.radius - 3:
            print(self.num)
            return self.num
        else:
            return 0


class Axis:
    def __init__(self, w, i):
        self.index = i
        self.size = 0.8
        self.x = [(-w.in_w / 2, 2), (w.in_w / 2 - 2, 2)]
        self.y = [(0, -w.in_h / 2), (0, w.in_h / 2)]
        self.z = [(0, 0), (0, 0)]
        self.colors = ['white', 'black']
        self.alive = w.axes_alive  # [T/F, T/F, T/F]
        self.id_x = w.space.create_line(self.x[0], self.x[1], fill=self.colors[w.light])
        self.id_y = w.space.create_line(self.y[0], self.y[1], fill=self.colors[w.light])
        self.id_z = w.space.create_line(self.z[0], self.z[1], fill=self.colors[w.light])
        pass

    def repaint(self, w):
        for i in (self.id_x, self.id_y, self.id_z):
            w.space.itemconfigure(i, fill=self.colors[w.light])
        pass

    def resize_surface(self, w):
        width, height = w.space.winfo_width(), w.space.winfo_height()
        if w.axes_alive[0]:
            self.x = [(-width / 2, 0), (width / 2, 0)]
            if w.axes_alive[1]:
                self.y = [(0, -height / 2), (0, height / 2)]
            else:
                self.z = [(0, -height / 2), (0, height / 2)]
        else:
            self.y = [(-width / 2, 0), (width / 2, 0)]
            self.z = [(0, -height / 2), (0, height / 2)]

        w.space.coords(self.id_x, self.x[0][0], self.x[0][1], self.x[1][0], self.x[1][1])
        w.space.coords(self.id_y, self.y[0][0], self.y[0][1], self.y[1][0], self.y[1][1])
        w.space.coords(self.id_z, self.z[0][0], self.z[0][1], self.z[1][0], self.z[1][1])
        pass

    def resize_general(self, w):
        # FIXME пока не знаю, что делать
        pass

