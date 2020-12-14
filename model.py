# coding: utf-8
# license: GPLv3

"""
Module for interaction model description
"""

import numpy as np

gravitational_constant = 1


def body_move(body, dt):
    """
    Defines point movement
    :param body: BigBody or SmallBody from Objects
    :param dt: time interval
    :return:
    """
    accel = body.F / body.m
    body.V = body.V + accel * dt
    body.r += body.V * dt + accel * dt ** 2 / 2
    pass


def sum_of_squares(v):
    """
    Returns sum of squares
    :param v: [v_1, v_2, ..., v_n] where w_i - a number
    :return: v_1**2 + v_2**2 + ... + v_n**2
    """
    return sum(vi ** 2 for vi in v)


def body_force(body, objects):
    """
    Calculates forces
    :param body: BigBody or SmallBody from Objects
    :param objects: Objects ([b1, b2, b])
    :return:
    """
    body.F = (0, 0, 0)
    body.Fa = body.Fb = body.Fc = 0
    for obj in objects:
        if body == obj:
            continue
        elif obj.type == 'small body':
            continue
        else:
            vec = np.array(obj.r) - np.array(body.r)
            r = np.sqrt(sum_of_squares(vec))
            unit_vec = vec / r

            df = gravitational_constant * body.m * obj.m / r ** 2
            body.F = np.array(body.F) + df * unit_vec
        pass


def recalculate_objects_positions(objects, dt):
    """
    Main function in module, recalculates objects positions
    :param objects: Objects ([b1, b2, b])
    :param dt: time interval
    :return:
    """
    for body in objects:
        body_force(body, objects)
    for body in objects:
        body_move(body, dt)
    pass


if __name__ == "__main__":
    print("This module is not for direct call!")
