import libtcodpy as libtcod
import random
import ConfigParser
# DEFAULT


Color = libtcod.Color

LEVEL_STYLE = ['Fixed']

GROUND_CHAR = [libtcod.CHAR_SUBP_DIAG]
GROUND_COLOR = ['lighter gray']
GROUND_BCOLOR = ['black']

WALL_CHAR = [libtcod.CHAR_BLOCK3]
WALL_COLOR = ['red']
WALL_BCOLOR = ['black']

DOOR_CLOSED_CHAR = [213]
DOOR_OPEN_CHAR = [214]
DOOR_COLOR = ['lighter grey']
DOOR_BCOLOR = ['black']

GLASS_CHAR = [libtcod.CHAR_BLOCK1]
GLASS_COLOR = ['lightest blue']
GLASS_BCOLOR = ['black']

SHROUD_CHAR = [libtcod.CHAR_BLOCK1]
SHROUD_COLOR = ['lightest blue']
SHROUD_BCOLOR = ['black']

OUT_OF_FOV_COLOR = ['darker gray']

theme_list = {}


def initialize():
    config = ConfigParser.RawConfigParser()
    config.read('Assets\_themes.list')

    for i in config.sections():
        theme_list[str(i)] = dict(config.items(i))

    set_theme('Diner')


def set_theme(theme):
    global LEVEL_STYLE
    global GROUND_CHAR, GROUND_COLOR, GROUND_BCOLOR
    global WALL_CHAR, WALL_COLOR, WALL_BCOLOR
    global DOOR_CLOSED_CHAR, DOOR_OPEN_CHAR, DOOR_COLOR, DOOR_BCOLOR
    global GLASS_CHAR, GLASS_COLOR, GLASS_BCOLOR
    global SHROUD_CHAR, SHROUD_COLOR, SHROUD_BCOLOR
    global OUT_OF_FOV_COLOR

    LEVEL_STYLE = theme_list[theme]['level_style'].split(' ')

    GROUND_CHAR = theme_list[theme]['ground_char'].split(' ')
    GROUND_COLOR = theme_list[theme]['ground_color'].split(',')
    GROUND_BCOLOR = theme_list[theme]['ground_bcolor'].split(',')

    WALL_CHAR = theme_list[theme]['wall_char'].split(' ')
    WALL_COLOR = theme_list[theme]['wall_color'].split(',')
    WALL_BCOLOR = theme_list[theme]['wall_bcolor'].split(',')

    DOOR_CLOSED_CHAR = theme_list[theme]['door_closed_char'].split(' ')
    DOOR_OPEN_CHAR = theme_list[theme]['door_open_char'].split(' ')
    DOOR_COLOR = theme_list[theme]['door_color'].split(',')
    DOOR_BCOLOR = theme_list[theme]['door_bcolor'].split(',')

    GLASS_CHAR = theme_list[theme]['glass_char'].split(' ')
    GLASS_COLOR = theme_list[theme]['glass_color'].split(',')
    GLASS_BCOLOR = theme_list[theme]['glass_bcolor'].split(',')

    SHROUD_CHAR = theme_list[theme]['shroud_char'].split(' ')
    SHROUD_COLOR = theme_list[theme]['shroud_color'].split(',')
    SHROUD_BCOLOR = theme_list[theme]['shroud_bcolor'].split(',')

    OUT_OF_FOV_COLOR = theme_list[theme]['out_of_fov_color']


def ground_char():
    return int(random.choice(GROUND_CHAR), 16)


def ground_color():
    print GROUND_COLOR
    color = random.choice(GROUND_COLOR)
    return color


def ground_bcolor():
    color = random.choice(GROUND_BCOLOR)
    # print "Background: {0}".format(color)
    return color


def wall_char():
    return int(random.choice(WALL_CHAR), 16)


def wall_color():
    color = random.choice(WALL_COLOR)
    return color


def wall_bcolor():
    color = random.choice(WALL_BCOLOR)
    return color


def glass_char():
    return eval(str(random.choice(GLASS_CHAR)))


def glass_color():
    color = random.choice(GLASS_COLOR)
    return color


def glass_bcolor():
    color = random.choice(GLASS_BCOLOR)
    return color


def shroud_char():
    return eval(str(random.choice(SHROUD_CHAR)))


def shroud_color():
    color = random.choice(SHROUD_COLOR)
    return color


def shroud_bcolor():
    color = random.choice(SHROUD_BCOLOR)
    return color





