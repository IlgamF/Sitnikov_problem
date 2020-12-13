# coding: utf-8
# license: GPLv3

"""
Main programme file
"""

from objects import *
from window import *
from model import *
from output import *
from numpy import *

Close = False
"""
Application-destroyer flag
"""

Objects = []
"""
List of bodies [b1, b2, b]
"""

Time_counter = 0
"""
Counter of renewing data
"""

W = Window('Sitnikov problem', Objects)



def get_objects():
    """
    Defines three bodies: b1 and b2 - with greater mass, b - width a small one
    :return: list of three bodies [b1, b2, b]
    """
    b1 = BigBody()
    b1.r = W.initial[0][0]  # initial coordinates (x, y, z)
    b1.V = W.initial[0][1]  # initial velocity (Vx, Vy, Vz)
    b1.color = "blue"
    b1.vec_0 = b1.r  # initial radius-vector
    b1.vel_0 = b1.V  # initial velocity-vector
    
    b2 = BigBody()
    b2.r = W.initial[1][0]
    b2.V = W.initial[1][1]
    b2.color = "green"
    b2.vec_0 = b2.r
    b2.vel_0 = b2.V
    
    b = SmallBody()
    b.r = W.initial[2][0]
    b.V = W.initial[2][1]
    b.vec_0 = (0, 0, 1)
    b.vel_0 = b.V
    
    return [b1, b2, b]


def moving():
    """
    Allows bodies to move
    :return:
    """
    global Time_counter
    Time_counter += 1
    recalculate_objects_positions(Objects, W.dt/2)
    if Time_counter % round((50 * sqrt(W.dt))) == 0:
        Time_counter = 0
        W.l_panel.show_info(W)

    data = W.r_panel.data
    W.dt = data[0]
    for i in range(len(Objects)):
        Objects[i].m = data[i + 1]

    if W.r_panel.renew_parameter:
        W.r_panel.renew_parameter = False
        for i in range(len(Objects)):
            Objects[i].r = W.initial[i][0]
            Objects[i].V = W.initial[i][1]
            delete_last_stats('output1.txt'), delete_last_stats('output2.txt')

    if Time_counter % round((5 * sqrt(W.dt))) == 0:
        write_stats_data_to_file('output1.txt', Objects[1])
        write_stats_data_to_file('output2.txt', Objects[2])

    for i, body in enumerate(Objects):
        update_object_position(W, body)
        W.space.update()

    if W.process:
        W.space.after(1, moving)
    pass


def close(event):
    """
    Changes parameters to destroy the window
    :param event: <Destroy>
    :return:
    """
    global Close
    W.process = False
    Close = True
    pass


def push(event):
    """
    Reaction to left-button click
    :param event: <Button-1>
    :return:
    """
    W.push(event)
    for i in range(len(Objects)):
        if Objects[i].push(event):
            W.l_panel.info = Objects[i]  # renew information on the left panel with another mass
            break
    if W.process:
        moving()  # if "play" was clicked -> continue
    W.l_panel.show_info(W)  # renew information on the left panel in case of stopping the programme
    W.space.update()
    pass


def main():
    """
    Main function of the programme
    :return:
    """
    global Objects

    # obj = ImageTk.PhotoImage(file='slowfast.png')
    # W.space.create_image(100, 100, anchor=NW, image=obj)

    print('Modelling started!')

    Objects = get_objects()
    W.objects = Objects
    delete_last_stats('output1.txt')
    delete_last_stats('output2.txt')
    for i in (0, 1):  # images of bodies b1 and b2
        create_body_image(W, Objects[i])
        update_object_position(W, Objects[i])

    create_body_image(W, Objects[2])  # image of body

    if W.l_panel.info == 0:
        W.l_panel.info = Objects[2]

    W.l_panel.show_info(W)

    W.space.bind("<Configure>", W.resize)
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
