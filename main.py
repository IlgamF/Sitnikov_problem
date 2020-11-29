# coding: utf-8
# license: GPLv3

"""

Main programme file
"""

import tkinter
from tkinter.filedialog import *  # это что такое? Пока эта штука не используется, но в будущем понадобится
from objects import *
from window import *
from model_Oxz import *
"""пока что менять ракурс можно, меняя импортируемый в этой строке модуль, это надо переделать"""

import ctypes

Objects = []  # space objects
Space = []  # canvas
Root = []  # window

one_button = []
two_button = []



'''
это странный ход. лучше задать b1 и b2 в отдельной функции, а потом добавить их в массив objects,
чтобы не делать лишних глобальных переменных. Тогда b1 и b2 можно будет вызвать, как
objects[0] и objects[1]

'''

B1 = BigBody()
B1.x = 100
B1.Vy = 1
B1.color = "blue"

B2 = BigBody()
B2.x = -100
B2.Vy = -1
B2.color = "green"

b = SmallBody()       
b.Vy = 2

Objects.append(B1)
Objects.append(B2)
Objects.append(b)

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

def moving():
    recalculate_objects_positions(Objects, dt)
    for i, body in enumerate(Objects):
        update_object_position(Space, body)
    Space.after(101 - dt, moving)

def main():

    print('Modelling started!')

    create_window()

    create_body_image(Space, B1)
    update_object_position(Space, B1)
    create_body_image(Space, B2)
    update_object_position(Space, B2)
    create_body_image(Space, b)
     
    moving()
    
    Root.mainloop()
    print('Modelling finished!')


if __name__ == "__main__":
    main()

