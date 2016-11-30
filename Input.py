import libtcodpy as libtcod
import UI
from bearlibterminal import terminal




def update_OLD():
    global key, mouse

    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
    key_char = chr(key.c)

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    if key.lalt and key_char == 'q':
        return UI.Display_MainMenu()


def read_key_int():
    # while terminal.has_input():

    if terminal.has_input():
        return terminal.read()
    return None

    # return None


def read_key_chr():
    return terminal.state(terminal.TK_CHAR)


def console_coords():
    global mouse
    return mouse.cx, mouse.cy


def clear():
    while terminal.has_input():
        terminal.read()



class Mouse:
    def __init__(self):
        pass

    @property
    def cx(self):
        return terminal.state(terminal.TK_MOUSE_X)

    @property
    def cy(self):
        return terminal.state(terminal.TK_MOUSE_Y)

    @property
    def lbutton_pressed(self):
        return bool(terminal.state(terminal.TK_MOUSE_LEFT))

    @property
    def rbutton_pressed(self):
        return bool(terminal.state(terminal.TK_MOUSE_RIGHT))

    @property
    def lbutton(self):
        return bool(terminal.state(terminal.TK_MOUSE_LEFT))

    @property
    def rbutton(self):
        return bool(terminal.state(terminal.TK_MOUSE_RIGHT))



# key = libtcod.Key()

# mouse = libtcod.Mouse()

key = terminal.read()
mouse = Mouse()

