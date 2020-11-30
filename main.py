# coding: utf-8
# license: GPLv3

"""
Main programme file
"""

from objects import *
from window import *
from model import *

W = Window()
W.root.bind('<Motion>', W.resize)  # это пока для удобства, всё будет работать по-другому
Stop = False
Objects = []


def get_objects():
    b1 = BigBody()
    b1.a = 150
    b1.b = 0
    b1.c = 0
    b1.Va = 0
    b1.Vb = 1
    b1.Vc = 0
    b1.color = "blue"
    
    b2 = BigBody()
    b2.a = -150
    b2.b = 0
    b2.c = 0
    b2.Va = 0
    b2.Vb = -1
    b2.Vc = 0
    b2.color = "green"
    
    b = SmallBody()
    b.a = 0
    b.b = 0
    b.c = 0
    b.Va = 0
    b.Vb = 0
    b.Vc = 2
    
    return [b1, b2, b]


def moving():
    dt = 10
    recalculate_objects_positions(Objects, dt/5)

    for i, body in enumerate(Objects):
        for obj in Objects:
            if obj.type == "smallbody":
                continue
            else:
                obj.x = obj.a
                obj.y = obj.b
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
