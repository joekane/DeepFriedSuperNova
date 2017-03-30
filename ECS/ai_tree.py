from enum import Enum


class TaskStatus(Enum):
    WAITING = 0
    FAILURE = 1
    SUCCESS = 2
    RUNNING = 3


class Task(object):
    def __init__(self, name, *args, **kwargs ):
        self.name = name
        self.children = []
        self.function = kwargs.get('function')

    def run(self):
        if self.function:
            self.function()

        return TaskStatus.SUCCESS


class Selector(Task):
    """
        A selector runs each task in order until one succeeds,
        at which point it returns SUCCESS. If all tasks fail, a FAILURE
        status is returned.  If a subtask is still RUNNING, then a RUNNING
        status is returned and processing continues until either SUCCESS
        or FAILURE is returned from the subtask.
    """

    def __init__(self, name, *args, **kwargs):
        super(Selector, self).__init__(name, *args, **kwargs)

    def run(self):
        for c in self.children:
            status = c.run()

            if status != TaskStatus.FAILURE:
                return status

        return TaskStatus.FAILURE


class Sequence(Task):
    """
        A sequence runs each task in order until one fails,
        at which point it returns FAILURE. If all tasks succeed, a SUCCESS
        status is returned.  If a subtask is still RUNNING, then a RUNNING
        status is returned and processing continues until either SUCCESS
        or FAILURE is returned from the subtask.
    """

    def __init__(self, name, *args, **kwargs):
        super(Sequence, self).__init__(name, *args, **kwargs)

    def run(self):
        for c in self.children:
            status = c.run()

            if status != TaskStatus.SUCCESS:
                return status

        return TaskStatus.SUCCESS


