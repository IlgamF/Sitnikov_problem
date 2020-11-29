# coding: utf-8
# license: GPLv3

"""
Main programme file
"""

import tkinter
from tkinter.filedialog import *  # это что такое?
from objects import *
from window import *

import ctypes

Objects = []  # space objects
Space = []  # canvas
Root = []  # window


'''
это странный ход. лучше задать b1 и b2 в отдельной функции, а потом добавить их в массив objects,
чтобы не делать лишних глобальных переменных. Тогда b1 и b2 можно будет вызвать, как
objects[0] и objects[1] 
'''

B1 = BigBody()
B1.x = 100
B2 = BigBody()
B2.x = -100

Objects.append(B1)
Objects.append(B2)


def create_window():
    global Root, Space

    Root = tkinter.Tk()  # create window
    Root.title('Sitnikov problem')  # window top-left title
    Root.resizable = True
    Root.minsize = (window_width, window_height)  # minimal window width

    Space = tkinter.Canvas(Root, width=window_width, height=window_height, bg="white")
    Space.pack(side=tkinter.TOP)
    Space.configure(scrollregion=(-window_width / 2, -window_height / 2, window_width / 2, window_height / 2))
    Space.xview_moveto(.5)
    Space.yview_moveto(.5)

    return


def main():
    print('Modelling started!')

    create_window()

    create_body_image(Space, B1)
    update_object_position(Space, B1)
    create_body_image(Space, B2)
    update_object_position(Space, B2)
    
    Root.mainloop()
    print('Modelling finished!')


if __name__ == "__main__":
    main()

