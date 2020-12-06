# coding: utf-8
# license: GPLv3

"""
Visualization module. Describes main screen processes
"""

from tkinter import *
import numpy as np
from PIL import ImageTk, Image


def point_towards(w, i):
    tg = w.angles[i][0] / w.angles[i][1]
    return [(-w.in_h / 2 * tg, w.in_h / 2), (w.in_h / 2 * tg, -w.in_h / 2)]


def round_pair(a):
    return [round(a[0], 0), round(a[1], 0)]


class RightPanel:
    def __init__(self, w):
        width, height = w.in_w, w.in_h
        self.left_top = (width * 3/8, - height//2 + 15)
        self.right_bottom = (width // 2 - 15, height // 2 - 75)
        self.id = w.space.create_rectangle(self.left_top, self.right_bottom, fill='#ccc')
        pass

    def resize(self, w):
        width, height = w.space.winfo_width(), w.space.winfo_height()
        self.left_top = (width // 2 - 115, - height//2 + 15)
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
            return self.num
        else:
            return 0

    def change_img(self, w):
        images = [['pl1', 'pl2'], ['pa1', 'pa2']]
        process = int(w.process)
        self.filename = images[process][w.light] + '.png'
        self.obj = ImageTk.PhotoImage(file=self.filename)
        w.space.itemconfigure(self.id, image=self.obj)
        pass


class Axis:
    def __init__(self, w):
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

    def redraw(self, w):
        x_pair = [(-w.in_w / 2, 2), (w.in_w / 2 - 2, 2)]
        y_pair = [(0, -w.in_h / 2), (0, w.in_h / 2)]
        zero = [(0, 0), (0, 0)]
        print(w.angles)
        print(w.axes_alive)
        if 0.05 < abs(w.angles[0][0]) < 0.95:
            self.x = point_towards(w, 0)
        if 0.05 < abs(w.angles[1][0]) < 0.95:
            print('good!')
            self.y = point_towards(w, 1)
        if 0.05 < abs(w.angles[2][0]) < 0.95:
            self.z = point_towards(w, 2)

        if not w.axes_alive[0]:
            self.x = zero
        elif not w.axes_alive[1]:
            self.y = zero
        elif not w.axes_alive[2]:
            self.z = zero

        if round_pair(w.angles[0]) == [-1, 0]:
            self.x = x_pair
        elif round_pair(w.angles[0]) == [0, -1]:
            self.x = y_pair

        if round_pair(w.angles[1]) == [-1, 0]:
            self.y = x_pair
        elif round_pair(w.angles[1]) == [0, -1]:
            self.y = y_pair

        if round_pair(w.angles[2]) == [-1, 0]:
            self.z = x_pair
        elif round_pair(w.angles[2]) == [0, -1]:
            self.z = y_pair

        self.re_cord(w)
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

        self.re_cord(w)
        pass

    def resize_general(self, w):
        pass

    def re_cord(self, w):
        w.space.coords(self.id_x, self.x[0][0], self.x[0][1], self.x[1][0], self.x[1][1])
        w.space.coords(self.id_y, self.y[0][0], self.y[0][1], self.y[1][0], self.y[1][1])
        w.space.coords(self.id_z, self.z[0][0], self.z[0][1], self.z[1][0], self.z[1][1])
        pass


class LeftPanel:
    def __init__(self, w):
        width, height = w.in_w, w.in_h
        self.left_top = (- width // 2 + 15, - height//2 + 15)
        self.right_bottom = (- width // 2 + 280, - height//2 + 210)
        self.id = w.space.create_rectangle(self.left_top, self.right_bottom, fill='#ccc')
        self.info = 2
        pass

    def resize(self, w):
        width, height = w.space.winfo_width(), w.space.winfo_height()
        self.left_top = (- width // 2 + 15, - height//2 + 15)
        self.right_bottom = (- width // 2 + 280, - height//2 + 210)
        w.space.coords(self.id, self.left_top[0], self.left_top[1], self.right_bottom[0], self.right_bottom[1])
        pass
