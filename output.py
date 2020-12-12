# coding: utf-8
# license: GPLv3

"""
Module for saving data to special files
"""


def py(a, b, c):
    return (a*a + b*b + c*c)**0.5


def cos_theorem(vec1, vec2):
    scalar = 0
    for i in range(3):
        scalar += vec1[i] * vec2[i]
    print(scalar)
    if scalar < 0:
        return -1
    else:
        return 1


def delete_last_stats(output_filename):
    """Функция удаляет предыдущие значения, записанные в файл output.txt"""
    with open(output_filename, 'w') as output_file:
        print('', file=output_file)


def write_stats_data_to_file(output_filename, body):
    """ Функция сохраняет расстояния и скорости. Строки имеют следующий формат:
    <r>, <V> """
  
    file_list = []
    r = py(body.a, body.b, body.c) * cos_theorem((body.a, body.b, body.c), body.vec_0)
    vel = py(body.Va, body.Vb, body.Vc) * cos_theorem((body.Va, body.Vb, body.Vc), body.vel_0)
    r = '{} '.format(r)
    vel = '{} '.format(vel)
    line = r + vel
    file_list.append(line)
  
    with open(output_filename, 'a') as output_file:
        for line in file_list:
            print(line, file=output_file)
    output_file.close()
