from collections import deque
import Queue
import libtcodpy as libtcod
import Render
import Fov

time_travelers = deque()

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
        if Fov.is_visible(obj=obj):
            obj.action_points += obj.speed
            # print time_travelers
            while obj.action_points > 0:
                obj.action_points -= obj.ai.take_turn()
                # print obj.name + ": " + str(obj.action_points)


def add_to_pq(item): # Tuple (priority, item)
    pq.put(item)


def get_next():
    return pq.get()

