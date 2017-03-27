class Event(object):
    def __init__(self, ID, params):
        self.ID = ID
        self.params = params


def is_blocked(position):
    return Event('is_blocked', {'position': position, 'blocked': False, 'target': ''})


def input(key, mouse):
    return Event('input', {'key': key, 'mouse': mouse, 'status': None})

def AI():
    return Event('AI', {})



def draw(type):
    if type == 'map':
        return Event('draw_map', {'layer': 0})
    if type == 'objects':
        return Event('draw_objects', {'layer': 2, 'position': (-1, -1), 'glyph': None, 'color': None})


def render_map(id):
    return Event('render_map', {'id': id, 'layer': 0})


def attack(target):
    return Event('attack', {'power': 0, 'type': '', 'target': target})


def take_damage(power, type):
    return Event('take_damage', {'power': power, 'type': type})


def search(pos, owner):
    return Event('search', {'position': pos, 'owner': owner})


def position():
    return Event('position', {'position': (-1, -1)})


def death():
    return Event('death', {'type': ''})


def add_item(item):
    return Event('add_item', {'item': item, 'result': False})


def remove_item(item):
    return Event('remove_item', {'item': item, 'result': False})


def contents():
    return Event('contents', {'contents': None, 'space': None})


def equip():
    return Event('equip', {'item': None, 'contents': None})


def move(actor, direction):
    return Event('move', {'actor': actor, 'direction': direction})


def move_to(pos):
    return Event('move_to', {'move_to': pos})










