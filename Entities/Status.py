import libtcodpy as libtcod
import copy

status_list = {
    'Rage': {
        'name': 'Rage',
        'color': libtcod.red,
        'damage_bonus' : 5,
        'duration': 100,
    },
    'Blessed': {
        'name': 'Blessed',
        'color': libtcod.yellow,
        'damage_reduction' : '1d5',
        'duration': 100,
    },
    'Poisoned': {
        'name': 'Poisoned',
        'color': libtcod.green,
        'duration': 25,
        'HP': -1
    },
    'Regen': {
        'name': 'Regen',
        'color': libtcod.light_green,
        'duration': 25,
        'HP': 1
    },
    'Haste': {
        'name': 'Haste',
        'color': libtcod.orange,
        'duration': 100,
        'speed': 10
    },
    'Slow': {
        'name': 'Slow',
        'color': libtcod.lighter_blue,
        'duration': 100,
        'speed': -5
    },
}


def new_status(status):
    return copy.deepcopy(status_list[status])


