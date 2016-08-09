import libtcodpy as libtcod
import random
import Constants


# reference
# http://www.evilscience.co.uk/a-c-algorithm-to-build-roguelike-cave-systems-part-1/

Caves = []
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



rnd = random.seed(123456)
Neighbours = 4
Interations = 50000
CloseCellProb = 45

LowerLimit = 16
UpperLimit = 500

MapSize = (100, 100)

EmptyNeighbours = 3
EmptyCellNeighbours = 4

CorridorSpace = 2
Corridor_MaxTurns = 10
Corridor_min = 2
Corridor_max = 5

pPreventBackTrack = True

break_out = 100000


def build():
    buildCaves()
    getCaves()
    return len(caves)

def get_level_data():
    return level_map


def buildCaves():
    global level_map, Interations
    level_map = [[1 for y in range(Constants.MAP_HEIGHT)]
                 for x in range(Constants.MAP_WIDTH)]

    for x in range(Constants.MAP_WIDTH):
        for y in range(Constants.MAP_HEIGHT):
            if random.randint(0,100) < CloseCellProb:
                level_map[x][y] = 1
            else:
                level_map[x][y] = 0

    for loops in range(Interations):
        cell = random.randint(0, Constants.MAP_WIDTH-1) , random.randint(0, Constants.MAP_HEIGHT-1)

        if get_num_of_closed_neighbours(cell) > Neighbours:
            print "Closed!"
            set_point(cell, 1)
        else:
            print "Open"
            set_point(cell, 0)

    # Smoothing
    for loops in range(5):
        for x in range(Constants.MAP_WIDTH):
            for y in range(Constants.MAP_HEIGHT):
                cell = x, y

                # print get_closed_neighbours(cell)

                if get_point(cell) == 0 and get_closed_neighbours(cell) == EmptyCellNeighbours:
                    set_point(cell, 1)


def getCaves():
    global caves

    for x in range(Constants.MAP_WIDTH):
        for y in range(Constants.MAP_HEIGHT):
            cell = x,y

            if get_point(cell) > 0 and cell not in caves:
                cave = []

                condition = True
                while condition:
                    temp_cell = locateCave(cell, cave)

                    if temp_cell is None:
                        condition = False
                    else:
                        cell = temp_cell

                if LowerLimit <= len(cave) <= UpperLimit:
                    caves.append(cave)
                else:
                    for tile in Caves:
                        set_point(tile, 0)


def caveGetEdge(cave):
    global pCavePoint, pDirection
    while(True):
        pCavePoint = random.choice(cave)
        pDirection = random.choice(directions)

        while(True):
            pCavePoint = pCavePoint[0] + pDirection[0], pCavePoint[1], pDirection[1]

            if not valid_check(pCavePoint):
                break
            else:
                return


def corridorGetEdge():
    global pCavePoint, pDirection, pLocation

    validdirections = []

    condition = True
    while condition:
        pLocation = corridors[random.randint(1, len(corridors) - 1)]

        for dir in directions:
            if valid_check( pLocation[0] + dir[0], pLocation[1], dir[1]  ):
                if get_point(pLocation[0] + dir[0], pLocation[1], dir[1]  ) == 0:
                    validdirections.append(dir)
        condition = len(validdirections) == 0


def connectCaves():
    global caves, corridors, break_out

    if len(caves) == 0:
        return False

    current_cave = random.choice(caves)
    connected_caves = []
    connected_caves.append(current_cave)
    del caves[current_cave]
    potential_corridor = []

    breakouttr = 0

    corridors = []

    while len(caves) > 0:
        if len(corridors) == 0:
            current_cave = random.choice(connected_caves)
            caveGetEdge(current_cave)
        else:
            if random.randint(0,100) > 50:
                current_cave = random.choice(connected_caves)
                caveGetEdge(current_cave)
            else:
                current_cave = None
                corridorGetEdge()

        potential_corridor = corridor_attempt()

        if potential_corridor is not None:
            for c in caves:
                if potential_corridor[-1] in c:
                    if current_cave is None or current_cave != c:
                        potential_corridor.remove(potential_corridor[-1])
                        for tile in potential_corridor:
                            corridors.append(tile)
                            set_point(tile, 1)

                    connected_caves.append(c)
                    del caves[c]
                    break
        breakouttr += 1
        if breakouttr > break_out:
            return False
    for tile in connected_caves:
        caves.append(tile)
    connected_caves = []
    return True





def corridor_attempt():
    global  pDirection
    lPotentialCorridor = []
    lPotentialCorridor.append(pCavePoint)

    corr_length = 0
    pStart = (pDirection[0], pDirection[1])

    pturns = Corridor_MaxTurns

    while pturns >= 0:
        pturns -= 1

        corr_length = random.randint(Corridor_min, Corridor_max)

        while corr_length > 0:
            corr_length -= 1

            pStart =(pStart[0] + pDirection[0], pStart[1] + pDirection[1] )

            if valid_check(pStart) and get_point(pStart) == 1:
                lPotentialCorridor.append(pStart)
                return lPotentialCorridor

            if not valid_check(pStart):
                return None
            elif not corridor_poit_test(pStart, pDirection):
                return None

            lPotentialCorridor.append(pStart)

        if pturns > 1:
            if not pPreventBackTrack:
                pDirection = random.choice(directions)
            else:
                pDirection = random.choice(directions)

    return None


def corridor_poit_test(point, dir):
    coor_list = [x for x in range(-CorridorSpace, CorridorSpace)]

    for r in coor_list:
        if dir[0] == 0:
            if valid_check(point[0] + r, point[1]):
                if get_point(point[0] + r, point[1]) != 0:
                    return False
        elif dir[1] == 0:
            if valid_check(point[0], point[1] + r):
                if get_point(point[0], point[1] + r) != 0:
                    return False

    return True


def locateCave(cell, cave ):
    for tile in get_open_neighbours(cell):
        # print "NOT HERE!"
        if tile not in cave:
            cave.append(tile)
            # locateCave(tile, cave)
            return tile
        return None


def get_point(cell):
    global level_map
    return level_map[cell[0]][cell[1]]

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


def get_closed_neighbours(tile):
    # print get_neightbours(tile)
    new_list = [n for n in get_neighbours(tile) if get_map_value(n) == 1]
    #print new_list
    return new_list

def get_num_of_closed_neighbours(tile):
    # print get_neightbours(tile)
    new_list = [n for n in get_neighbours(tile) if get_map_value(n) == 1]
    print new_list
    return len(new_list)


def get_num_of_open_neighbours(tile):
    new_list = [n for n in get_neighbours(tile) if get_map_value(n) == 0]
    # print new_list
    return len(new_list)


def get_open_neighbours(tile):
    return [n for n in get_neighbours(tile) if get_map_value(n) == 0]


def get_map_value(loc):
    if 0 <= loc[0] < Constants.MAP_WIDTH and 0 <= loc[1] < Constants.MAP_HEIGHT:
        return level_map[loc[0]][loc[1]]



def valid_check(tile):
    if 0 <= tile[0] <= Constants.MAP_WIDTH and 0 <= tile[1] <= Constants.MAP_HEIGHT:
        return True
    return False






