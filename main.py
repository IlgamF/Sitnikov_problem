# coding: utf-8
# license: GPLv3

"""
Main programme file
"""

from objects import *
from window import *
from model_Oxy import *

W = Window()
Stop = False
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
    dt = 10
    recalculate_objects_positions(Objects, dt/5)
    for i, body in enumerate(Objects):
        update_object_position(W.space, body)
        W.space.update()

    W.space.after(101 - dt, moving)
    pass


def close(event):
    global Stop
    Stop = True
    return


def main():
    global Objects

    print('Modelling started!')

    Objects = get_objects()

    for i in (0, 1):  # images of bodies b1 and b2
        create_body_image(W.space, Objects[i])
        update_object_position(W.space, Objects[i])

    create_body_image(W.space, Objects[2])  # image of body b

    W.init_buttons()

    W.space.bind("<Configure>", W.resize)
    W.root.bind("<space>", W.repaint)
    W.root.bind("<Destroy>", close)
     
    moving()
    if not Stop:
        W.root.mainloop()
    print('Modelling finished!')
    return


if __name__ == "__main__":
    main()
