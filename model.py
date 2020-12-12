# coding: utf-8
# license: GPLv3

"""
Module for interaction model description
"""

import numpy as np

gravitational_constant = 1

"""Функции движения написаны для плоскости Oxy(см.в ТЗ),
   при наблюдении из точки на оси z."""


def body_move(body, dt):
    accel = body.F / body.m
    body.V = body.V + accel * dt
    body.r += body.V * dt + accel * dt ** 2 / 2


def sum_of_squares(v):
    """ v1 * v1 + v2 * v2 ... + vn * vn"""
    # или return dot_product(v, v)
    return sum(vi ** 2 for vi in v)


def body_force(body, objects):
    body.F = (0, 0, 0)
    body.Fa = body.Fb = body.Fc = 0
    for obj in objects:
        if body == obj:
            continue
        else:
            vec = np.array(obj.r) - np.array(body.r)
            # vec = np.array([obj.a - body.a, obj.b - body.b, obj.c - body.c])
            r = np.sqrt(sum_of_squares(vec))
            unit_vec = vec / r

            df = gravitational_constant * body.m * obj.m / r ** 2
            body.F = np.array(body.F) + df * unit_vec
        pass


def recalculate_objects_positions(objects, dt):      
    for body in objects:
        body_force(body, objects)
    for body in objects:
        body_move(body, dt)


if __name__ == "__main__":
    print("This module is not for direct call!")
