# Author: Christian Careaga (christian.careaga7@gmail.com)
# A* Pathfinding in Python (2.7)
# Please give credit if used

from heapq import *
from random import shuffle
import GameState
import Constants


# from Engine import Map


def reset():
    map = GameState.current_level.map_array
    for x in range(Constants.MAP_WIDTH):
        for y in range(Constants.MAP_HEIGHT):
            map[x][y].distance_to_player = -1


def BFS(source):

    map = GameState.current_level.map_array
    x, y = source.x, source.y
    # dest_x, dest_y = dest
    # print "UPDATING BFS!"
    reset()

    visited_tiles = set([])
    tiles_to_proces = []

    tiles_to_proces.append( ((x, y), 0) )

    count = 0

    while tiles_to_proces:
        # print tiles_to_proces
        # print tiles_to_proces[0]
        x, y = tiles_to_proces[0][0]
        dist = tiles_to_proces[0][1]

        if dist > Constants.BFS_MAX_DISTANCE:
            break
        count += 1

        map[x][y].distance_to_player = dist
        visited_tiles.add(tiles_to_proces.pop(0)[0])

        if not GameState.current_level.is_blocked(x + 1, y, True): # RIGHT
            if (x + 1, y) not in visited_tiles:
                visited_tiles.add((x + 1, y))
                tiles_to_proces.append( ((x + 1, y), dist + 1))
        if not GameState.current_level.is_blocked(x - 1, y, True):  # RIGHT
            if (x - 1, y) not in visited_tiles:
                visited_tiles.add((x - 1, y))
                tiles_to_proces.append( ((x - 1, y), dist + 1))
        if not GameState.current_level.is_blocked(x, y + 1, True):  # RIGHT
            if (x , y + 1) not in visited_tiles:
                visited_tiles.add((x, y + 1))
                tiles_to_proces.append( ((x, y + 1), dist + 1))
        if not GameState.current_level.is_blocked(x, y - 1, True):  # RIGHT
            if (x, y - 1) not in visited_tiles:
                visited_tiles.add((x, y - 1))
                tiles_to_proces.append( ((x, y - 1), dist + 1))

        if not GameState.current_level.is_blocked(x + 1, y + 1, True): #
            if (x + 1, y + 1) not in visited_tiles:
                visited_tiles.add((x + 1, y + 1))
                tiles_to_proces.append( ((x + 1, y + 1), dist + 1))
        if not GameState.current_level.is_blocked(x - 1, y - 1, True):  # RIGHT DOWN
            if (x - 1, y - 1) not in visited_tiles:
                visited_tiles.add((x - 1, y - 1))
                tiles_to_proces.append( ((x - 1, y - 1), dist + 1))
        if not GameState.current_level.is_blocked(x - 1, y + 1, True):  # RIGHT
            if (x - 1, y + 1) not in visited_tiles:
                visited_tiles.add((x - 1, y + 1))
                tiles_to_proces.append( ((x - 1, y + 1), dist + 1))
        if not GameState.current_level.is_blocked(x + 1, y - 1, True):  # RIGHT
            if (x + 1, y - 1) not in visited_tiles:
                visited_tiles.add((x + 1, y - 1))
                tiles_to_proces.append( ((x + 1, y - 1), dist + 1))


def heuristic(a, b):
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2


def astar(start, goal, use_fov=True):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    closest_match = []

    heappush(oheap, (fscore[start], start))

    while oheap:

        current = heappop(oheap)[1]
        # print "Heap Length: " + str(len(oheap))

        if current == goal:
            data = []
            while current in came_from:
                #print "adding point..."
                data.append(current)
                current = came_from[current]
            data.reverse()
            #print "Path Found! (" + str(use_fov) + ")"
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < Constants.MAP_WIDTH: # width
                if 0 <= neighbor[1] < Constants.MAP_HEIGHT:  # height
                    if use_fov:
                        if Fov.is_blocked(neighbor): # == 1:6 # map[x][y]
                            continue
                            # print "FOV: {0}, MAP: {1}".format(Fov.is_blocked(neighbor), map[neighbor[0]][neighbor[1]].blocked)
                    else:
                        if Map.is_blocked(neighbor[0], neighbor[1], ignore_mobs=True):  # == 1:6 # map[x][y]
                            continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                closest_match = [current]
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current

                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heappush(oheap, (fscore[neighbor], neighbor))

        if use_fov:
            if len(oheap) > 35:
                #print "Fov Break!"
                oheap = None
                break
        else:
            if len(oheap) > 35:
                #print "Map Break!"
                return False


    second_try = astar(start, goal, use_fov=False)
    print second_try
    if second_try:
        return second_try
    else:
        print "Failed! " + str(use_fov)
        return False


def get_lowest_neighbor(x, y):

    map = GameState.current_level.map_array

    options = []

    """
    Check Neighbors for lowest D-Value
    """
    if not GameState.current_level.is_blocked(x, y - 1) and map[x][y - 1].distance_to_player != -1:
        options.append(((x, y - 1), map[x][y - 1].distance_to_player))
    if not GameState.current_level.is_blocked(x - 1, y) and map[x - 1][y].distance_to_player != -1:
        options.append(((x - 1, y), map[x - 1][y].distance_to_player))
    if not GameState.current_level.is_blocked(x + 1, y) and map[x + 1][y].distance_to_player != -1:
        options.append(((x + 1, y), map[x + 1][y].distance_to_player))
    if not GameState.current_level.is_blocked(x, y + 1) and map[x][y + 1].distance_to_player != -1:
        options.append(((x, y + 1), map[x][y + 1].distance_to_player))

    if not GameState.current_level.is_blocked(x - 1, y - 1) and map[x - 1][y - 1].distance_to_player != -1:
        options.append(((x - 1, y - 1), map[x - 1][y - 1].distance_to_player))
    if not GameState.current_level.is_blocked(x - 1, y + 1) and map[x - 1][y + 1].distance_to_player != -1:
        options.append(((x - 1, y + 1), map[x - 1][y + 1].distance_to_player))
    if not GameState.current_level.is_blocked(x + 1, y - 1) and map[x + 1][y - 1].distance_to_player != -1:
        options.append(((x + 1, y - 1), map[x + 1][y - 1].distance_to_player))
    if not GameState.current_level.is_blocked(x + 1, y + 1) and map[x + 1][y + 1].distance_to_player != -1:
        options.append(((x + 1, y + 1), map[x + 1][y + 1].distance_to_player))

    """
    Randomize results and sort lowest to hieghest. Return lowest Coords.
    """
    shuffle(options)
    print "Options: {0}".format(options)
    options.sort(key=lambda tup: tup[1])

    """
    if no Valud Coords, stay put.
    """
    if options:
        return options[0][0]
    else:
        return (x,y)


def find_path_to_player():
    # Use B-Line to see if area is open.
    # If line is unobstructed, travel that line.
    # this will speed up open area monster navigation, as well as making monster following look better.
    # if line is obstructed, use BFS to determine appriopriate direction
    pass


