prefabs = {
    'Room': ('basic_room', (9, 9)),
    'LRoom': ('large_room', (18, 18)),
    'Test': ('test_room', (9, 9)),
    '+hall': ('plus_hallway', (13, 3))
}


def get_size(key, rotation):
    if rotation == '90' or rotation == '270':
        w = prefabs[key][1][0]
        h = prefabs[key][1][1]
        return h, w
    else:
        return prefabs[key][1]


def get_prefab(key):
    return prefabs[key][0]


def get_keys():
    return prefabs.keys()