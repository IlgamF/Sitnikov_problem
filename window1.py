# coding: utf-8
# license: GPLv3

"""
Visualization module. Describes main screen processes
"""
""" Наверное, стоит сделать два модуля визуализации,
    один модуль слишком громоздкий.
    Сюда переместил кнопки"""
import ctypes
from tkinter import *
import numpy as np
from PIL import ImageTk, Image
           
class RightPanel:
    def __init__(self, canvas, root):
        w, h = root.winfo_width(), root.winfo_height()
        print(w, h)
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
