# coding: utf-8
# license: GPLv3

"""
Main programme file
"""

from objects import *
from window import *
from model import *
from output import *

Close = False
Objects = []
Time_counter = 0
P = Point()
W = Window('Sitnikov problem', Objects)


def get_objects():
    b1 = BigBody()
    b1.r = (150, 0, 0)
    b1.V = (0, 1.5, 0)
    b1.color = "blue"
    b1.vec_0 = b1.r
    b1.vel_0 = b1.V
    
    b2 = BigBody()
    b2.r = (-150, 0, 0)
    b2.V = (0, -1.5, 0)
    b2.color = "green"
    b2.vec_0 = b2.r
    b2.vel_0 = b2.V
    
    b = SmallBody()
    b.r = (0, 0, 0)
    b.V = (0, 0, 2)
    b.vec_0 = (0, 0, 1)
    b.vel_0 = b.V
    
    return [b1, b2, b]


def moving():
    global Time_counter
    Time_counter += 1
    recalculate_objects_positions(Objects, W.dt/200)
    if Time_counter % 50 == 0:
        Time_counter = 0
        W.l_panel.show_info(W)

    if Time_counter % 5 == 0:
        write_stats_data_to_file('output1.txt', Objects[1])
        write_stats_data_to_file('output2.txt', Objects[2])

    for i, body in enumerate(Objects):
        update_object_position(W, body)
        W.space.update()

    if W.process:
        W.space.after(101 - W.dt, moving)
    pass


def close(event):
    global Close
    W.process = False
    Close = True
    pass


def push(event):
    W.push(event)
    for i in range(len(Objects)):
        if Objects[i].push(event):
            W.l_panel.info = Objects[i]
            break
    if W.process:
        W.l_panel.show_info(W)
        moving()
    pass


def main():
    global Objects

    print('Modelling started!')

    Objects = get_objects()
    W.o = Objects
    delete_last_stats('output1.txt')
    delete_last_stats('output2.txt')
    for i in (0, 1):  # images of bodies b1 and b2
        create_body_image(W, Objects[i])
        update_object_position(W, Objects[i])

    create_body_image(W, Objects[2])  # image of body

    if W.l_panel.info == 0:
        W.l_panel.info = Objects[2]

    W.space.bind("<Configure>", W.resize)
    W.root.bind("<space>", W.repaint)
    W.space.bind("<Button-1>", push)
    W.root.bind("<Destroy>", close)

    if W.process:
        moving()

    if not Close:
        W.root.mainloop()
    print('Modelling finished!')
    return


if __name__ == "__main__":
    main()



