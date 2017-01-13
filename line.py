"""Script demonstrating drawing of anti-aliased lines using Xiaolin Wu's line
algorithm

usage: python xiaolinwu.py [output-file]

"""
from __future__ import division
import PyBearLibTerminal as terminal



import sys

def _fpart(x):
    return round(min(x - int(x) , 1.0), 2)


def _rfpart(x):
    return round(min(1 - _fpart(x),1.0), 2)


def drawchar(xy, color, alpha=1):
    x, y = xy
    terminal.color(color.trans(alpha))
    #terminal.bkcolor('black')
    terminal.put(x, y, 'O')
    #terminal.bkcolor('black')


def draw_line(p1, p2, color):
    """Draws an anti-aliased line in img from p1 to p2 with the given color."""

    x1, y1, x2, y2 = p1 + p2
    dx, dy = x2 - x1, y2 - y1
    steep = abs(dx) < abs(dy)
    p = lambda px, py: ((px, py), (py, px))[steep]

    if steep:
        x1, y1, x2, y2, dx, dy = y1, x1, y2, x2, dy, dx
    if x2 < x1:
        x1, x2, y1, y2 = x2, x1, y2, y1

    if dx == 0:
        grad = 0
    else:
        grad = dy / dx

    intery = y1 + _rfpart(x1) * grad

    def draw_endpoint(pt):
        x, y = pt
        xend1 = round(x)
        yend1 = y + grad * (xend1 - x)
        px, py = int(xend1), int(yend1)
        drawchar(p(px, py), color)
        return px

    xstart = draw_endpoint(p(*p1)) + 1
    xend = draw_endpoint(p(*p2))

    if xstart > xend:
        xstart, xend = xend, xstart

    for x in range(xstart, xend):
        y = int(intery)

        a1 = abs(int(_rfpart(intery) * 255) )
        a2 = abs(int(_fpart(intery) * 255) )
        drawchar(p(x, y), color, a1)
        drawchar(p(x, y+1), color, a2)
        intery += grad




