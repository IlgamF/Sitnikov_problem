# coding: utf-8
# license: GPLv3

"""
Module for interaction model description
"""

import numpy as np

gravitational_constant = 1

"""Большие тела уничтожаются спустя четверть периода. Почему?."""


def body_move(body, dt):
    ax = body.Fx / body.m
    body.Vx += ax*dt
    body.x += body.Vx * dt + ax*dt**2/2

    ay = body.Fy / body.m
    body.Vy += ay*dt
    body.y += body.Vy * dt + ay*dt**2/2

    az = body.Fz / body.m
    body.Vz += az*dt
    body.z += body.Vy * dt + az*dt**2/2


def sum_of_squares(v):
    """ v1 * v1 + v2 * v2 ... + vn * vn"""
    # или return dot_product(v, v)
    return sum(vi ** 2 for vi in v)


def body_force(body, objects):
    body.Fx = body.Fy = 0
    for obj in objects:
        if body == obj:
            continue
        if obj.type == "smallbody":
            continue
        vec = np.array([obj.x - body.x, obj.y - body.y, obj.z - body.z])
        r = np.sqrt(sum_of_squares(vec))
        unit_vec = vec / r

        df = gravitational_constant * body.m * obj.m / r ** 2
        body.Fx += df * unit_vec[0]
        body.Fy += df * unit_vec[1]
        body.Fz += df * unit_vec[2]


def recalculate_objects_positions(objects, dt):
    for body in objects:
        if body.type == "bigbody":
            body.x = body.x
            body.y = 0
            body.z = 0
        if body.type == "smallbody":
            body.x = 0
            body.y = body.z 
    for body in objects:
        body_force(body, objects)
    for body in objects:
        body_move(body, dt)


if __name__ == "__main__":
    print("This module is not for direct call!")
