# coding: utf-8
# license: GPLv3

"""
Module for physical bodies description
"""

import numpy as np


class BigBody:
    """Класс, описывающий тело большей массы."""
    def __init__(self):
        self.type = "big body"
        self.m = 1000
        self.R = 10
        self.color = "red"
        self.image = None
        self.path = []
        
        self.x, self.y = 0, 0

        self.a, self.b, self.c = 0, 0, 0
        self.Va, self.Vb, self.Vc = 0, 0, 0
        self.Fa, self.Fb, self.Fc = 0, 0, 0

    def push(self, event):
        center = (self.x, self.y)
        x, y = event.x - event.widget.winfo_width()//2, event.y - event.widget.winfo_height()//2
        if np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2) < self.R:
            return True
        else:
            return False


class SmallBody:
    """Класс, описывающий тело меньшей массы."""
    def __init__(self):
        self.type = "small body"
        self.m = 1
        self.R = 5
        self.color = "#c00"
        self.image = None

        self.x, self.y = 0, 0

        self.a, self.b, self.c = 0, 0, 0
        self.Va, self.Vb, self.Vc = 0, 0, 0
        self.Fa, self.Fb, self.Fc = 0, 0, 0

    def push(self, event):
        center = (self.x, self.y)
        x, y = event.x - event.widget.winfo_width() // 2, event.y - event.widget.winfo_height() // 2
        if np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2) < self.R:
            return True
        else:
            return False


if __name__ == "__main__":
    print("This module is not for direct call!")
