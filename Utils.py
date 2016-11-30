# *******************************************************
# * Copyright (C) 2016-2017 Joe Kane
# *
# * This file is part of 'Deep Fried Supernova"
# *
# * Deep Fried Supernova can not be copied and/or distributed without the express
# * permission of Joe Kane
# *******************************************************/


import math
import Constants
import GameState
import libtcodpy as libtcod
import Map
import Fov
import time
import Animate
import Render
import re
from bearlibterminal import terminal
from timeit import default_timer as timer

map_old_x = 0
map_old_y = 0
delay = 0
new_animation = True


def remove_tags(text):
    return re.sub('<[^>]*>', '', text)


def get_tags(text):
    return re.findall("[<].*?[>]", text)


def message(new_msg, color=libtcod.white):
    import textwrap
    # split the message if necessary, among multiple lines
    new_msg_lines = textwrap.wrap(new_msg, Constants.MSG_WIDTH)

    for line in new_msg_lines:
        # if the buffer is full, remove the first line to make room for the new one
        if len(GameState.get_msg_queue()) == Constants.MSG_HEIGHT:
            GameState.del_msg(0)

        # add the new line as a tuple, with the text and the color
        GameState.add_msg(line, color)


def distance_to(self, other):
    # return the distance to another object
    dx = other.x - self.x
    dy = other.y - self.y
    return math.sqrt(dx ** 2 + dy ** 2)


def get_drunk_line(start, end):
    pass


def get_line(start, end, walkable=False, ignore_mobs=False, max_length=99999):

    if start == (None, None) or end == (None, None):
        return []

    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        if  Map.is_blocked(coord[0], coord[1], ignore_mobs) and walkable is True:
            points.append((None, None))
            #max_length += 1
        else:
            points.append(coord)

        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx


    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    # points.remove(start)
    # print points, max_length
    return points[0:max_length+1]


def distance_between(x1, y1, x2, y2):
    # return the distance to another object
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx ** 2 + dy ** 2)


def get_names_under_mouse():
    import Fov
    mouse = libtcod.Mouse()
    # return a string with the names of all objects under the mouse
    (x, y) = (mouse.cx, mouse.cy)
    # create a list with the names of all objects at the mouse's coordinates and in FOV
    names = [obj.name for obj in Map.get_all_objects()
             if obj.x == x and obj.y == y and Fov.is_visible(obj=obj)]
    names = ', '.join(names)  # join the names, separated by commas
    return names.capitalize()


def get_fighters_under_mouse():
    import Fov
    mouse = libtcod.Mouse()
    # return a string with the names of all objects under the mouse
    (x, y) = (mouse.cx, mouse.cy)
    # create a list with the names of all objects at the mouse's coordinates and in FOV
    fighters = [obj for obj in Map.get_all_objects()
                if obj.x == x and obj.y == y and Fov.is_visible(obj)]

    return fighters


def from_dungeon_level(table):
    # returns a value that depends on level. the table specifies what value occaurs after each level, default is 0.
    for (value, level) in reversed(table):
        # print "V: " + str(value) + " |L: " + str(level) + "   DL: " + str(dungeon_level)
        if GameState.dungeon_level >= int(level):
            return int(value)
    return 0


def random_choice_index(chances):  # choose one option from list of chances, returning its index
    # the dice will land on some number between 1 and the sum of the chances
    # print chances
    dice = libtcod.random_get_int(0, 1, sum(chances))

    # go through all chances, keeping the sum so far
    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w

        # see if the dice landed in the part that corresponds to this choice
        if dice <= running_sum:
            return choice
        choice += 1


def random_choice(chances_dict):
    # choose one option from dictionary of chances, returning its key
    chances = chances_dict.values()
    strings = chances_dict.keys()
    # print chances
    return strings[random_choice_index(chances)]


def inspect_tile(x, y):
    global delay, map_old_x, map_old_y, new_animation

    if 0 < x < Constants.MAP_CONSOLE_WIDTH and 0 < y < Constants.MAP_CONSOLE_HEIGHT:
        # Mouse over Inspection

        camera_x, camera_y = Map.get_camera()
        map_x, map_y = (camera_x + x, camera_y + y)

        if map_x is map_old_x and map_y is map_old_y:
            if time.time() - delay > Constants.INSPECTION_DELAY:
                # Post-Delay

                if Map.level_map[map_x][map_y].explored:
                    obj = [obj for obj in Map.get_all_objects() if obj.x == map_x and obj.y == map_y]
                    if len(obj) == 0:
                        pass
                    else:
                        # print "animating..."
                        #TODO: FIX animation calls
                        #Animate.inspect_banner(x, y, obj[0].name, new_animation)
                        new_animation = False
            else:
                # Pre-Delay
                pass
        else:
            # 88Render.clear_animations()
            new_animation = True
            map_old_x = map_x
            map_old_y = map_y
            delay = time.time()


def find_path(source, target):
    fov_map = libtcod.map_new(Constants.MAP_WIDTH, Constants.MAP_HEIGHT)
    for y in range(Constants.MAP_HEIGHT):
        for x in range(Constants.MAP_WIDTH):
            libtcod.map_set_properties(fov_map, x, y, True, True)

    path = libtcod.path_new_using_map(fov_map, 1.5)
    libtcod.path_compute(path, source[0], source[1], target[0], target[1])
    return path


def connected_cells(source, target):

    my_path = libtcod.path_new_using_map(Fov.get_fov_map(), 1.41)

    libtcod.path_compute(my_path, source[0], source[1], target[0], target[1])

    if not libtcod.path_is_empty(my_path):
        return True
    else:
        return False


def is_mouse_in(con_x, con_y, width, height):
    import Input
    mouse = Input.mouse

    # print mouse.cx, mouse.cy, " -> ", con_x, con_y

    if con_x <= mouse.cx <= con_x + width - 1 and con_y <= mouse.cy <= con_y + height - 1:
        return True
    else:
        return False


def get_circle_points(x0, y0, radius, ring=False, size=2):
    if x0 is not None and y0 is not None:
        if ring:
            x = radius - size + 1
        else:
            x = 0
        y = 0
        err = 0

        points = []

        start_x = x

        while start_x <= radius:
            x = start_x
            y = 0
            while x >= y:
                points.append((x0 + x, y0 + y))
                points.append((x0 + y, y0 + x))
                points.append((x0 - y, y0 + x))
                points.append((x0 - x, y0 + y))
                points.append((x0 - x, y0 - y))
                points.append((x0 - y, y0 - x))
                points.append((x0 + y, y0 - x))
                points.append((x0 + x, y0 - y))

                y += 1
                err += 1 + 2 * y
                if 2 * (err - x) + 1 > 0:
                    x -= 1
                    err += 1 - 2 * x
            start_x += 1

        #return points
        return list(set(points))
    return False


def find_element_in_list(element, list_element):
    try:
        index_element = list_element.index(element)
        return index_element
    except ValueError:
        return None


def convert_color(color, alpha=255):

    if type(color) is libtcod.Color:
        return terminal.color_from_argb(alpha, color[0], color[1], color[2])
    else:
        return color


def profile(some_function):
    import time

    def wrapper():
        startA = timer()
        #print("Something is happening before some_function() is called.")

        some_function()
        startB = timer()

        print("{0} Took {1} secs to execute".format(some_function, startB - startA))

    return wrapper


def clear_layer(layer, color='black'):
    terminal.bkcolor(color)
    terminal.layer(layer)
    terminal.clear_area(0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)


def get_unicode(code):
    # print "Code: {0}".format(code)

    look_up = {
        '176': 0x2591,
        '177': 0x2592,
        '178': 0x2593,
        '179': 0x2502,
        '180': 0x2524,
        '181': 0x2561,
        '182': 0x2562,
        '183': 0x2556,
        '184': 0x2555,
        '185': 0x2563,
        '186': 0x2551,
        '187': 0x2557,
        '188': 0x255D,
        '189': 0x255C,
        '190': 0x255B,
        '191': 0x2510,

        '192': 0x2514,
        '193': 0x2534,
        '194': 0x252C,
        '195': 0x251C,
        '196': 0x2500,
        '197': 0x253C,
        '198': 0x255E,
        '199': 0x255F,
        '200': 0x255A,
        '201': 0x2554,
        '202': 0x2569,
        '203': 0x2566,
        '204': 0x2560,
        '205': 0x2550,
        '206': 0x256C,
        '207': 0x2567,

        '208': 0x2568,
        '209': 0x2564,
        '210': 0x2565,
        '211': 0x2559,
        '212': 0x2558,
        '213': 0x2552,
        '214': 0x2553,
        '215': 0x256B,
        '216': 0x256A,
        '217': 0x2518,
        '218': 0x250C,
        '219': 0x2588,
        '220': 0x2584,
        '221': 0x258C,
        '222': 0x2590,
        '223': 0x2580,

        '224': 0x03B1,
        '225': 0x00DF,
        '226': 0x0393,
        '227': 0x03C0,
        '228': 0x03A3,
        '229': 0x03C3,
        '230': 0x00B5,
        '231': 0x03C4,
        '232': 0x03A6,
        '233': 0x0398,
        '234': 0x03A9,
        '235': 0x03B4,
        '236': 0x221E,
        '237': 0x03C6,
        '238': 0x03B5,
        '239': 0x2229,

        '240': 0x2261,
        '241': 0x00B1,
        '242': 0x2265,
        '243': 0x2264,
        '244': 0x2320,
        '245': 0x2321,
        '246': 0x00F7,
        '247': 0x2248,
        '248': 0x00B0,
        '249': 0x2219,
        '250': 0x00B7,
        '251': 0x221A,
        '252': 0x207F,
        '253': 0x00B2,
        '254': 0x25A0,
        '255': 0x00A0

    }

    if str(code) in look_up.keys():
        return look_up[str(code)]
    else:
        return code
