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
    aa = body.Fa / body.m
    body.Va += aa*dt
    body.a += body.Va * dt + aa*dt**2/2 

    ab = body.Fb / body.m
    body.Vb += ab*dt
    body.b += body.Vb * dt + ab*dt**2/2 

    ac = body.Fc / body.m
    body.Vc += ac*dt
    body.c += body.Vc * dt + ac*dt**2/2 


def sum_of_squares(v):
    """ v1 * v1 + v2 * v2 ... + vn * vn"""
    # или return dot_product(v, v)
    return sum(vi ** 2 for vi in v)


def body_force(body, objects):
    body.Fa = body.Fb = body.Fc = 0
    for obj in objects:
        if body == obj:
            continue
        vec = np.array([obj.a - body.a, obj.b - body.b, obj.c - body.c])
        r = np.sqrt(sum_of_squares(vec))
        unit_vec = vec / r

        df = gravitational_constant * body.m * obj.m / r ** 2
        body.Fa += df * unit_vec[0]
        body.Fb += df * unit_vec[1]
        body.Fc += df * unit_vec[2]


def recalculate_objects_positions(objects, dt):      
    for body in objects:
        body_force(body, objects)
    for body in objects:
        body_move(body, dt)
            
if __name__ == "__main__":
    print("This module is not for direct call!")
