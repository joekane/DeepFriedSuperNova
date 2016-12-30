import libtcodpy as libtcod
import UI
from bearlibterminal import terminal



class Mouse:
    def __init__(self):
        self.lreleased = True
        self.lbutton_used = False
        pass

    def lused(self):
        self.lbutton_used = True

    @property
    def cx(self):
        return terminal.state(terminal.TK_MOUSE_X)

    @property
    def cy(self):
        return terminal.state(terminal.TK_MOUSE_Y)

    @property
    def lbutton_pressed(self):
        if key == terminal.TK_MOUSE_LEFT:
            return True
        else:
            return False

    @property
    def rbutton_pressed(self):
        if key == terminal.TK_MOUSE_RIGHT:
            return True
        else:
            return False

    @property
    def lbutton(self):
        return bool(terminal.state(terminal.TK_MOUSE_LEFT))

    @property
    def rbutton(self):
        return bool(terminal.state(terminal.TK_MOUSE_RIGHT))


key = None
mouse = Mouse()


def update():
    global key
    if terminal.has_input():
        key = terminal.read()
    else:
        key = None


def read_key_chr():
    return terminal.state(terminal.TK_CHAR)


def console_coords():
    global mouse
    return mouse.cx, mouse.cy


def clear():
    while terminal.has_input():
        terminal.read()




