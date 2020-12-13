# coding: utf-8
# license: GPLv3

"""
Module for physical bodies description
"""

import numpy as np


class BigBody:
    """Class that describes body with big mass"""
    def __init__(self):
        self.type = "big body"
        self.m = 1000
        self.R = 10
        self.color = "red"
        self.image = None
        self.path = []

        self.x, self.y = 0, 0

        self.r = np.array([0, 0, 0])
        self.V = np.array([0, 0, 0])
        self.F = np.array([0, 0, 0])

        self.vel_0 = (0, 0, 0)
        self.vec_0 = (0, 0, 0)

    def push(self, event):
        """
        Reacts on click
        :param event: <Button-1>
        :return: True if click was on it and False else.
        """
        center = (self.x, self.y)
        x, y = event.x - event.widget.winfo_width()//2, event.y - event.widget.winfo_height()//2
        if np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2) < self.R:
            return True
        else:
            return False


class SmallBody:
    """Class that describes body with small mass"""
    def __init__(self):
        self.type = "small body"
        self.m = 1
        self.R = 5
        self.color = "#c00"
        self.image = None

        self.x, self.y = 0, 0

        self.r = np.array([0, 0, 0])
        self.V = np.array([0, 0, 0])
        self.F = np.array([0, 0, 0])

        self.vel_0 = (0, 0, 0)
        self.vec_0 = (0, 0, 0)

    def push(self, event):
        """
        Reacts on click
        :param event: <Button-1>
        :return: True if click was on it and False else.
        """
        center = (self.x, self.y)
        x, y = event.x - event.widget.winfo_width() // 2, event.y - event.widget.winfo_height() // 2
        if np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2) < self.R:
            return True
        else:
            return False


if __name__ == "__main__":
    print("This module is not for direct call!")
