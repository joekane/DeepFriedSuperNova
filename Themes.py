import libtcodpy as libtcod
import random
# DEFAULT

GROUND_CHAR = ['.', ',', ';']
GROUND_COLOR = [libtcod.green, libtcod.light_green, libtcod.dark_green]

WALL_CHAR = [libtcod.CHAR_BLOCK1]
WALL_COLOR = [libtcod.grey]

DOOR_CLOSED_CHAR = ['+']
DOOR_OPEN_CHAR = ['_']
DOOR_COLOR = [libtcod.darkest_yellow]

GLASS_CHAR = [libtcod.CHAR_BLOCK1]
GLASS_COLOR = [libtcod.lightest_blue]

BOX_CHAR = [libtcod.CHAR_BLOCK1]
BOX_COLOR = [libtcod.lightest_blue]

OUT_OF_FOV_COLOR = libtcod.dark_gray


def apply_default_theme():
    global GROUND_CHAR, GROUND_COLOR
    global WALL_CHAR, WALL_COLOR
    global DOOR_CLOSED_CHAR, DOOR_OPEN_CHAR, DOOR_COLOR
    global GLASS_CHAR, GLASS_COLOR
    global BOX_CHAR, BOX_COLOR
    global OUT_OF_FOV_COLOR

    GROUND_CHAR = ['.']
    GROUND_COLOR = [libtcod.white]

    WALL_CHAR = [libtcod.CHAR_BLOCK1]
    WALL_COLOR = [libtcod.grey]

    DOOR_CLOSED_CHAR = ['+']
    DOOR_OPEN_CHAR = ['_']
    DOOR_COLOR = [libtcod.darkest_yellow]

    GLASS_CHAR = [libtcod.CHAR_BLOCK1]
    GLASS_COLOR = [libtcod.lightest_blue]

    BOX_CHAR = ['#']
    BOX_COLOR = libtcod.light_orange
    OUT_OF_FOV_COLOR = libtcod.dark_gray


def apply_forrest_theme():
    global GROUND_CHAR, GROUND_COLOR
    global WALL_CHAR, WALL_COLOR
    global DOOR_CLOSED_CHAR, DOOR_OPEN_CHAR, DOOR_COLOR
    global GLASS_CHAR, GLASS_COLOR
    global BOX_CHAR, BOX_COLOR
    global OUT_OF_FOV_COLOR

    GROUND_CHAR = ['.', ',', ';']
    GROUND_COLOR = [libtcod.green, libtcod.light_green, libtcod.dark_green]

    WALL_CHAR = [libtcod.CHAR_ARROW2_N]
    WALL_COLOR = [libtcod.darker_sepia]

    DOOR_CLOSED_CHAR = ['X']
    DOOR_OPEN_CHAR = ['|']
    DOOR_COLOR = [libtcod.darkest_yellow]

    GLASS_CHAR = [libtcod.CHAR_BLOCK1]
    GLASS_COLOR = [libtcod.lightest_blue]

    BOX_CHAR = [libtcod.CHAR_BLOCK1]
    BOX_COLOR = [libtcod.lightest_blue]

    OUT_OF_FOV_COLOR = libtcod.dark_gray



def apply_ssa_theme():
    global GROUND_CHAR, GROUND_COLOR
    global WALL_CHAR, WALL_COLOR
    global DOOR_CLOSED_CHAR, DOOR_OPEN_CHAR, DOOR_COLOR
    global GLASS_CHAR, GLASS_COLOR
    global BOX_CHAR, BOX_COLOR
    global OUT_OF_FOV_COLOR

    GROUND_CHAR = [libtcod.CHAR_CHECKBOX_UNSET]
    GROUND_COLOR = [libtcod.white]

    WALL_CHAR = [libtcod.CHAR_BLOCK3]
    WALL_COLOR = [libtcod.darker_red]

    DOOR_CLOSED_CHAR = ['#']
    DOOR_OPEN_CHAR = ['_']
    DOOR_COLOR = [libtcod.lighter_grey]

    GLASS_CHAR = [libtcod.CHAR_BLOCK1]
    GLASS_COLOR = [libtcod.lightest_blue]

    BOX_CHAR = [libtcod.CHAR_BLOCK1]
    BOX_COLOR = [libtcod.lightest_blue]

    OUT_OF_FOV_COLOR = libtcod.dark_gray


def ground_char():
    return random.choice(GROUND_CHAR)


def ground_color():
    return random.choice(GROUND_COLOR)

def wall_char():
    pass

def wall_color():
    pass

def glass_char():
    pass

def glass_color():
    pass

def box_char():
    pass

def box_color():
    pass

apply_ssa_theme()