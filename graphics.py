# coding: utf-8
# license: GPLv3

"""
Module for drawing graphics
"""

from matplotlib import pyplot as pl


def py(a, b, c):
    return (a*a + b*b + c*c)**0.5


def data_list(obj):
    data = []
    data.append(py(obj.a, obj.b, obj.c))
    data.append(py(obj.Va, obj.Vb, obj.Vc))
    return data


def draw_graph(objects):
    """
    Функция строит графики зависимость v(r) для каждого тел
    """
    for obj in objects:
        data = data_list(obj)
        pl.title(r'$Фазовый портрет$')
        pl.ylabel(r'$v - скорость тела$')
        pl.xlabel(r'$r - расстояние$')
        pl.plot(data[0], data[1])  # v(r)
    pl.show()
    pass


if __name__ == "__main__":
    print("This module is not for direct call!")
