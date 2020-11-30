# coding: utf-8
# license: GPLv3

"""
Visualization module. Describes main screen processes
"""

import ctypes
from tkinter import *
from PIL import Image, ImageTk


class Window:
    """
    Window class: carries parameters:
    self.root - window
    self.space - canvas
    self.color - canvas color
    """
    def __init__(self):
        user32 = ctypes.windll.user32
        window_width = round(user32.GetSystemMetrics(0) / 16 * 8)
        window_height = round(user32.GetSystemMetrics(1) / 9 * 6)

        self.root = Tk()  # create window
        self.root.geometry('%ix%i' % (window_width, window_height))
        self.root.title('Sitnikov problem')  # window top-left title
        self.root.minsize()

        self.light = 0  # defines color of canvas (black or white)
        self.colours = ('black', 'white')

        self.space = Canvas(self.root, bg='black')
        self.space.pack(side=TOP, fill="both", expand=True)
        self.space.configure(scrollregion=(-window_width / 2, -window_height / 2, window_width / 2, window_height / 2))
        self.space.xview_moveto(.5)
        self.space.yview_moveto(.5)

        self.buttons = self.init_buttons()
        # self.resize(1)

        pass

    def resize(self, event):
        w, h = self.root.winfo_width(), self.root.winfo_height()
        self.space.configure(scrollregion=(- w / 2, - h / 2, w / 2, h / 2))
        for i in range(len(self.buttons)):
            self.buttons[i].resize(self.space)
        pass

    def repaint(self, event):
        self.light = abs(self.light - 1)
        self.space.configure(bg=self.colours[self.light])
        pass

    def init_buttons(self):
        canvas = self.space
        theory = RoundButton(canvas, 1)
        graphics = RoundButton(canvas, 2)
        info = RoundButton(canvas, 3)
        quest = RoundButton(canvas, 4)
        eye = RoundButton(canvas, 17)
        play = RoundButton(canvas, 18)
        return [theory, graphics, info, quest, eye, play]


class RightPanel:
    def __init__(self, canvas, root):
        w, h = root.winfo_width(), root.winfo_height()
        print(w, h)
        pass


class RoundButton:
    def __init__(self, canvas, i):
        self.width, self.height = canvas.winfo_width(), canvas.winfo_height()
        self.radius = self.width // 20
        self.i = i
        self.num = i % 12  # button serial number
        self.colours_light = ['#c00', '#0c0', '#00c', '#f40', '#408', '#408']
        self.colours_dark = ['#c55', '#0f8', '#dff', '#fe8', '#e8e', '#e8e']
        self.id = canvas.create_oval((-self.width // 2 + (self.radius + 1) * i, self.height // 2 - self.radius - 5),
                                     (-self.width//2 + (self.radius+1)*(i+1), self.height//2 - 5),
                                     fill=self.colours_dark[self.num-1], width=4)
        pass

    def resize(self, canvas):
        self.width, self.height = canvas.winfo_width(), canvas.winfo_height()
        self.radius = self.width // 20
        canvas.coords(self.id, -self.width // 2 + (self.radius + 1) * self.i, self.height // 2 - self.radius - 5,
                      -self.width//2 + (self.radius+1)*(self.i+1), self.height//2 - 5)
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
