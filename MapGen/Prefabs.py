
# Prefab KEYS = Filename minus "_" , and Room size -1, -1 (for border)
prefabs = {
    'Room': ('basic_room', (9, 9)),
    #'L-Hall': ('L_hallway', (9, 9)),
    # 'Pipe': ('pipe_room', (9, 9)),
    #'LRoom': ('large_room', (18, 18)),
    # 'Test': ('test_room', (9, 9)),
    #'+hall': ('plus_hallway', (13, 3)),
    #'hall': ('hallway', (13, 3)),
    #'B': ('blank_room', (9, 9)),
    #'B2': ('blank2_room', (13, 6)),
    #'B3': ('blank3_room', (11, 11)),
    # 'B4': ('blank4_room', (16, 9))
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