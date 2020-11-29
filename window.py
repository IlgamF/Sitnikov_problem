# coding: utf-8
# license: GPLv3

"""
Visualization module. Describes main screen processes
"""

import ctypes
import tkinter

user32 = ctypes.windll.user32
window_width = round(user32.GetSystemMetrics(0) * 0.8)
window_height = round(user32.GetSystemMetrics(1) * 0.6)


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
