# coding: utf-8
# license: GPLv3

"""
Visualization module. Describes main screen processes
"""

import ctypes
import tkinter


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

        self.root = tkinter.Tk()  # create window
        self.root.title('Sitnikov problem')  # window top-left title
        self.root.resizable = (True, True)
        self.root.minsize = (window_width, window_height)  # minimal window width

        self.light = False  # defines color of canvas (black or white

        self.space = tkinter.Canvas(self.root, width=window_width, height=window_height, bg='black')
        self.space.pack(side=tkinter.TOP)
        self.space.configure(scrollregion=(-window_width / 2, -window_height / 2, window_width / 2, window_height / 2))
        self.space.xview_moveto(.5)
        self.space.yview_moveto(.5)
        pass

    def resize(self, event):
        self.space.configure(width=event.widget.winfo_width(), height=event.widget.winfo_height())
        pass

    def repaint(self):
        print('Paint!')
        self.light = not self.light
        if self.light:
            self.space.configure(bg='white')
        else:
            self.space.configure(bg='black')
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
