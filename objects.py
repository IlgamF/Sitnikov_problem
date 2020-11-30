# coding: utf-8
# license: GPLv3

"""
Module for physical bodies description
"""


class BigBody:
    """Класс, описывающий тело большей массы."""
    def __init__(self):
        self.type = "bigbody"
        self.m = 1000
        self.R = 10
        self.color = "red"
        self.image = None
        self.path = []
        
        self.x, self.y = 0, 0

        self.a, self.b, self.c = 0, 0, 0
        self.Va, self.Vb, self.Vc = 0, 0, 0
        self.Fa, self.Fb, self.Fc = 0, 0, 0


class SmallBody:
    """Класс, описывающий тело меньшей массы."""
    def __init__(self):
        self.type = "smallbody"
        self.m = 1
        self.R = 5
        self.color = "red"
        self.image = None

        self.x, self.y = 0, 0

        self.a, self.b, self.c = 0, 0, 0
        self.Va, self.Vb, self.Vc = 0, 0, 0
        self.Fa, self.Fb, self.Fc = 0, 0, 0


if __name__ == "__main__":
    print("This module is not for direct call!")
