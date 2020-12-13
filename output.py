# coding: utf-8
# license: GPLv3

"""
Module for saving data to special files
"""


def py(vec):
    """
    Returns vector length
    :param vec: [x1, x2, ..., xn]
    :return: sqrt(x1**2 + ... + xn**2)
    """
    square = 0
    for i in range(len(vec)):
        square += vec[i]**2
    return square**0.5


def cos_theorem(vec1, vec2):
    """
    Defines relative orientation
    :param vec1: [x1, x2, ..., xn]
    :param vec2: [y1, y2, ..., yn]
    :return: 1 if scalar product is > 0, else returns -1
    """
    scalar = 0
    for i in range(3):
        scalar += vec1[i] * vec2[i]
    if scalar < 0:
        return -1
    else:
        return 1


def delete_last_stats(output_filename):
    """
    Deletes previous data in 'output_filename.txt'
    :param output_filename: 'filename.txt'
    :return:
    """
    with open(output_filename, 'w') as output_file:
        print('', file=output_file)
    pass


def write_stats_data_to_file(output_filename, body):
    """
    Saves center-distance and velocity as <r>, <V> into 'output_filename.txt'
    :param output_filename: 'filename.txt'
    :param body: BigBody or SmallBody from Objects: [b1, b2, b]
    :return:
    """
  
    file_list = []
    r = py(body.r) * cos_theorem(body.r, body.vec_0)
    vel = py(body.V) * cos_theorem(body.V, body.vel_0)
    r = '{} '.format(r)
    vel = '{} '.format(vel)
    line = r + vel
    file_list.append(line)
  
    with open(output_filename, 'a') as output_file:
        for line in file_list:
            print(line, file=output_file)
    output_file.close()
    pass


if __name__ == "__main__":
    print("This module is not for direct call!")
