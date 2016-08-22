import libtcodpy as libtcod
import random
import ConfigParser
# DEFAULT


Color = libtcod.Color

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

theme_list = {}

def initialize():
    config = ConfigParser.RawConfigParser()
    config.read('Assets\_themes.list')

    for i in config.sections():
        theme_list[str(i)] = dict(config.items(i))



    print theme_list


def set_theme(theme):
    global GROUND_CHAR, GROUND_COLOR, GROUND_BCOLOR
    global WALL_CHAR, WALL_COLOR, WALL_BCOLOR
    global DOOR_CLOSED_CHAR, DOOR_OPEN_CHAR, DOOR_COLOR, DOOR_BCOLOR
    global GLASS_CHAR, GLASS_COLOR, GLASS_BCOLOR
    global BOX_CHAR, BOX_COLOR, BOX_BCOLOR
    global OUT_OF_FOV_COLOR

    print GROUND_COLOR
    GROUND_CHAR = theme_list[theme]['ground_char'].split(' ')
    GROUND_COLOR = theme_list[theme]['ground_color'].split(' ')
    GROUND_BCOLOR = theme_list[theme]['ground_bcolor'].split(' ')
    print GROUND_COLOR

    WALL_CHAR = theme_list[theme]['wall_char'].split(' ')
    WALL_COLOR = theme_list[theme]['wall_color'].split(' ')
    WALL_BCOLOR = theme_list[theme]['wall_bcolor'].split(' ')

    DOOR_CLOSED_CHAR = theme_list[theme]['door_closed_char'].split(' ')
    DOOR_OPEN_CHAR = theme_list[theme]['door_open_char'].split(' ')
    DOOR_COLOR = theme_list[theme]['door_color'].split(' ')
    DOOR_BCOLOR =theme_list[theme]['door_bcolor'].split(' ')

    GLASS_CHAR = theme_list[theme]['glass_char'].split(' ')
    GLASS_COLOR = theme_list[theme]['glass_color'].split(' ')
    GLASS_BCOLOR = theme_list[theme]['glass_bcolor'].split(' ')

    BOX_CHAR = theme_list[theme]['box_char'].split(' ')
    BOX_COLOR = theme_list[theme]['box_color'].split(' ')
    BOX_BCOLOR = theme_list[theme]['box_bcolor'].split(' ')

    OUT_OF_FOV_COLOR = theme_list[theme]['out_of_fov_color']







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
    GROUND_COLOR = [libtcod.dark_green, libtcod.darker_green, libtcod.darkest_green]
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
    GROUND_COLOR = [libtcod.grey]
    GROUND_BCOLOR = [libtcod.dark_grey]

    WALL_CHAR = [255]
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


def OLD_apply_diner_theme():
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
    color = random.choice(GROUND_COLOR)
    # return color
    return eval(str(color))


def ground_bcolor():
    color = random.choice(GROUND_BCOLOR)
    return eval(str(color))


def wall_char():
    return random.choice(WALL_CHAR)

def wall_color():
    print "C) " + str(WALL_COLOR)
    color = random.choice(WALL_COLOR)
    return eval(str(color))

def wall_bcolor():
    color = random.choice(WALL_BCOLOR)
    return eval(str(color))


def glass_char():
    pass

def glass_color():
    pass

def box_char():
    pass

def box_color():
    pass

apply_ssa_theme()