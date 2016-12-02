import sys
import heapq
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import math


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.room_list = []
        self.num_vertices = 0
        self.num_rooms = 0
        self.previous = None

    def __iter__(self):
        return iter(self.room_list)
        # return iter(self.vert_dict.values())

    def add_room(self, room, id):
        self.num_rooms += 1
        room.id = id
        self.room_list.append(room)
        return room

    def add_room_edge(self, frm, to, cost=0):
        if frm not in self.room_list:
            self.add_room(frm)
        if to not in self.room_list:
            self.add_room(to)
        # print "Room edge!"
        frm.add_neighbor(to, cost)
        to.add_neighbor(frm, cost)

    def set_previous(self, current):
        self.previous = current

    def get_previous(self):
        return self.previous


def shortest(v, path):
    # make shortest path from v.previous
    if v.previous:
        path.append(v.previous.center())
        shortest(v.previous, path)
    return


def calculate_all_paths(aGraph, start):
    # print '''Dijkstra's shortest path'''
    # Set the distance for the start node to zero
    start.set_distance(0)

    # Put tuple pair into the priority queue
    # print "Graph:"
    # print
    unvisited_queue = [(v.get_distance(), v)for v in aGraph]
    heapq.heapify(unvisited_queue)

    # print "UV:"
    # print unvisited_queue

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        # for next in v.adjacent:
        for next in current.adjacent:
            # if visited, skip
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)

            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(), v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)



def get_triangles(list):

    x, y = [item.center()[0] for item in list], [item.center()[1] for item in list]
    triang = tri.Triangulation(x, y)
    '''
    # GRAPH OUTPUT
    plt.figure()
    plt.gca().set_aspect('equal')
    graph = plt.gca()
    plt.triplot(triang, 'bo-')
    plt.title('triplot of Delaunay triangulation')

    graph.invert_yaxis()

    plt.show()
    '''
    return triang.triangles
