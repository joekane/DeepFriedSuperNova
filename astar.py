# Author: Christian Careaga (christian.careaga7@gmail.com)
# A* Pathfinding in Python (2.7)
# Please give credit if used

import Fov
import Map
import Constants
from heapq import *


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

