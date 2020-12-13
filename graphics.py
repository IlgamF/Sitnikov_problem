# coding: utf-8
# license: GPLv3

"""
Module for drawing graphics
"""


from matplotlib import pyplot as pl


def draw_graph(objects, output_filenames):
    """
    gets data out of files with names given
    :param objects: [b1, b2, b3]
    :param output_filenames: ['filename1.txt', 'filename2.txt']
    :return:
    """
    distances = []
    velocities = []
    for filename in output_filenames:
        distance = []
        velocity = []
        with open(filename, 'r') as output_file:
            for line in output_file:
                if not line.split():
                    continue
                else:
                    distance.append(float(line.split()[0]))
                    velocity.append(float(line.split()[1]))
        distances.append(distance)
        velocities.append(velocity)

    pl.figure(figsize=(18, 8))

    pl.subplot(1, 2, 1)
    pl.title(r'Фазовый портрет массивного тела')
    pl.ylabel(r'$v - скорость тела$')
    pl.xlabel(r'$r - расстояние$')
    for i in range(len(distances[1])):
        distances[0][i] = abs(distances[0][i])
        velocities[0][i] = abs(velocities[0][i])
    pl.scatter(distances[0], velocities[0], 2)  # v(r)

    pl.subplot(1, 2, 2)
    pl.title(r'Фазовый портрет легкого тела')
    pl.ylabel(r'$v - скоростьтела$')
    pl.xlabel(r'$r - расстояние$')
    pl.plot(distances[1], velocities[1], color='red')  # v(r)

    pl.show()
    pass


if __name__ == "__main__":
    print("This module is not for direct call!")
