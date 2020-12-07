# coding: utf-8
# license: GPLv3

"""
Module for drawing graphics
"""


from matplotlib import pyplot as pl




def draw_graph(objects, output_filename):

    distance = []
    velocity = []
    with open(output_filename, 'r') as output_file:
        for line in output_file:
            if line.split() == []:
                continue
            else:
                distance.append(float(line.split()[0]))
                velocity.append(float(line.split()[1]))
    
    pl.title(r'$Фазовый портрет$')
    pl.ylabel(r'$v - скорость тела$')
    pl.xlabel(r'$r - расстояние$')
    pl.plot(distance, velocity)  # v(r)
    pl.show()
    pass


if __name__ == "__main__":
    print("This module is not for direct call!")
