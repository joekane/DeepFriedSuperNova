import GameState


class Scheduler:
    def __init__(self):
        self.time_travelers = []

    """
    Adds Entity to scheduler
    """
    def register(self, obj):
        self.time_travelers.append(obj)
        obj.action_points = 0


    """
    Removes object from scheduler (ie: death)
    """
    def release(self, obj):
        self.time_travelers.remove(obj)

    """
    Resets scheduler to just player
    """
    def reset(self):
        self.time_travelers = [GameState.get_player()]

    """
    Cycles through entities and executes their AI.Take_Turn when delay == 0
    """
    def process(self):
        for obj in self.time_travelers:
            if obj.delay > 0:
                obj.delay -= obj.speed
            else:
                value = 0
                while value == 0:
                    value = obj.ai.take_turn()
                    if value != 0:
                        obj.delay = value



