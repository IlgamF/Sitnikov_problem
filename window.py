# coding: utf-8
# license: GPLv3

"""
Visualization module. Describes main screen processes
"""

import ctypes
from items import *
from graphics import *


views = [['Oxy', 3*np.pi/2, np.pi, 'off'],  # surface Oxy
         ['Oxz', 3*np.pi/2, 'off', np.pi],  # surface Oxz
         ['Oyz', 'off', 3*np.pi/2, np.pi],  # surface Oyz
         ['Xyz', np.pi/4, 3*np.pi/2, np.pi],  # x looks at us and surface Oyz
         ['Yxz', 3*np.pi/2, np.pi/4, np.pi],  # y looks at us and surface Oxz
         ['Zxy', 3*np.pi/2, np.pi, np.pi/4],  # Z looks at us and surface Oxy
         ['XYz', np.pi/3, 5*np.pi/3, np.pi]]  # X, Y look at us and axis Z - up
"""
special global list with different types of views.
[View name, Angle between X axis and vertical line(VL), that looks down, btw. Y and VL, btw Z and VL]
if Angle == 'off', it means that axis is not drawn on canvas                                                     
"""


class Window:
    """
    Window class: carries parameters needed to build a window with all the buttons and axes and bodies, etc.
    """
    def __init__(self, title, o):
        user32 = ctypes.windll.user32
        self.in_w = round(user32.GetSystemMetrics(0) / 16 * 10.8)  # Initial window width
        self.in_h = round(user32.GetSystemMetrics(1) / 9 * 8.1)  # Initial window height

        self.root = Tk()  # Create window
        self.root.geometry('%ix%i' % (self.in_w, self.in_h))  # initial window size
        self.root.title(title)  # Window top-left title

        self.light = 0  # Defines color of canvas (black or white)
        self.colours = ('#262a2e', '#dcecf5')  # Window colours: (dark, light)

        self.dt = 0.5  # Time interval

        self.initial = [[(100, 0, 0), (0, 2, 0)], [(-100, 0, 0), (0, -2, 0)], [(0, 0, 0), (0, 0, 2)]]
        # Initial parameters of three bodies

        # Main canvas
        self.space = Canvas(self.root, bg=self.colours[self.light])
        self.space.pack(side=TOP, fill="both", expand=True)
        self.space.configure(scrollregion=(-self.in_w / 2, -self.in_h / 2, self.in_w / 2, self.in_h / 2))
        self.space.xview_moveto(.5)
        self.space.yview_moveto(.5)

        self.process = False  # Flag of process

        self.view = 0  # Number of view in views
        self.axes_alive = [True, True, False]  # Declares initial axis conditions [x: on, y:on, z: off]
        self.axes = Axis(self)  # axes drawn on canvas
        self.angles = [(0, 0), (0, 0), (0, 0)]  # Declares zero axis conditions
        self.reorganize_axes()

        self.buttons = self.init_buttons()  # Left-Bottom buttons panel

        self.l_panel = LeftPanel(self)  # Left-Top information panel
        self.r_panel = RightPanel(self)  # Right panel with buttons

        self.additional = 0  # Defines new windows
        self.objects = o  # contains Objects from main
        pass

    def init_buttons(self):
        """
        Initializes buttons
        :return: [RoundButton1, ..., RoundButton6]
        """
        buttons = []
        for i in (1, 2, 3, 4, -2, -1):
            but = RoundButton(self.space, self.in_w, self.in_h, i)
            buttons.append(but)
        return buttons

    def resize(self, event):
        """
        Changes all the coordinates when user changes window-size
        :param event: <Configure>
        :return:
        """
        w, h = self.root.winfo_width(), self.root.winfo_height()

        self.space.configure(scrollregion=(- w / 2, - h / 2, w / 2, h / 2))

        for i in range(len(self.buttons)):
            self.buttons[i].resize(self.space)

        self.axes.resize(self)

        self.r_panel.resize(self)

        self.in_w, self.in_h = w, h
        pass

    def repaint(self):
        """
        Repaints all the elements when user clicks 'Repaint' button
        :return:
        """
        self.light = abs(self.light - 1)

        self.space.configure(bg=self.colours[self.light])

        for i in self.buttons:
            i.repaint(self)
        self.buttons[5].change_img(self)

        self.axes.repaint(self)
        pass

    def reorganize_axes(self):
        """
        Reorganizes axes positions when user changes the view
        :return:
        """
        view = views[self.view]
        self.axes_alive = [True, True, True]
        self.angles = [(0, 0), (0, 0), (0, 0)]
        for i in range(len(view)):
            if i == 0:
                continue
            if view[i] == 'off':  # Switches off the axis, if it is not used
                self.axes_alive[i - 1] = False
                self.angles[i - 1] = (0, 0)
            else:
                phi = view[i]
                self.angles[i-1] = (np.sin(phi), np.cos(phi))
        self.axes.redraw(self)
        pass

    def push(self, event):
        """
        Gives reaction on pushing left-bottom buttons panel
        :param event: <Button-1>
        :return:
        """
        a = 0
        for i in self.buttons:
            a += i.push(event)
        if a == 1:
            self.additional = InfoWindow('Теоретическое описание', 'teor.txt')
            self.additional.file_reading('teor.txt')
            self.process = False
        if a == 2:
            self.process = False
            self.buttons[5].change_img(self)
            draw_graph(self.objects, ('output1.txt', 'output2.txt'))
        if a == 3:
            self.additional = InfoWindow('Информация о программе', 'info.txt')
            self.additional.file_reading('info.txt')
            self.process = False
        if a == 4:
            self.additional = InfoWindow('Помощь', 'help.txt')
            self.additional.file_reading('help.txt')
            self.process = False
        if a == 5:
            self.view = (self.view + 1) % len(views)
            self.reorganize_axes()
        if a == 6:
            self.process = not self.process
        if a != 0:
            self.buttons[5].change_img(self)  # Changes image of 'play' button
        pass


class InfoWindow:
    """
    Information Window class
    """
    def __init__(self, title, filename):
        user32 = ctypes.windll.user32
        self.in_w = round(user32.GetSystemMetrics(0) / 16 * 6)  # Window width
        if filename == 'teor.txt':
            self.in_h = round(user32.GetSystemMetrics(1) / 9 * 8)
        elif filename == 'info.txt':
            self.in_h = round(user32.GetSystemMetrics(1) / 9 * 3)
        else:
            self.in_h = round(user32.GetSystemMetrics(1) / 9 * 4.5)  # Window height

        self.close = False  # If the window exists, this parameter is False

        self.root = Tk()  # Create window
        self.root.geometry('%ix%i' % (self.in_w, self.in_h))
        self.root.title(title)  # Window top-left title
        
        self.space = Canvas(self.root, bg='white')  # Canvas to print on it
        self.space.pack(side=TOP, fill="both", expand=True)
        self.space.configure(scrollregion=(-self.in_w / 2, -self.in_h / 2,
                                           self.in_w / 2, self.in_h / 2))

        pass

    def file_reading(self, filename):
        """
        Places text on the canvas
        :param filename: 'filename.txt' <- from this file text for windows is taken
        :return:
        """
        inp = open(filename, 'r', encoding='utf-8')
        s = inp.readlines()
        for i in range(len(s)):
            st = Label(self.root, text=s[i], font="TimesNewRoman 12", bg="white", fg="black")
            st.place(x=50, y=5+20*i)
        pass


def reorganize_coordinates(w, body):
    """
    Reorganises coordinates from (x, y, z) axis to (X, Y) - window coordinates
    :param w: Window
    :param body: BigBody or SmallBody from Objects: [b1, b2, b]
    :return:
    """
    axes, angles = w.axes_alive, w.angles
    phi_x, phi_y, phi_z = angles[0], angles[1], angles[2]
    da, db, dc = (0, 0), (0, 0), (0, 0)

    if axes[0]:  # if x exists
        da = (-body.r[0] * phi_x[0], body.r[0] * phi_x[1])
    if axes[1]:
        db = (-body.r[1] * phi_y[0], body.r[1] * phi_y[1])
    if axes[2]:
        dc = (-body.r[2] * phi_z[0], body.r[2] * phi_z[1])
    body.x, body.y = da[0] + db[0] + dc[0], da[1] + db[1] + dc[1]
    pass


def create_body_image(w, body):
    """
    Creates body image
    :param w: Window
    :param body: BigBody or SmallBody from Objects: [b1, b2, b]
    :return:
    """
    reorganize_coordinates(w, body)
    body.image = w.space.create_oval([body.x - body.R, body.y - body.R],
                                     [body.x + body.R, body.y + body.R],
                                     fill=body.color)
    pass


def update_object_position(w, body):
    """
    Updates body positions on the canvas
    :param w: Window
    :param body: BigBody or SmallBody from Objects: [b1, b2, b]
    :return:
    """
    reorganize_coordinates(w, body)
    w.space.coords(body.image,
                   body.x - body.R, body.y - body.R,
                   body.x + body.R, body.y + body.R)
    w.space.update()
    pass


if __name__ == "__main__":
    print("This module is not for direct call!")
