# coding: utf-8
# license: GPLv3

"""
Visualization module. Describes main screen processes
"""

import ctypes
from tkinter import *
import numpy as np


class Window:
    """
    Window class: carries parameters:
    self.root - window
    self.space - canvas
    self.color - canvas color
    """
    def __init__(self):
        user32 = ctypes.windll.user32
        self.window_width = round(user32.GetSystemMetrics(0) / 16 * 8)
        self.window_height = round(user32.GetSystemMetrics(1) / 9 * 6)

        self.root = Tk()  # create window
        self.root.geometry('%ix%i' % (self.window_width, self.window_height))
        self.root.title('Sitnikov problem')  # window top-left title
        self.root.minsize()

        self.light = 0  # defines color of canvas (black or white)
        self.colours = ('black', 'white')

        self.space = Canvas(self.root, bg='black')
        self.space.pack(side=TOP, fill="both", expand=True)
        self.space.configure(scrollregion=(-self.window_width / 2, -self.window_height / 2,
                                           self.window_width / 2, self.window_height / 2))
        self.space.xview_moveto(.5)
        self.space.yview_moveto(.5)

        self.buttons = self.init_buttons()

        self.axes = self.init_axes()
        pass

    def init_buttons(self):
        canvas = self.space
        theory = RoundButton(canvas, self.window_width, self.window_height, 1)
        graphics = RoundButton(canvas, self.window_width, self.window_height, 2)
        info = RoundButton(canvas, self.window_width, self.window_height, 3)
        quest = RoundButton(canvas, self.window_width, self.window_height, 4)
        eye = RoundButton(canvas, self.window_width, self.window_height, 17)
        play = RoundButton(canvas, self.window_width, self.window_height, 18)
        return [theory, graphics, info, quest, eye, play]

    def init_axes(self):
        axis_a = Axis(self.space, self.window_width, self.window_height, 1)
        axis_b = Axis(self.space, self.window_width, self.window_height, 2)
        axis_c = Axis(self.space, self.window_width, self.window_height, 3)
        self.space.update()
        return [axis_a, axis_b, axis_c]

    def resize(self, event):
        w, h = self.root.winfo_width(), self.root.winfo_height()
        self.space.configure(scrollregion=(- w / 2, - h / 2, w / 2, h / 2))
        for i in range(len(self.buttons)):
            self.buttons[i].resize(self.space)
        for k in range(len(self.axes)):
            self.axes[k].resize(self.space)
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
        for i in self.buttons:
            i.push(event)
        pass


class RightPanel:
    def __init__(self, canvas, root):
        w, h = root.winfo_width(), root.winfo_height()
        print(w, h)
        pass


class Axis:
    def __init__(self, canvas, width, height, i):
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
        if self.i == 1:  # axis X
            self.start_x, self.finish_x = -self.width // 2, self.width // 2
            self.start_y, self.finish_y = 0, 0
        elif self.i == 2:  # axis Y
            self.start_x, self.finish_x = 0, 0
            self.start_y, self.finish_y = -self.height // 2, self.height // 2
        else:  # axis Z
            self.start_x = self.start_y = self.finish_x = self.finish_y = 0
        canvas.coords(self.id, self.start_x, self.start_y, self.finish_x, self.finish_y)
        pass

    def repaint(self, canvas, light):
        canvas.itemconfigure(self.id, fill=self.colours[light])
        pass


class RoundButton:
    def __init__(self, canvas, width, height, i):
        self.width, self.height = width, height
        print(self.width, self.height)
        self.radius = self.width // 40
        self.i = i
        self.num = i % 12  # button serial number
        self.colours_light = ['#c00', '#0c0', '#00c', '#f40', '#408', '#408']
        self.colours_dark = ['#c55', '#0f8', '#dff', '#fe8', '#e8e', '#e8e']
        self.center_x = -self.width//2 + self.i * 2 * self.radius + 1
        self.center_y = self.height // 2 - self.radius - 5
        self.id = canvas.create_oval((self.center_x - self.radius, self.center_y - self.radius),
                                     (self.center_x + self.radius, self.center_y + self.radius),
                                     fill=self.colours_dark[self.num-1], width=2)
        pass

    def resize(self, canvas):
        self.width, self.height = canvas.winfo_width(), canvas.winfo_height()
        print(self.width, self.height)
        self.radius = self.width // 40
        self.center_x = -self.width // 2 + self.i * 2 * self.radius + 1
        self.center_y = self.height // 2 - self.radius - 5
        canvas.coords(self.id,
                      self.center_x - self.radius, self.center_y - self.radius,
                      self.center_x + self.radius, self.center_y + self.radius)
        pass

    def repaint(self, light, canvas):
        if light == 1:
            canvas.itemconfigure(self.id, fill=self.colours_light[self.num-1])
        else:
            canvas.itemconfigure(self.id, fill=self.colours_dark[self.num-1])
        pass

    def push(self, event):
        x, y = event.x - self.width//2, event.y - self.height//2
        if np.sqrt((x - self.center_x)**2 + (y - self.center_y)**2) <= self.radius:
            if self.num == 1:
                print(1)
                # функция вывода окна с теоретическими выгладками
            elif self.num == 2:
                print(2)
                # функция вывода окна с графиками
            elif self.num == 3:
                print(3)
                # функция вывода окна с графиками
            elif self.num == 4:
                print(4)
                # функция вывода окна с графиками
            elif self.num == 5:
                print(5)
                change_view()  # функция смены вида
            else:
                print(6)   # функция запуска


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


def change_view():
    pass


def create_body_image(space, body):
    """
    :param space:
    :param body:
    :return:
    """
    x = body.x
    y = body.y
    r = body.R
    body.image = space.create_oval([x - r, y - r], [x + r, y + r], fill=body.color)
    return


def update_object_position(space, body):
    """
    :param space:
    :param body:
    :return:
    """
    x = body.x
    y = body.y
    r = body.R
    space.coords(body.image, x - r, y - r, x + r, y + r)
    space.update()
    return


if __name__ == "__main__":
    print("This module is not for direct call!")
