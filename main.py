# coding: utf-8
# license: GPLv3

"""
Main programme file
"""

from objects import *
from window import *
from model import *

Stop = False
Objects = []
P = Point()
W = Window('Sitnikov problem', Objects)

def get_objects():
    b1 = BigBody()
    b1.a = 150
    b1.Vb = 1.5
    b1.color = "blue"
    
    b2 = BigBody()
    b2.a = -150
    b2.Vb = -1.5
    b2.color = "green"
    
    b = SmallBody()
    b.Vc = 2
    
    return [b1, b2, b]


def moving():
    dt = 100
    recalculate_objects_positions(Objects, dt/400)

    for i, body in enumerate(Objects):
        for obj in Objects:
            if obj.type == "smallbody":
                continue
            else:
                obj.x = obj.a
                obj.y = obj.b
            # P.draw_point(Objects, W)
        update_object_position(W, body)
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
    W.o = Objects
    
    for i in (0, 1):  # images of bodies b1 and b2
        create_body_image(W, Objects[i])
        update_object_position(W, Objects[i])

    create_body_image(W, Objects[2])  # image of body

    moving()

    W.space.bind("<Configure>", W.resize)
    W.root.bind("<space>", W.repaint)
    W.space.bind("<Button-1>", W.push)
    W.root.bind("<Destroy>", close)

    if not Stop:
        W.root.mainloop()
    print('Modelling finished!')
    return


if __name__ == "__main__":
    main()



