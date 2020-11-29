# coding: utf-8
# license: GPLv3

"""
Visualization module. Describes main screen processes
"""

import ctypes
user32 = ctypes.windll.user32

window_width = round(user32.GetSystemMetrics(0) * 0.8)  # ширина окна - половина ширины экрана
window_height = round(user32.GetSystemMetrics(1) * 0.85)  # высота окна - 0.85 высоты экрана

def create_body_image(space, body):
    x = body.x
    y = body.y
    r = body.R
    body.image = space.create_oval([x - r, y - r], [x + r, y + r], fill=body.color)



def update_object_position(space, body):
    x = body.x
    y = body.y
    r = body.R
    space.coords(body.image, x - r, y - r, x + r, y + r)
    space.update()


if __name__ == "__main__":
    print("This module is not for direct call!")
