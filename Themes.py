import libtcodpy as libtcod
import random
# DEFAULT

GROUND_CHAR = ['.', ',', ';']
GROUND_COLOR = [libtcod.green, libtcod.light_green, libtcod.dark_green]
GROUND_BCOLOR = None

WALL_CHAR = [libtcod.CHAR_BLOCK1]
WALL_COLOR = [libtcod.grey]
WALL_BCOLOR = None

DOOR_CLOSED_CHAR = ['+']
DOOR_OPEN_CHAR = ['_']
DOOR_COLOR = [libtcod.darkest_yellow]
DOOR_BCOLOR = None

GLASS_CHAR = [libtcod.CHAR_BLOCK1]
GLASS_COLOR = [libtcod.lightest_blue]
GLASS_BCOLOR = None

BOX_CHAR = [libtcod.CHAR_BLOCK1]
BOX_COLOR = [libtcod.lightest_blue]
BOX_BCOLOR = None

OUT_OF_FOV_COLOR = libtcod.darker_gray


def apply_default_theme():
    global GROUND_CHAR, GROUND_COLOR, GROUND_BCOLOR
    global WALL_CHAR, WALL_COLOR, WALL_BCOLOR
    global DOOR_CLOSED_CHAR, DOOR_OPEN_CHAR, DOOR_COLOR, DOOR_BCOLOR
    global GLASS_CHAR, GLASS_COLOR, GLASS_BCOLOR
    global BOX_CHAR, BOX_COLOR, BOX_BCOLOR
    global OUT_OF_FOV_COLOR

    GROUND_CHAR = ['.']
    GROUND_COLOR = [libtcod.white]
    GROUND_BCOLOR = None

    WALL_CHAR = [libtcod.CHAR_BLOCK1]
    WALL_COLOR = [libtcod.grey]
    WALL_BCOLOR = None

    DOOR_CLOSED_CHAR = ['+']
    DOOR_OPEN_CHAR = ['_']
    DOOR_COLOR = [libtcod.darkest_yellow]
    DOOR_BCOLOR = None

    GLASS_CHAR = [libtcod.CHAR_BLOCK1]
    GLASS_COLOR = [libtcod.lightest_blue]
    GLASS_BCOLOR = None

    BOX_CHAR = ['#']
    BOX_COLOR = libtcod.light_orange
    BOX_BCOLOR = None

    OUT_OF_FOV_COLOR = libtcod.darker_gray


def apply_forrest_theme():
    global GROUND_CHAR, GROUND_COLOR, GROUND_BCOLOR
    global WALL_CHAR, WALL_COLOR, WALL_BCOLOR
    global DOOR_CLOSED_CHAR, DOOR_OPEN_CHAR, DOOR_COLOR, DOOR_BCOLOR
    global GLASS_CHAR, GLASS_COLOR, GLASS_BCOLOR
    global BOX_CHAR, BOX_COLOR, BOX_BCOLOR
    global OUT_OF_FOV_COLOR

    GROUND_CHAR = ['.', ',', '"']
    GROUND_COLOR = [libtcod.green, libtcod.light_green, libtcod.dark_green]
    GROUND_BCOLOR = [libtcod.darkest_sepia]

    WALL_CHAR = [libtcod.CHAR_ARROW2_N]
    WALL_COLOR = [libtcod.sepia]
    WALL_BCOLOR = [libtcod.darkest_green]

    DOOR_CLOSED_CHAR = ['X']
    DOOR_OPEN_CHAR = ['|']
    DOOR_COLOR = [libtcod.darkest_yellow]
    DOOR_BCOLOR = [libtcod.dark_sepia]

    GLASS_CHAR = [libtcod.CHAR_BLOCK1]
    GLASS_COLOR = [libtcod.lightest_blue]
    GLASS_BCOLOR = [libtcod.black]

    BOX_CHAR = [libtcod.CHAR_BLOCK1]
    BOX_COLOR = [libtcod.lightest_blue]
    BOX_BCOLOR = [libtcod.black]

    OUT_OF_FOV_COLOR = libtcod.darker_gray


def apply_ssa_theme():
    global GROUND_CHAR, GROUND_COLOR, GROUND_BCOLOR
    global WALL_CHAR, WALL_COLOR, WALL_BCOLOR
    global DOOR_CLOSED_CHAR, DOOR_OPEN_CHAR, DOOR_COLOR, DOOR_BCOLOR
    global GLASS_CHAR, GLASS_COLOR, GLASS_BCOLOR
    global BOX_CHAR, BOX_COLOR, BOX_BCOLOR
    global OUT_OF_FOV_COLOR

    GROUND_CHAR = [libtcod.CHAR_SE]
    GROUND_COLOR = [libtcod.light_grey]
    GROUND_BCOLOR = [libtcod.grey]

    WALL_CHAR = [libtcod.CHAR_CHECKBOX_UNSET]
    WALL_COLOR = [libtcod.darker_flame]
    WALL_BCOLOR = [libtcod.dark_red]

    DOOR_CLOSED_CHAR = ['#']
    DOOR_OPEN_CHAR = ['_']
    DOOR_COLOR = [libtcod.lighter_grey]
    DOOR_BCOLOR = [libtcod.black]

    GLASS_CHAR = [libtcod.CHAR_BLOCK1]
    GLASS_COLOR = [libtcod.lightest_blue]
    GLASS_BCOLOR = [libtcod.black]

    BOX_CHAR = [libtcod.CHAR_BLOCK1]
    BOX_COLOR = [libtcod.lightest_blue]
    BOX_BCOLOR = [libtcod.black]

    OUT_OF_FOV_COLOR = libtcod.darker_gray


def apply_diner_theme():
    global GROUND_CHAR, GROUND_COLOR, GROUND_BCOLOR
    global WALL_CHAR, WALL_COLOR, WALL_BCOLOR
    global DOOR_CLOSED_CHAR, DOOR_OPEN_CHAR, DOOR_COLOR, DOOR_BCOLOR
    global GLASS_CHAR, GLASS_COLOR, GLASS_BCOLOR
    global BOX_CHAR, BOX_COLOR, BOX_BCOLOR
    global OUT_OF_FOV_COLOR

    GROUND_CHAR = [libtcod.CHAR_SUBP_DIAG]
    GROUND_COLOR = [libtcod.lighter_gray]
    GROUND_BCOLOR = [libtcod.black]

    WALL_CHAR = [libtcod.CHAR_BLOCK3]
    WALL_COLOR = [libtcod.red]
    WALL_BCOLOR = [libtcod.black]

    DOOR_CLOSED_CHAR = ['#']
    DOOR_OPEN_CHAR = ['_']
    DOOR_COLOR = [libtcod.lighter_grey]
    DOOR_BCOLOR = [libtcod.black]

    GLASS_CHAR = [libtcod.CHAR_BLOCK1]
    GLASS_COLOR = [libtcod.lightest_blue]
    GLASS_BCOLOR = [libtcod.black]

    BOX_CHAR = [libtcod.CHAR_BLOCK1]
    BOX_COLOR = [libtcod.lightest_blue]
    BOX_BCOLOR = [libtcod.black]

    OUT_OF_FOV_COLOR = libtcod.darker_gray


def ground_char():
    return random.choice(GROUND_CHAR)


def ground_color():
    return random.choice(GROUND_COLOR)


def ground_bcolor():
    return random.choice(GROUND_BCOLOR)


def wall_char():
    return random.choice(WALL_CHAR)

def wall_color():
    return random.choice(WALL_COLOR)

def wall_bcolor():
    return random.choice(WALL_BCOLOR)


def glass_char():
    pass

def glass_color():
    pass

def box_char():
    pass

def box_color():
    pass

apply_ssa_theme()