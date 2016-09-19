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

map_old_x = 0
map_old_y = 0
delay = 0
new_animation = True


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


def get_line(start, end):

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
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    points.remove(start)
    return points


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
    print chances
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
                        Animate.inspect_banner(x, y, obj[0].name, new_animation)
                        new_animation = False
            else:
                # Pre-Delay
                pass
        else:
            Render.clear_animations()
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


    if con_x <= mouse.cx <= con_x + width - 1 and con_y <= mouse.cy <= con_y + height - 1:
        return True
    else:
        return False


def get_circle_points(x0, y0, radius, ring=False, size=2):
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
