# *******************************************************
# * Copyright (C) 2016-2017 Joe Kane
# *
# * This file is part of 'Deep Fried Supernova"
# *
# * Deep Fried Supernova can not be copied and/or distributed without the express
# * permission of Joe Kane
# *******************************************************/


import random
import sys

import Constants
import Utils
import libtcodpy as libtcod

sys.setrecursionlimit((Constants.MAP_WIDTH * Constants.MAP_HEIGHT))

# reference
# http://www.evilscience.co.uk/a-c-algorithm-to-build-roguelike-cave-systems-part-1/

# Caves = []
Corridors = []

level_map = [[]]

directions = [
    (0, -1),
    (0, 1),
    (1, 0),
    (-1, 0)
]

full_directions = [
    (0, -1),
    (0, 1),
    (1, 0),
    (-1, 0),
    (1, -1),
    (-1, -1),
    (-1, 1),
    (1, 1)
]

caves = []
corridors = []
pCavePoint = None
pDirection = None
pLocation = None

recur_count = 0
recur_max = 900


# rnd = random.seed(666)
Neighbours = 4  # Openess 3 or 4
Interations = 15000   #

CloseCellProb = 55  # Lower Number (45) = Open, Higher = Constricted (75)
CloseCellRange = 10 # variabliity

Smoothing = 50

LowerLimit = 16
UpperLimit = 500

EmptyNeighbours = 3
EmptyCellNeighbours = 4

CorridorSpace = 2
Corridor_MaxTurns = 10
Corridor_min = 2
Corridor_max = 5

pPreventBackTrack = True

break_out = 100000


def build(map=None):

    build_caves(map)
    getCaves()
    connectCaves_new()
    return


def get_level_data():
    return level_map


def build_caves(map):
    global level_map, Interations

    if map is None:
        level_map = [[1 for y in range(Constants.MAP_HEIGHT)]
                     for x in range(Constants.MAP_WIDTH)]
    else:
        level_map = map

    for x in range(1, Constants.MAP_WIDTH-2):
        for y in range(1, Constants.MAP_HEIGHT-2):
            cell = x, y
            if random.randint(0, 100) < random.randint(CloseCellProb, CloseCellProb + CloseCellRange):
                set_point(cell, 1)
            else:
                set_point(cell, 0)

    for loops in range(Interations):
        cell = random.randint(1, Constants.MAP_WIDTH - 3), random.randint(1, Constants.MAP_HEIGHT - 3)

        neighbors = get_full_closed_neighbours(cell)
        # print neighbors
        if len(neighbors) > Neighbours:
            # print "Closed!"
            set_point(cell, 1)
        else:
            # print "Open"
            set_point(cell, 0)


    # Smoothing
    for loops in range(Smoothing):
        for x in range(Constants.MAP_WIDTH):
            for y in range(Constants.MAP_HEIGHT):
                cell = x, y

                # print get_closed_neighbours(cell)

                if get_point(cell) == 1 and len(get_open_neighbours(cell)) >= EmptyNeighbours:
                    # print "Smoothing......."
                    set_point(cell, 0)

    for x in range(1, Constants.MAP_WIDTH-1):
        for y in range(1, Constants.MAP_HEIGHT-1):
            cell = x, y

            if get_point(cell) == 0 and len(get_closed_neighbours(cell)) >= EmptyCellNeighbours:
                    # print "Smoothing......."
                    set_point(cell, 1)

def point_in_cave_check(cell):
    global caves

    # print cell
    # print caves

    for cave in caves:
        if cell in cave:
            return True
    # print "Not in cave"
    return False

def getCaves():
    global caves, recur_count

    for x in range(Constants.MAP_WIDTH):
        for y in range(Constants.MAP_HEIGHT):
            cell = x, y

            # IF CELL IS OPEN
            if get_point(cell) == 0:
                # IF CELL IS NOT IN EXISITNG CAVE FLOOD FILL
                if not point_in_cave_check(cell):
                    cave = []
                    floodfill(cell, cave)
                    if LowerLimit <= len(cave) <= UpperLimit:
                        caves.append(cave)


def floodfill(cell, cave, fill=4):
    global level_map

    # print "Cell: " + str(cell)
    x, y = cell

    # assume surface is a 2D image and surface[x][y] is the color at x, y.
    if level_map[x][y] == 1: # the base case
        return
    if level_map[x][y] == fill: # the base case
        return
    if 0 < x < Constants.MAP_WIDTH-1 and 0 < y < Constants.MAP_HEIGHT - 1:
        cave.append(cell)
        level_map[x][y] = fill
        floodfill( (x + 1, y), cave) # right
        floodfill( (x - 1, y), cave) # left
        floodfill((x, y + 1), cave)
        floodfill((x, y - 1), cave) # up



def connected_points(source, target):
    x, y = source

    if source == target:
        return True
    # assume surface is a 2D image and surface[x][y] is the color at x, y.
    if level_map[x][y] == 1:  # the base case
        return False
    connected_points((x + 1, y), target)
    connected_points((x - 1, y), target)
    connected_points((x, y + 1), target)
    connected_points((x, y - 1), target)



def caveXGetEdge(cave):
    global pCavePoint, pDirection, pCave
    while True:
        pCavePoint = random.choice(cave)
        pDirection = random.choice(directions)

        while True:
            pCavePoint = offset(pCavePoint, pDirection)

            if not valid_check(pCavePoint):
                break
            elif get_point(pCavePoint) == 0:
                return


def corridorXGetEdge():
    global pDirection, pLocation

    validdirections = []

    condition = True
    while condition:
        pLocation = corridors[random.randint(1, len(corridors) - 1)]

        for dir in directions:
            if valid_check( offset(pLocation, dir)):
                if get_point(offset(pLocation, dir)) == 0:
                    validdirections.append(dir)
        condition = len(validdirections) == 0

    pDirection = random.choice(validdirections)
    pLocation = offset(pLocation, pDirection)


def connectCaves_new():
    global caves

    connected_caves = []

    while len(caves) > 1:

        # if len(connected_caves) == 0:
        current_cave = caves[0]
        del caves[caves.index(current_cave)]
        target_cave = caves[0]

        if Utils.connected_cells(current_cave[0], target_cave[0]):
            pass
        else:
            print "added connection...."
            connect_two_caves(current_cave, target_cave )




def connect_two_caves(cave1, cave2):

    prev_x, prev_y = random.choice(cave1)
    new_x, new_y = random.choice(cave2)

    if libtcod.random_get_int(0, 0, 1) == 1:
        # first move horizontally, then vertically
        create_h_tunnel(prev_x, new_x, prev_y)
        create_v_tunnel(prev_y, new_y, new_x)
    else:
        # first move vertically, then horizontally
        create_v_tunnel(prev_y, new_y, prev_x)
        create_h_tunnel(prev_x, new_x, new_y)




def create_v_tunnel(y1, y2, x):
    global level_map
    # vertical tunnel
    for y in range(min(y1, y2), max(y1, y2) + 1):
        set_point( (x, y), 2)

def create_h_tunnel(x1, x2, y):
    global level_map
    for x in range(min(x1, x2), max(x1, x2) + 1):
        set_point( (x, y), 2)





def connectCaves():
    global caves, corridors, break_out

    if len(caves) == 0:
        return False

    current_cave = random.choice(caves)
    connected_caves = []
    connected_caves.append(current_cave)

    # if current_cave in caves:
    #    print "Cave in Caves!"
    del caves[caves.index(current_cave)]
    # if current_cave not in caves:
    #    print "Cave removed from Caves!"



    potential_corridor = []

    breakouttr = 0

    corridors = []

    while len(caves) > 0:
        if len(corridors) == 0:
            #print "Cors = 0"
            current_cave = random.choice(connected_caves)
            print "# of Connected Caves: " + str(len(connected_caves))
            print "# of Caves:           " + str(len(caves))
            caveGetEdge(current_cave)
        else:
            # print "Cors != 0"
            if random.randint(0,100) > 50:
                print "from cave"
                current_cave = random.choice(connected_caves)
                caveGetEdge(current_cave)
            else:
                print "from coor"
                current_cave = None
                corridorGetEdge()


        potential_corridor = corridor_attempt()
        # print "pot:"
        # print potential_corridor




        if potential_corridor is not None:
            # print "PotCor!!!!"
            for c in caves:
                if potential_corridor[-1] in c:
                    # print potential_corridor
                    # if current_cave is None or current_cave != c:
                    # print potential_corridor
                    potential_corridor.remove(potential_corridor[-1])
                    # print potential_corridor
                    for tile in potential_corridor:
                        print "Append!"
                        corridors.append(tile)
                        set_point(tile, 0)

                    connected_caves.append(c)
                    # print connected_caves
                    del caves[caves.index(c)]
                    break
        breakouttr += 1
        if breakouttr > break_out:
            print "BREAK!!!!"
            return False
    for tile in connected_caves:
        caves.append(tile)
    connected_caves = []
    return True


def corridor_attempt():
    global pDirection
    lPotentialCorridor = []
    lPotentialCorridor.append(pCavePoint)

    corr_length = 0
    startdirection = (pDirection[0], pDirection[1])
    pStart = offset(pCavePoint, (0,0) )

    pturns = Corridor_MaxTurns

    while pturns >= 0:
        pturns -= 1

        corr_length = random.randint(Corridor_min, Corridor_max)

        while corr_length > 0:
            corr_length -= 1

            pStart = offset(pStart, pDirection)
            # print pStart

            if valid_check(pStart) and get_point(pStart) == 1:
                lPotentialCorridor.append(pStart)
                return lPotentialCorridor

            if not valid_check(pStart):
                return None
            elif not corridor_point_test(pStart, pDirection):
                return None

            lPotentialCorridor.append(pStart)

        if pturns > 1:
            if not pPreventBackTrack:
                pass
            else:
                pDirection = random.choice(directions)

    return None


def corridor_point_test(point, dir):
    coor_list = [x for x in range(-CorridorSpace, CorridorSpace)]

    for r in coor_list:
        if dir[0] == 0:
            if valid_check(  (point[0] + r, point[1]) ):
                if get_point( (point[0] + r, point[1] )) != 0:
                    return False
        elif dir[1] == 0:
            if valid_check(  (point[0], point[1] + r) ):
                if get_point( (point[0], point[1] + r)   ) != 0:
                    return False
    return True


def locateCave(cell, cave):
    global recur_count

    if recur_count >= recur_max:
        return None, cave
    else:
        recur_count += 1
        for tile in get_open_neighbours(cell):
            # print "NOT HERE!"
            if tile not in cave:
                cave.append(tile)
                # locateCave(tile, cave)
                locateCave(tile, cave)
    return None, cave


def get_point(loc):
    global level_map
    if 0 <= loc[0] < Constants.MAP_WIDTH and 0 <= loc[1] < Constants.MAP_HEIGHT:
        return level_map[loc[0]][loc[1]]


def set_point(cell, value):
    global level_map
    # print cell
    level_map[cell[0]][cell[1]] = value


def offset(tile, offset):
    import operator
    # print tile
    # print offset
    new_tup = tuple(map(operator.add, tile, offset))
    return new_tup


def get_neighbours(tile):
    return [offset(tile, dir) for dir in directions if valid_check(offset(tile, dir))]


def get_all_neighbours(tile):
    return [offset(tile, dir) for dir in full_directions if valid_check(offset(tile, dir))]


def get_closed_neighbours(tile):
    # print get_neightbours(tile)
    new_list = [n for n in get_neighbours(tile) if get_point(n) == 1]
    #print new_list
    return new_list


def get_full_closed_neighbours(tile):
    # print get_all_neighbours(tile)
    new_list = [n for n in get_all_neighbours(tile) if get_point(n) == 1]
    #print new_list
    return new_list


def get_num_of_closed_neighbours(tile):
    # print get_neightbours(tile)
    neighbour_list = get_neighbours(tile)
    # print neighbour_list

    count = 0
    for cell in neighbour_list:
        # print cell
        # print get_map_value(cell)
        if get_point(cell) == 1:
            count += 1
    # print count
    return count
    #
    # new_list = [n for n in neighbour_list if get_map_value(n) == 1]
    # print new_list
    # return len(new_list)


def get_num_of_open_neighbours(tile):
    new_list = [n for n in get_neighbours(tile) if get_point(n) == 0]
    # print new_list
    return len(new_list)


def get_open_neighbours(tile):
    return [n for n in get_neighbours(tile) if get_point(n) == 0]


def valid_check(tile):
    if 0 <= tile[0] <= Constants.MAP_WIDTH and 0 <= tile[1] <= Constants.MAP_HEIGHT:
        return True
    return False






