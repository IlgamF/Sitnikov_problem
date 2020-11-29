# coding: utf-8
# license: GPLv3

"""
Main programme file
"""

import tkinter
from tkinter.filedialog import *
from objects import *
from window import *

import ctypes
user32 = ctypes.windll.user32

window_width = round(user32.GetSystemMetrics(0) * 0.8)  # ширина окна - половина ширины экрана
window_height = round(user32.GetSystemMetrics(1) * 0.85)  # высота окна - 0.85 высоты экрана

objects = []
space = []

B1 = Big_body()
B1.x = 100
B2 = Big_body()
B2.x = -100

objects.append(B1)
objects.append(B2)

def main():
    print('Modelling started!')
    
    root = tkinter.Tk()
    space = tkinter.Canvas(root, width=window_width, height=window_height, bg="white")
    space.pack(side=tkinter.TOP)
    space.configure(scrollregion=(-window_width/2,-window_height/2, window_width/2, window_height/2))
    space.xview_moveto(.5)
    space.yview_moveto(.5)

    
    create_body_image(space, B1)
    update_object_position(space, B1)
    create_body_image(space, B2)
    update_object_position(space, B2)
    
    root.mainloop()
    print('Modelling finished!')

if __name__ == "__main__":
    main()

