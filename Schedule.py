from collections import deque
import Queue
import libtcodpy as libtcod
import Render
import Fov
import Map
import Constants
import GameState
import Pathing

# time_travelers = deque()
time_travelers = []

pq = Queue.PriorityQueue()

player_turn = False


def register(obj):
    global time_travelers
    time_travelers.append(obj)
    obj.action_points = 0


def release(obj):
    global time_travelers
    time_travelers.remove(obj)


def reset():
    global time_travelers
    time_travelers = [GameState.get_player()]


def process():
    global player_turn
    for obj in time_travelers:
        # Render.render_all()
        if obj.delay > 0:
            # print obj.name, obj.delay
            # TODO: create method to handle speed/delay. Allowing for per tick proceesgin (Gasses, etc)
            obj.delay -= obj.speed
        else:
            if obj == GameState.get_player():
                pass
                # Render.render_all()
                # print str(libtcod.sys_get_fps())
            value = 0
            while value == 0:
                # Render.render_all()
                value = obj.ai.take_turn()
                # print "Waiting..."
                if value != 0:
                    obj.delay = value
                    if obj is GameState.get_player():
                        Pathing.BFS(GameState.player)
                        GameState.get_player().pass_time()
