# coding: utf-8
# license: GPLv3

"""
Main programme file
"""

import tkinter
from tkinter.filedialog import *
from objects import *
from window import *
from model_Oxy import *


def get_objects():
    b1 = BigBody()
    b1.x = 150
    b1.Vy = 1
    b1.color = "blue"
    
    b2 = BigBody()
    b2.x = -150
    b2.Vy = -1
    b2.color = "green"
    
    b = SmallBody()
    b.Vz = 2
    
    return [b1, b2, b]


def moving(space, objects):
    dt = 1
    recalculate_objects_positions(objects, dt)
    for i, body in enumerate(objects):
        update_object_position(space, body)
    space.after(101 - dt, moving(space, objects))


def main():

    print('Modelling started!')

    w = Window()

    objects = get_objects()

    for i in (0, 1):  # images of bodies b1 and b2
        create_body_image(w.space, objects[i])
        update_object_position(w.space, objects[i])

    create_body_image(w.space, objects[2])  # image of body b
     
    moving(w.space, objects)
    
    w.root.mainloop()
    print('Modelling finished!')


if __name__ == "__main__":
    main()

