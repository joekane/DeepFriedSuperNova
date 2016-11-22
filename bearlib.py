# coding=utf8

from __future__ import division
from bearlibterminal import terminal as blt
import Render

tiles = {
    'grass': 0xE200 + 0,
    'tree': 0xE200 + 1,
    'tree_fall': 0xE200 + 2,
    'pine': 0xE200 + 3,
    'moutain': 0xE200 + 4,
    'volcano': 0xE200 + 5,
    'tree_dead': 0xE200 + 6,
    'rocks': 0xE200 + 7,

    'stone_wall': 0xE200 + 8,
    'stairs': 0xE200 + 9,
    'human': 0xE200 + 10,
    'cape': 0xE200 + 11,
    'tunic': 0xE200 + 12,
    'staff': 0xE200 + 13,
    'boots': 0xE200 + 14,
    'equals': 0xE200 + 15,

    'ant': 0xE200 + 16,
    'dragonfly': 0xE200 + 17,
    'frog': 0xE200 + 18,
    'sand': 0xE200 + 19,
    'gravel': 0xE200 + 20,
    'door': 0xE200 + 21,
    'potion': 0xE200 + 22,
    'scroll': 0xE200 + 23,

    'gold': 0xE200 + 29,
}


def test_basic_output():
    blt.set("window.title='Omni: basic output'")
    blt.clear()
    blt.color("white")

    # Wide color range
    n = blt.print_(2, 1, "[color=orange]1.[/color] Wide color range: ")
    long_word = "antidisestablishmentarianism."
    long_word_length = len(long_word)
    for i in range(long_word_length):
        factor = i / long_word_length
        red = int((1 - factor) * 255)
        green = int(factor * 255)
        blt.color(blt.color_from_argb(255, red, green, 0))
        blt.put(2 + n + i, 1, long_word[i])

    blt.color("white")

    blt.print_(2, 3, "[color=orange]2.[/color] Backgrounds: [color=black][bkcolor=gray] grey [/bkcolor] [bkcolor=red] red ")

    blt.print_(2, 5, "[color=orange]3.[/color] Unicode support: Кириллица Ελληνικά α=β²±2°")

    blt.print_(2, 7, "[color=orange]4.[/color] Tile composition: @ + [color=red]|[/color] = @[+][color=red]|[/color], a vs. ¨ a[+][color=red]¨[/color]")

    blt.printf(2, 9, "[color=orange]5.[/color] Box drawing symbols:")

    blt.print_(5, 11,
        "   ┌────────┐  \n"
        "   │!......s└─┐\n"
        "┌──┘........s.│\n"
        "│............>│\n"
        "│...........┌─┘\n"
        "│<.@..┌─────┘  \n"
        "└─────┘  ■█┘╙       \n"
    )





    blt.refresh()
    key = None
    while key not in (blt.TK_CLOSE, blt.TK_ESCAPE):
        key = blt.read()


def test_tilesets():
    blt.set("window.title='Omni: tilesets'")
    blt.composition(True)

    # Load tilesets
    blt.set("U+E100: ./Images/Runic.png, size=8x16")
    blt.set("U+E200: ./Images/Tiles.png, size=32x32, align=top-left")
    blt.set("U+E400: ./Images/test_tiles.png, size=16x16, align=top-left")
    blt.set("U+E300: ./Fonts/fontawesome-webfont.ttf, size=24x24, spacing=3x2, codepage=./Fonts/fontawesome-codepage.txt")
    blt.set("zodiac font: ./Fonts/Zodiac-S.ttf, size=24x36, spacing=3x3, codepage=437")

    blt.clear()
    blt.color("white")

    blt.print_(2, 1, "[color=orange]1.[/color] Of course, there is default font tileset.")

    blt.print_(2, 3, "[color=orange]2.[/color] You can load some arbitrary tiles and use them as glyphs:")
    blt.print_(2+3, 4,
        "Fire rune ([color=red][U+E102][/color]), "
        "water rune ([color=lighter blue][U+E103][/color]), "
        "earth rune ([color=darker green][U+E104][/color])")

    blt.print_(2, 6, "[color=orange]3.[/color] Tiles are not required to be of the same size as font symbols:")
    blt.put(2+3+0, 7, 0xE200+7)
    blt.put(2+3+5, 7, 0xE200+8)
    blt.put(2+3+10, 7, 0xE200+9)

    blt.print_(2, 10, "[color=orange]4.[/color] Like font characters, tiles may be freely colored and combined:")

    blt.put_ext(2+3+0, 11, 0, 0, tiles['stone_wall'], [blt.color_from_name("red"),
                                                       blt.color_from_name("red"),
                                                       blt.color_from_name("blue"),
                                                       blt.color_from_name("red")])
    blt.put_ext(2 + 3 + 2, 11, 0, 0, tiles['stone_wall'], [blt.color_from_name("red"),
                                                           blt.color_from_name("blue"),
                                                           blt.color_from_name("red"),
                                                           blt.color_from_name("red")])
    blt.put_ext(2 + 3 + 0, 13, 0, 0, tiles['stone_wall'], [blt.color_from_name("red"),
                                                           blt.color_from_name("red"),
                                                           blt.color_from_name("blue"),
                                                           blt.color_from_name("blue")])
    blt.put_ext(2 + 3 + 2, 13, 0, 0, tiles['stone_wall'], [blt.color_from_name("blue"),
                                                           blt.color_from_name("blue"),
                                                           blt.color_from_name("red"),
                                                           blt.color_from_name("red")])

    blt.put_ext(2 + 3 + 0 + 5, 11, 0, 0, '#', [blt.color_from_name("yellow"),
                                                           blt.color_from_name("black"),
                                                           blt.color_from_name("black"),
                                                           blt.color_from_name("black")])
    blt.put_ext(2 + 3 + 1 + 5, 11, 0, 0, 'A', [blt.color_from_name("black"),
                                                           blt.color_from_name("yellow"),
                                                           blt.color_from_name("yellow"),
                                                           blt.color_from_name("black")])
    blt.put_ext(2 + 3 + 0 + 5, 12, 0, 0, 'A', [blt.color_from_name("black"),
                                                           blt.color_from_name("black"),
                                                           blt.color_from_name("yellow"),
                                                           blt.color_from_name("yellow")])
    blt.put_ext(2 + 3 + 1 + 5, 12, 0, 0,'@', [blt.color_from_name("dark yellow"),
                                                           blt.color_from_name("dark yellow"),
                                                           blt.color_from_name("dark yellow"),
                                                           blt.color_from_name("dark yellow")])

    blt.put_ext(2 + 3 + 0 + 7, 11, 0, 0, 'A', [blt.color_from_name("black"),
                                               blt.color_from_name("yellow"),
                                               blt.color_from_name("black"),
                                               blt.color_from_name("black")])

    blt.put_ext(2 + 3 + 0 + 7, 12, 0, 0, 'A', [blt.color_from_name("yellow"),
                                               blt.color_from_name("yellow"),
                                               blt.color_from_name("black"),
                                               blt.color_from_name("black")])


    '''
    # blt.color("lightest red")
    blt.put(2+3+4, 11,tiles['stairs'])
    # blt.color("purple")
    blt.put(2+3+8, 11, tiles['gold'])
    #blt.color("darkest red")
    blt.put(17, 11, 0xE400+0)
    blt.put(18, 11, 0xE400+0)
    blt.put(19, 11, 0xE400+1)
    blt.put(20, 11, 0xE400 + 0)
    blt.put(20, 11, 0xE400 + 2)

    blt.put(17, 12, 0xE400 + 10)
    blt.put(18, 12, 0xE400 + 10)
    blt.put(19, 12, 0xE400 + 11)
    blt.put(20, 12, 0xE400 + 10)
    blt.put(20, 12, 0xE400 + 12)
    '''
    blt.put(21, 11, 0xE400+0)
    blt.color("blue")
    blt.put(18, 11, '@')

    blt.color("white")
    order = [11, 10, 14, 12, 13]
    for i in range(len(order)):
        blt.put(30 + i * 4, 11, 0xE200 + order[i]);
        blt.put(30 + (len(order)+1) * 4, 11, 0xE200 + order[i])

    blt.put(30 + len(order) * 4, 11, 0xE200 + 15)

    blt.print_(2, 15, "[color=orange]5.[/color] And tiles can even come from TrueType fonts like this:")
    for i in range(6):
        blt.put(5 + i * 5, 15, 0xE300 + i)

    blt.print_(5, 18, "...or like this:\n[font=zodiac]D F G S C")

    blt.refresh()

    key = None
    while key not in (blt.TK_CLOSE, blt.TK_ESCAPE):
        key = blt.read()

    # Clean up
    blt.set("U+E100: none; U+E200: none; U+E300: none; zodiac font: none")
    blt.composition(False)


def test():
    blt.open()
    # blt.set("window: size=80x25, cellsize=auto, title='Omni: menu'; font: default")
    # blt.set("window: size=80x25, cellsize=auto, title='Omni: menu'; font: arial.ttf, size=8")  # font: UbuntuMono-R.ttf, size=12"
    blt.set("window: size=80x25, cellsize=auto, title='Omni: menu'; font: .\Fonts\cp437_16x16_alpha.png, size=16x16, codepage=437")  # font: UbuntuMono-R.ttf, size=12"
    blt.composition(blt.TK_ON)
    blt.color("white")
    test_basic_output()
    test_tilesets()
    blt.close()
