import libtcodpy as libtcod
import UI

key = libtcod.Key()
mouse = libtcod.Mouse()


def update():
    global key, mouse
    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
    key_char = chr(key.c)

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    if key.lalt and key_char == 'q':
        return UI.Display_MainMenu()


def console_coords():
    global mouse
    return mouse.cx, mouse.cy


