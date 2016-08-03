import libtcodpy as libtcod
import Utils
import time
import Render

def follow_line(source, target):

    line = Utils.get_line((source.x, source.y), (target.x, target.y))

    for loc in line:
        x, y = loc

        if (x, y) == line[-1]:
            libtcod.console_put_char_ex(0, x, y, '*', libtcod.dark_amber, libtcod.BKGND_NONE)
        else:
            libtcod.console_put_char_ex(0, x, y, '-', libtcod.dark_amber, libtcod.BKGND_NONE)

        libtcod.console_flush()
        time.sleep(0.0025)
        Render.map()
        Render.objects()
        Render.ui()
        Render.update()

