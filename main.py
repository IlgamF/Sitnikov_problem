# coding: utf-8
# license: GPLv3

"""
Main programme file
"""

from objects import *
from window import *
from model_Oxy import *

Stop = False
Space = []
Objects = []


def get_objects():
    b1 = BigBody()
    b1.x = 150
    b1.Vy = 1.5
    b1.color = "blue"
    
    b2 = BigBody()
    b2.x = -150
    b2.Vy = -1.5
    b2.color = "green"
    
    b = SmallBody()
    b.Vz = 2
    
    return [b1, b2, b]


def moving():
    dt = 1
    recalculate_objects_positions(Objects, dt)
    for i, body in enumerate(Objects):
        update_object_position(Space, body)

    if not Stop:
        Space.after(101 - dt, moving)
    pass


def main():
    global Space, Objects

    print('Modelling started!')

    w = Window()

    Objects = get_objects()
    Space = w.space

    for i in (0, 1):  # images of bodies b1 and b2
        create_body_image(w.space, Objects[i])
        update_object_position(w.space, Objects[i])

    create_body_image(w.space, Objects[2])  # image of body b

    w.root.bind("<Space>", w.repaint())
     
    moving()
    
    w.root.mainloop()
    print('Modelling finished!')
    return


if __name__ == "__main__":
    main()

