import libtcodpy as libtcod
import Utils
import time
import Render


def follow_line(source, target, projectile='-', end_tile='*', color=libtcod.dark_amber):

    line = Utils.get_line((source.x, source.y), (target.x, target.y))

    for loc in line:
        x, y = loc

        Render.render_all()

        if (x, y) == line[-1]:
            libtcod.console_put_char_ex(0, x, y, end_tile, color, libtcod.BKGND_NONE)
        else:
            libtcod.console_put_char_ex(0, x, y, projectile, color, libtcod.BKGND_NONE)

        libtcod.console_flush()
        time.sleep(0.0025)


def explosion(target, radius=3):
    for r in range(0, radius):
        Render.render_all()
        if r >= 0:
            libtcod.console_put_char_ex(0, target.x, target.y, 'X', libtcod.red, libtcod.BKGND_NONE)
            print "1"
        if r >= 1:
            libtcod.console_put_char_ex(0, target.x-1, target.y, 'X', libtcod.red, libtcod.BKGND_NONE)
            libtcod.console_put_char_ex(0, target.x+1, target.y, 'X', libtcod.red, libtcod.BKGND_NONE)
            libtcod.console_put_char_ex(0, target.x, target.y-1, 'X', libtcod.red, libtcod.BKGND_NONE)
            libtcod.console_put_char_ex(0, target.x, target.y+1, 'X', libtcod.red, libtcod.BKGND_NONE)
            print "2"
        if r >= 2:
            libtcod.console_put_char_ex(0, target.x - 2, target.y, 'X', libtcod.red, libtcod.BKGND_NONE)
            libtcod.console_put_char_ex(0, target.x + 2, target.y, 'X', libtcod.red, libtcod.BKGND_NONE)
            libtcod.console_put_char_ex(0, target.x, target.y - 2, 'X', libtcod.red, libtcod.BKGND_NONE)
            libtcod.console_put_char_ex(0, target.x, target.y + 2, 'X', libtcod.red, libtcod.BKGND_NONE)

            libtcod.console_put_char_ex(0, target.x+1, target.y + 1, 'X', libtcod.red, libtcod.BKGND_NONE)
            libtcod.console_put_char_ex(0, target.x-1, target.y + 1, 'X', libtcod.red, libtcod.BKGND_NONE)
            libtcod.console_put_char_ex(0, target.x+1, target.y - 1, 'X', libtcod.red, libtcod.BKGND_NONE)
            libtcod.console_put_char_ex(0, target.x-1, target.y - 1, 'X', libtcod.red, libtcod.BKGND_NONE)
            print "3"
        libtcod.console_flush()
        print "sleep"
        time.sleep(0.025)


def inspect_banner(x, y, banner_text):
    color = libtcod.light_blue
    libtcod.console_set_default_foreground(0, libtcod.lighter_blue)
    length = len(banner_text)

    libtcod.console_put_char_ex(0, x + 1, y, libtcod.CHAR_HLINE, color, libtcod.BKGND_NONE)

    libtcod.console_put_char_ex(0, x + 2, y - 1, libtcod.CHAR_NW, color, libtcod.BKGND_NONE)
    libtcod.console_put_char_ex(0, x + 2, y, libtcod.CHAR_TEEW, color, libtcod.BKGND_NONE)
    libtcod.console_put_char_ex(0, x + 2, y + 1, libtcod.CHAR_SW, color, libtcod.BKGND_NONE)

    libtcod.console_put_char_ex(0, x + 3 + length, y - 1, libtcod.CHAR_NE, color, libtcod.BKGND_NONE)
    libtcod.console_put_char_ex(0, x + 3 + length, y, libtcod.CHAR_VLINE, color, libtcod.BKGND_NONE)
    libtcod.console_put_char_ex(0, x + 3 + length, y + 1, libtcod.CHAR_SE, color, libtcod.BKGND_NONE)

    for z in range(length):
        libtcod.console_put_char_ex(0, x + z + 3, y - 1, libtcod.CHAR_HLINE, color, libtcod.BKGND_NONE)
        libtcod.console_put_char_ex(0, x + z + 3, y + 1, libtcod.CHAR_HLINE, color, libtcod.BKGND_NONE)

    libtcod.console_print_ex(0, x + 3, y, libtcod.BKGND_NONE, libtcod.LEFT, banner_text)
