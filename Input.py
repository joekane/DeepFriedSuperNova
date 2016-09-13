import libtcodpy as libtcod
import UI

key = libtcod.Key()
mouse = libtcod.Mouse()


def update():
    global key, mouse
    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    if key.vk == libtcod.KEY_ESCAPE or key.vk == libtcod.KEY_ESCAPE or key.vk == libtcod.KEY_SPACE:
        return UI.Display_MainMenu()




