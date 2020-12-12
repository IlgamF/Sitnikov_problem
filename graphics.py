# coding: utf-8
# license: GPLv3

"""
Module for drawing graphics
"""


from matplotlib import pyplot as pl


def draw_graph(objects, output_filename1, output_filename2):

    distance1 = []
    velocity1 = []
    with open(output_filename1, 'r') as output_file:
        for line in output_file:
            if not line.split():
                continue
            else:
                distance1.append(float(line.split()[0]))
                velocity1.append(float(line.split()[1]))

    distance2 = []
    velocity2 = []
    with open(output_filename2, 'r') as output_file:
        for line in output_file:
            if not line.split():
                continue
            else:
                distance2.append(float(line.split()[0]))
                velocity2.append(float(line.split()[1]))

    pl.figure(figsize=(18, 8))

    pl.subplot(1, 2, 1)
    pl.title(r'Фазовый портрет массивного тела')
    pl.ylabel(r'$v - скорость тела$')
    pl.xlabel(r'$r - расстояние$')
    pl.plot(distance1, velocity1)  # v(r)

    pl.subplot(1, 2, 2)
    pl.title(r'Фазовый портрет легкого тела')
    pl.ylabel(r'$v - скоростьтела$')
    pl.xlabel(r'$r - расстояние$')
    pl.plot(distance2, velocity2)  # v(r)

    pl.show()
    pass


if __name__ == "__main__":
    print("This module is not for direct call!")
