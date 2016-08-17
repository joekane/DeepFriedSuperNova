import libtcodpy as libtcod
import Constants

noise_field = None
height_map = None
rnd = libtcod.random_new_from_seed(654321)


def initialze():
    global noise_field, height_map
    noise_field = libtcod.noise_new(2, 0.5, 2.0, rnd)  # 0.5f  and 2.0f
    libtcod.noise_set_type(noise_field, libtcod.NOISE_SIMPLEX)

    height_map = libtcod.heightmap_new(Constants.MAP_WIDTH, Constants.MAP_HEIGHT)

    for y in range(Constants.MAP_HEIGHT):
        for x in range(Constants.MAP_WIDTH):
            libtcod.heightmap_set_value(height_map, x, y, get_noise_value(x, y, scale=50))

    libtcod.heightmap_normalize(height_map, 0.0, 1.0)
    libtcod.heightmap_add_hill(height_map, 40, 40, 6, 0.8)
    libtcod.heightmap_rain_erosion(height_map, 5000, 0.5, 0.2)


def get_height_value(x, y):
    return libtcod.heightmap_get_value(height_map, x, y)


def get_noise_value(x, y, scale=10):
    nx, ny = float(x) / scale, float(y) / scale

    # pre_value = libtcod.noise_get(noise_field, (nx, ny) , libtcod.NOISE_PERLIN)
    pre_value = libtcod.noise_get_fbm(noise_field, (nx, ny), 8, libtcod.NOISE_DEFAULT)
    # pre_value = libtcod.noise_get_turbulence(noise_field, (nx, ny), 8, libtcod.NOISE_DEFAULT)
    return pre_value





