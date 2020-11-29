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

        self.frame = Frame(self.root)
        self.frame.pack(side=BOTTOM)

        pass

    def resize(self, event):
        w, h = self.root.winfo_width(), self.root.winfo_height()
        self.space.configure(scrollregion=(- w / 2, - h / 2, w / 2, h / 2))
        pass

    def repaint(self, event):
        self.light = abs(self.light - 1)
        self.space.configure(bg=self.colours[self.light])
        pass

    def init_buttons(self):
        canvas = self.root
        theory = RoundButton('Т', canvas)
        graphics = RoundButton('Г', canvas)
        info = RoundButton('И', canvas)
        quest = RoundButton('?', canvas)
        return


class RoundButton:
    def __init__(self, filename, frame):
        """
        :param filename:
        :param frame:
        """
        self.radius = frame.winfo_height() / 20
        self.id = Button(frame, text=filename, width=10).pack(side=LEFT)
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
