import GameState

time_travelers = []

"""
Adds Entity to scheduler
"""
def register(obj):
    global time_travelers
    time_travelers.append(obj)
    obj.action_points = 0

11
"""
Removes object from scheduler (ie: death)
"""
def release(obj):
    global time_travelers
    time_travelers.remove(obj)

"""
Resets scheduler to just player
"""
def reset():
    global time_travelers
    time_travelers = [GameState.get_player()]

"""
Cycles through entities and executes their AI.Take_Turn when delay == 0
"""

def process():
    for obj in time_travelers:
        if obj.delay > 0:
            obj.delay -= obj.speed
        else:
            value = 0
            while value == 0:
                value = obj.ai.take_turn()
                if value != 0:
                    obj.delay = value



