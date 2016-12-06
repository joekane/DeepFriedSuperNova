from bearlibterminal import terminal
import libtcodpy as libtcod
from itertools import cycle
import Render
import Utils
import GameState
import random


""" ANIMATIONS """

animations = {
    'Flame': {
        'color_list': Utils.gradient([libtcod.yellow,
                                      libtcod.flame,
                                      libtcod.darker_flame,
                                      libtcod.darkest_flame,
                                      libtcod.darkest_grey],
                                     [0,
                                      5,
                                      10,
                                      20,
                                      25]),
        'char_list': [0x2022, 0x25CB, 'o', 'O'],
        'min_size': 0,
        'max_size': 6,
        'density': 20,
        'angle_range': 22.5,
        'loop': True,
        'delay_avg': 0.4,
        'delay_sd': 0.1,
        'background': True,
        'vector': 'Line',
        'random_chr': True,
        'random_color': False
    },
    'TinyFire': {
        'color_list': Utils.gradient([libtcod.yellow,
                                      libtcod.flame,
                                      libtcod.darker_flame,
                                      libtcod.darkest_flame,
                                      libtcod.darkest_grey],
                                     [0,
                                      5,
                                      10,
                                      20,
                                      25]),
        'char_list': [0x2022, 0x25CB, 'o', 'O'],
        'min_size': 0,
        'max_size': 0,
        'density': 1,
        'angle_range': 360,
        'loop': True,
        'delay_avg': 0.0,
        'delay_sd': 0.0,
        'background': True,
        'vector': 'Line',
        'random_chr': True,
        'random_color': False
    },
    'Burst': {
        'color_list': Utils.gradient([libtcod.yellow,
                                      libtcod.dark_flame,
                                      libtcod.darker_flame,
                                      libtcod.darkest_flame,
                                      libtcod.darkest_flame],
                                     [0,
                                      4,
                                      8,
                                      9,
                                      10]),
        'char_list': [0x2022, 0x25CB, 'o', 'O'],
        'min_size': 1,
        'max_size': 5,
        'density': 75,
        'angle_range': 360,
        'loop': False,
        'delay_avg': 0.5,
        'delay_sd': 0.2,
        'background': True,
        'vector': 'Line',
        'random_target': True,
        'random_chr': True,
        'random_color': False
    },
    'Xmas': {
        'color_list': [libtcod.red, libtcod.green],
        'char_list': [0x2022, 0x25CB, 'o', 'O'],
        'min_size': 5,
        'max_size': 5,
        'density': 50,
        'angle_range': 360,
        'loop': True,
        'delay_avg': 1.0,
        'delay_sd': 0.5,
        'background': True,
        'vector': 'Line',
        'random_chr': True,
        'random_color': False
    },
    'Shot': {
        'color_list': [libtcod.light_grey],
        'char_list': [0x2022],
        'min_size': 1,
        'max_size': 1,
        'density': 1,
        'angle_range': 0,
        'loop': False,
        'delay_avg': 0.1,
        'delay_sd': 0.1,
        'background': False,
        'vector': 'Line',
        'random_target': False,
        'random_chr': True,
        'random_color': False
    },
    'Breath': {
        'color_list':  Utils.gradient([libtcod.light_blue,
                                      libtcod.azure,
                                      libtcod.blue,
                                      libtcod.darkest_azure,
                                      libtcod.darkest_blue],
                                     [0,
                                      5,
                                      10,
                                      20,
                                      25]),
        'char_list':[0x2022, 0x25CB, 'o', 'O'],
        'min_size': 3,
        'max_size': 5,
        'density': 30,
        'angle_range': 23,
        'target_angle': 0,
        'loop': False,
        'delay_avg': 0.2,
        'delay_sd': 0.2,
        'background': True,
        'vector': 'Breath',
        'random_target': True,
        'random_chr': True,
        'random_color': False
    }
}

vectors = {
    'Line': {

    }

}

A_FLAME = animations['Flame']


class Animation:
    def __init__(self, animation_name, **kwargs):
        self.animation = animations[animation_name]
        self.animation.update(kwargs)
        self.cells = []

    def play(self):
        for cell in self.cells:
            results = cell._draw()
            if results == 'Done':
                # print "should be removed"
                self.cells.remove(cell)
        if not self.cells:
            return "Done"


class AddAnimation(Animation):
    def __init__(self, animation_name, kwargs):
        Animation.__init__(self, animation_name, **kwargs)

        for number in range(int(self.animation['density'])):
            self.cells.append(Cell(self.animation))





class Cell:
    def __init__(self, animation):

        # NEED TO CONVERT Coords to Camera Coords

        self.origin = animation['origin']
        self.target = animation['target']
        self._chr_list = animation['char_list']
        self._color_list = animation['color_list']
        self.chr_list = cycle(animation['char_list'])
        self.color_list = cycle(animation['color_list'])
        self.delay = random.gauss(animation['delay_avg'],animation['delay_sd'])
        self.current_frame = 999
        self.chr = animation['char_list'][0]
        self.color = animation['color_list'][0]
        self.frame = None
        self.max_size = animation['max_size']
        self.random_chr = animation['random_chr']
        self.random_color = animation['random_color']
        self.background = animation['background']
        self.loops = 1
        #print "Color Key: {0}".format(self.color_keys)

        """ VARIOUS ANIMATION VECTORS """
        if animation['vector'] == 'Line':
            if not animation['random_target']:
                # Goto Target
                source = animation['origin']
                target = animation['target']
            else:
                # if Non specified, randomize
                source = animation['target']
                target = Utils.get_vector(source[0], source[1],
                                          random.randint(animation['min_size'], animation['max_size']),
                                          random.randint(0 - (animation['angle_range']/2), 0 + (animation['angle_range']/2) ))
            self.vector = Line(source, target, animation['loop'])
        if animation['vector'] == 'Breath':
            target_angle = animation['target_angle']
            if not animation['random_target']:
                # Goto Target
                source = animation['origin']
                target = animation['target']
            else:
                # if Non specified, randomize
                source = animation['origin']
                target = Utils.get_vector(source[0], source[1],
                                          random.randint(animation['min_size'], animation['max_size']),
                                          random.randint(target_angle - (animation['angle_range']/2), target_angle + (animation['angle_range']/2) ))
            self.vector = Line(source, target, animation['loop'])

    def _draw(self):

        self.current_frame += 0.1
        if self.current_frame >= self.delay:
            self.current_frame = 0
            self.frame = self.vector.next_pos()
            if self.random_chr:
                self.chr = random.choice(self._chr_list)
            else:
                self.chr = next(self.chr_list)
            if self.random_color:
                self.color = random.choice(self._color_list)
            else:
                #determin percentage of travel
                index = int((float(self.loops) / float(self.max_size))*len(self._color_list))
                # print "Loops: {0}, Max Size: {2}, Index: {1}".format(self.loops, index, self.max_size)

                self.color = self._color_list[min(index, len(self._color_list)-1)]
                # print "Loops: {0}, Max Size: {2}, Index: {1}".format(self.loops, index, self.max_size)
            self.loops += 1


        if self.frame:
            for cell in self.frame:
                cam_x, cam_y = Utils.to_camera_coordinates(cell[0], cell[1])
                if not GameState.current_level.is_blocked(cell[0], cell[1], ignore_mobs=True) and GameState.current_level.is_visible(pos=(cell[0], cell[1])):
                    if self.background:
                        Render.draw_char(10, cam_x, cam_y, Utils.get_unicode(219), color=random.choice(self._color_list), alpha=64)
                    Render.draw_char(10, cam_x, cam_y, self.chr, color=self.color)

        else:
            #print "Animation Done."
            return 'Done'



class Vector:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.pos = pos
        pass

    def _update(self):
        pass

    def next_pos(self):
        return self._update()





class Line(Vector):
    def __init__(self, start, target, loop=True):
        Vector.__init__(self, start)
        self.end_x = target[0]
        self.end_y = target[1]
        self.target_pos = target
        self.path = cycle(Utils.b_line((self.x, self.y), (self.end_x, self.end_y)))
        self.loop = loop
        self.stop_animating = False
        self.distance = Utils.distance_between(self.x, self.y, self.end_x, self.end_y)

    def _update(self):
        if not self.stop_animating:
            x, y = next(self.path)
            if x == self.end_x and y == self.end_y:
                if not self.loop:
                    self.stop_animating = True
                elif type(self.loop) == int:
                    self.loop -= 1
            return [(x, y)]
        else:
            return None


class Blast(Vector):
    def __init__(self, x, y, radius, loop=True):
        Vector.__init__(self, x, y)
        self.radius = radius
        self.path = cycle(Utils.b_line((self.x, self.y), (self.end_x, self.end_y)))
        self.loop = loop
        self.stop_animating = False


'''
class Anim:
    def __init__(self, cell_list):
        self.cell_list = cell_list

    def draw(self):
        for cell in self.cell_list:
            result = cell._draw()
            if result == 'Done':
                self.cell_list.remove(cell)
        if not self.cell_list:
            return "Done"
'''