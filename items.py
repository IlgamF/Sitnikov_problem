# coding: utf-8
# license: GPLv3

"""
Visualization module. Describes main screen processes
"""

from tkinter import *
import numpy as np
from PIL import ImageTk


def point_towards(w, i):
    tg = w.angles[i][0] / w.angles[i][1]
    return [(-w.in_h / 2 * tg, w.in_h / 2), (w.in_h / 2 * tg, -w.in_h / 2)]


def point_resize(w, i):
    width, height = w.space.winfo_width(), w.space.winfo_height()
    tg = w.angles[i][0] / w.angles[i][1]
    return [(-height / 2 * tg, height / 2), (height / 2 * tg, -height / 2)]


def round_pair(a):
    return [round(a[0], 0), round(a[1], 0)]


def sum_of_squares(a, b, c):
    return (a**2 + b**2 + c**2)**0.5


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
        self.x = [(-w.in_w / 2, -2), (w.in_w / 2 - 2, -2)]
        self.y = [(0, -w.in_h / 2), (0, w.in_h / 2)]
        self.z = [(0, 0), (0, 0)]
        self.colors = [w.colours[1], w.colours[0]]
        self.alive = w.axes_alive  # [T/F, T/F, T/F]

        self.id_x = w.space.create_line(self.x[0], self.x[1], fill=self.colors[w.light])
        self.id_y = w.space.create_line(self.y[0], self.y[1], fill=self.colors[w.light])
        self.id_z = w.space.create_line(self.z[0], self.z[1], fill=self.colors[w.light])

        self.name_x = Label(w.space, text='x', font="Arial 15", bg=self.colors[w.light - 1], fg=self.colors[w.light])
        self.name_y = Label(w.space, text='y', font="Arial 15", bg=self.colors[w.light - 1], fg=self.colors[w.light])
        self.name_z = Label(w.space, text='z', font="Arial 15", bg=self.colors[w.light - 1], fg=self.colors[w.light])

        self.name_x.place(x=(self.x[1][0] + 3 * w.in_w / 8), y=(self.x[1][1] + w.in_h / 2))
        self.name_y.place(x=(self.y[0][0] + w.in_w / 2 + 10), y=20)
        pass

    def repaint(self, w):
        for i in (self.id_x, self.id_y, self.id_z):
            w.space.itemconfigure(i, fill=self.colors[w.light])

        for j in (self.name_x, self.name_y, self.name_z):
            j.configure(bg=self.colors[w.light-1], fg=self.colors[w.light])
        pass

    def redraw(self, w):
        """
        Function changes Axis positions when view changes
        :param w: Window
        :return:
        """
        x_pair = [(-w.in_w / 2, -2), (w.in_w / 2 - 2, -2)]
        x_name_pair = [(w.in_w / 2 + 3 * w.in_w // 8 - 2), (w.in_h // 2 + 5)]

        y_pair = [(0, -w.in_h / 2), (0, w.in_h / 2)]
        y_name_pair = [(w.in_w // 2 + 10), 20]

        zero = [(0, 0), (0, 0)]
        name_hide = (-100, -100)
        delta, dy = 220, 10  # special parameters for labels coordinates

        axes = [self.x, self.y, self.z]
        axis_names = [self.name_x, self.name_z, self.name_y]

        for i in range(len(axes)):
            if 0.05 < abs(w.angles[i][0]) < 0.95:
                axes[i] = point_towards(w, i)
                tg = w.angles[i][0] / w.angles[i][1]
                axis_names[i].place(x=(axes[i][0][0] + w.in_w / 2 + delta * tg),
                                    y=(axes[i][0][1]) + w.in_h / 2 - delta + dy)
            if not w.axes_alive[i]:
                axes[i] = zero
                axis_names[i].place(x=name_hide[0], y=name_hide[1])

            if round_pair(w.angles[i]) == [-1, 0]:
                axes[i] = x_pair
                axis_names[i].place(x=x_name_pair[0], y=x_name_pair[1])
            elif round_pair(w.angles[i]) == [0, -1]:
                axes[i] = y_pair
                axis_names[i].place(x=y_name_pair[0], y=y_name_pair[1])

        self.x, self.y, self.z = axes
        self.re_cord(w)
        pass

    def resize(self, w):
        width, height = w.space.winfo_width(), w.space.winfo_height()

        x_pair = [(-width / 2, -2), (width / 2 - 2, -2)]
        x_name_pair = [(width / 2 + 3 * width // 8 - 2), (height // 2 + 5)]

        y_pair = [(0, -height / 2), (0, height / 2)]
        y_name_pair = [(width // 2 + 10), 20]

        zero = [(0, 0), (0, 0)]
        name_hide = (-100, -100)
        delta, dy = 220, 10  # special parameters for labels coordinates

        axes = [self.x, self.y, self.z]
        axis_names = [self.name_x, self.name_y, self.name_z]

        for i in range(len(axes)):
            if 0.05 < abs(w.angles[i][0]) < 0.95:
                axes[i] = point_resize(w, i)
                tg = w.angles[i][0] / w.angles[i][1]
                axis_names[i].place(x=(axes[i][0][0] + width / 2 + delta * tg),
                                    y=(axes[i][0][1]) + height / 2 - delta + dy)
            if not w.axes_alive[i]:
                axes[i] = zero
                axis_names[i].place(x=name_hide[0], y=name_hide[1])

            if round_pair(w.angles[i]) == [-1, 0]:
                axes[i] = x_pair
                axis_names[i].place(x=x_name_pair[0], y=x_name_pair[1])
            elif round_pair(w.angles[i]) == [0, -1]:
                axes[i] = y_pair
                axis_names[i].place(x=y_name_pair[0], y=y_name_pair[1])

        self.x, self.y, self.z = axes
        self.re_cord(w)
        pass

    def re_cord(self, w):
        id_list = [self.id_x, self.id_y, self.id_z]
        coordinates_list = [self.x, self.y, self.z]
        for i in range(len(id_list)):
            w.space.coords(id_list[i],
                           coordinates_list[i][0][0], coordinates_list[i][0][1],
                           coordinates_list[i][1][0], coordinates_list[i][1][1])
        pass


class LeftPanel:
    def __init__(self, w):
        width, height = w.in_w, w.in_h
        self.left_top = (- width // 2 + 15, - height//2 + 15)
        self.right_bottom = (- width // 2 + 400, - height//2 + 125)
        self.id = w.space.create_rectangle(self.left_top, self.right_bottom, fill='#fff')
        self.info = 0
        pass

    def resize(self, w):
        width, height = w.space.winfo_width(), w.space.winfo_height()
        self.left_top = (- width // 2 + 15, - height//2 + 15)
        self.right_bottom = (- width // 2 + 350, - height//2 + 125)
        w.space.coords(self.id, self.left_top[0], self.left_top[1], self.right_bottom[0], self.right_bottom[1])
        pass

    def show_info(self, w):
        # функция должна выводить информацию о координате и скорости тел
        if self.info.type == "big body":
            text_name = 'Массивное тело \n'
        else:
            text_name = 'Тело малой массы \n'
        dist = round(sum_of_squares(self.info.a, self.info.b, self.info.c), 2)
        vel = round(sum_of_squares(self.info.Va, self.info.Vb, self.info.Vc), 2)
        accel = round(sum_of_squares(self.info.Fa, self.info.Fb, self.info.Fc) / self.info.m, 3)
        text_mass = 'Масса тела: ' + str(self.info.m) + ' отн. ед. \n'
        text_distance = 'Расстояние от центра системы: ' + str(dist) + ' у.е. \n'
        text_velocity = 'Скорость тела: ' + str(vel) + ' у.е \n'
        text_accel = 'Ускорение тела: ' + str(accel) + ' у.е'

        txt = text_name + text_mass + text_distance + text_velocity + text_accel
        st = Label(w.space, text=txt, font="Arial 12", bg="#fff", fg=self.info.color, justify='left')
        st.place(x=17, y=17)
        pass


class RightPanel:
    def __init__(self, w):
        width, height = w.in_w, w.in_h
        self.left_top = (width // 2 - 118, - height//2 + 15)
        self.right_bottom = (width // 2 - 15, height // 2 - 75)
        self.id = w.space.create_rectangle(self.left_top, self.right_bottom, fill='#fff')
        pass

    def resize(self, w):
        width, height = w.space.winfo_width(), w.space.winfo_height()
        self.left_top = (width // 2 - 118, - height//2 + 15)
        self.right_bottom = (width // 2 - 15, height // 2 - 75)
        w.space.coords(self.id, self.left_top[0], self.left_top[1], self.right_bottom[0], self.right_bottom[1])
        pass
