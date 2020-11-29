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
        self.x = 0
        self.y = 0
        self.z = 0
        self.Vx = 0
        self.Vy = 0
        self.Vz = 0
        self.Fx = 0
        self.Fy = 0
        self.Fz = 0
        self.R = 10
        self.color = "red"
        self.image = None
 

class SmallBody:
    """Класс, описывающий тело меньшей массы."""
    def __init__(self):
        self.type = "smallbody"
        self.m = 1
        self.x = 0
        self.y = 0
        self.z = 0
        self.Vx = 0
        self.Vy = 0
        self.Vz = 0
        self.Fx = 0
        self.Fy = 0
        self.Fz = 0
        self.R = 5
        self.color = "red"
        self.image = None


if __name__ == "__main__":
    print("This module is not for direct call!")
