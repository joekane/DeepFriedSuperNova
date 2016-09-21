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

player_turn = False


def register(obj):
    time_travelers.append(obj)
    obj.action_points = 0


def release(obj):
    time_travelers.remove(obj)


def process():
    global player_turn
    if player_turn:

        Render.render_all()
        value = GameState.get_player().ai.take_turn()
        if value != 0:
            print "Player Turn"
            GameState.get_player().pass_time()
            player_turn = False
    else:
        for obj in time_travelers:
            if obj.delay > 0:
                # print obj.name, obj.delay
                # TODO: create method to handle speed/delay. Allowing for per tick proceesgin (Gasses, etc)
                obj.delay -= obj.speed
            else:

                value = obj.ai.take_turn()
                if value == 0:
                    player_turn = True
                else:

                    obj.delay = value
                    player_turn = False


    # time_travelers.sort(key=lambda x: x.delay, reverse=False)
