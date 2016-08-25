from collections import deque
import Queue
import libtcodpy as libtcod
import Render
import Fov
import Map
import Constants
import GameState

# time_travelers = deque()
time_travelers = []

pq = Queue.PriorityQueue()


def register(obj):
    time_travelers.append(obj)
    obj.action_points = 0


def release(obj):
    time_travelers.remove(obj)


def tick():
    if len(time_travelers) > 0:
        obj = time_travelers[0]
        time_travelers.rotate()

        if obj.action_points <= 0:
            print obj.name + " - " + str(obj.action_points)
            obj.action_points += obj.speed

        if obj in Map.get_visible_objects():
            # print time_travelers
            while obj.action_points > 0:
                obj.action_points -= obj.ai.take_turn()
                print "turn"
                # print obj.name + ": " + str(obj.action_points)

def alt_tick():
    if len(time_travelers) > 0:
        obj = time_travelers[0]
        result = obj.ai.take_turn()
        if result != 0:
            obj.action_points -= result
            time_travelers.sort(key=lambda x: x.action_points, reverse=True)
           # for obj in time_travelers:
                #print obj.name + " | " + str(obj.action_points)


def all_at_once():
    for obj in time_travelers:
        if obj.delay > 0:
            # print obj.name, obj.delay
            obj.delay -= obj.speed
        else:

            obj.delay = obj.ai.take_turn()


    # time_travelers.sort(key=lambda x: x.delay, reverse=False)




def add_to_pq(item): # Tuple (priority, item)
    pq.put(item)


def get_next():
    return pq.get()

