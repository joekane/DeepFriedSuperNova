from bearlibterminal import terminal

import collections
import Constants
import GameState
import Input
import Render
import Utils
import Engine.Animate as Animate
import libtcodpy as libtcod

Pos = collections.namedtuple('Pos', 'x y')
layers = {}


class Button:

    def __init__(self, text, x, y, function=None, length=None, target=0):
        self.text = text
        self.x = x
        self.y = y
        self.target = target
        if length is None:
            self.length = len(text)
        else:
            self.length = length
        self.fore = Constants.UI_Button_Fore
        self.back = Constants.UI_Button_Back
        self.fore_alt = Constants.UI_Button_Back
        self.back_alt = Constants.UI_Button_Fore

        if function is None:
            self.function = do_nothing
        else:
            self.function = function

    def draw(self, offset_x, offset_y):
        mouse = Input.mouse

        min_x = offset_x - (self.length / 2)
        if Utils.is_mouse_in(min_x + self.x - 1, offset_y + self.y - 1, self.length + 2, 3):
            # libtcod.console_set_default_foreground(self.target, self.fore_alt)
            # libtcod.console_set_default_background(self.target, self.back_alt)


            Animate.large_button(self.x + offset_x, self.y + offset_y, self.text, True, length=self.length, target=self.target)

            if mouse.lbutton_pressed:
                print "Func!"
                return self.function()

        else:
            # libtcod.console_set_default_foreground(self.target, self.fore)
            # libtcod.console_set_default_background(self.target, self.back)

            Animate.large_button(self.x + offset_x, self.y + offset_y, self.text, False, length=self.length, target=self.target)

        # libtcod.console_print_ex(self.target, 0, 0, libtcod.BKGND_SET, libtcod.LEFT, self.text)

        # libtcod.console_blit(self.target, 0, 0, self.rect.width, self.rect.height, 0 , min_x + 1 , min_y , 1.0, 1.0)


class Skill:
    def __init__(self, char, purchased=False):
        self.char = char
        self.purchased = purchased


class Palette:

    def __init__(self, width=None, height=None, title='', text=''):
        self.width = width
        self.height = height
        self.title = title
        self.text = text
        if width is None:
            self.width = Constants.MAP_CONSOLE_WIDTH - 10
        if height is None:
            self.height = libtcod.console_get_height_rect(0, 0, 0, width, Constants.SCREEN_HEIGHT, text) + 10
        self.opened = False

    def draw(self):
        Render.clear_layer(5)
        self.opened = True
        print self.width, self.height



        x = 5
        y = 5

        button_text = 'Close'
        button = Button(button_text,
                        self.width / 2,
                        self.height - 3,
                        function=close_window,
                        target=Render.layers['overlay_console'])

        dragging = False
        click_x = None

        mouse = Input.mouse

        while True:

            Input.update()
            Render.clear_layer(Render.layers['overlay_console'])

            Render.draw_rect(Render.layers['overlay_console'], x, y,
                             self.width,
                             self.height,
                             frame=True,
                             f_color=terminal.color_from_argb(255, 100, 100, 255),
                             bk_color=terminal.color_from_argb(192, 32, 32, 128),
                             title="POP_UP TEST!")

            Render.print_rect(Render.layers['overlay_console'], x + 2, y + 2, self.width - 4, self.height - 4, self.text)

            if mouse.lbutton and x <= mouse.cx <= x + self.width and (mouse.cy == y or dragging):
                if click_x is None:
                    click_x = mouse.cx - x
                x = mouse.cx - click_x    # (width / 2)
                y = mouse.cy
                dragging = True
            else:
                dragging = False
                click_x = None

            if button.draw(x, y) == 'close':
                self.opened = False
                Render.clear_layer(Render.layers['overlay_console'])
                return

            # libtcod.console_flush()

            # graphics.draw_image(x, y, enlarge=True)
            # graphics.draw_image(x + 1, y + 1, enlarge=True)
            # graphics.clear()
            # graphics.draw_font(0,0)

            GameState.render_ui()



def initilize_hud():
    global layers
    layers = Render.layers
    load_from_xp(Constants.MAP_CONSOLE_WIDTH, 0, 'Side_panel', Render.layers['UI_Back'])
    load_from_xp(0, Constants.MAP_CONSOLE_HEIGHT, 'Panel', Render.layers['UI_Back'])


def draw_hud():
    Render.clear_layer(layers['panel_console'])
    Render.clear_layer(layers['side_panel_console'])
    render_common()
    render_messages()
    render_status()
    render_stat_bars()


def render_common():
    import Input

    pos = Pos(Constants.MAP_CONSOLE_WIDTH, 0)

    Render.set_foreground(layers['side_panel_console'], libtcod.Color(0, 70, 140))

    """ LEVEL NUMBER """
    Render.print_rect(layers['side_panel_console'], pos.x + 1, pos.y + 1, 17, 1, "Level 1".center(17, ' '))

    """ MOUSE X / Y """
    Render.print_rect(layers['side_panel_console'], pos.x + 9, pos.y + 18, 17, 2,
                               "X: " + str(Input.mouse.cx) + "  \nY: " + str(Input.mouse.cy) + "  ")

    """ STATS """
    Render.set_foreground(layers['panel_console'], libtcod.Color(175, 175, 255))
    player = GameState.player

    Render.print_line(layers['side_panel_console'], Constants.MAP_CONSOLE_WIDTH + 5, 18, str(player.fighter.base_str).rjust(3))
    Render.print_line(layers['side_panel_console'], Constants.MAP_CONSOLE_WIDTH + 5, 19, str(player.fighter.base_def).rjust(3))
    Render.print_line(layers['side_panel_console'], Constants.MAP_CONSOLE_WIDTH + 5, 20, str(player.fighter.base_agl).rjust(3))
    Render.print_line(layers['side_panel_console'], Constants.MAP_CONSOLE_WIDTH + 5, 21, str(player.fighter.base_stm).rjust(3))
    Render.print_line(layers['side_panel_console'], Constants.MAP_CONSOLE_WIDTH + 5, 22, str(player.fighter.base_skl).rjust(3))
    Render.print_line(layers['side_panel_console'], Constants.MAP_CONSOLE_WIDTH + 5, 23, str(player.fighter.base_int).rjust(3))

    """ Items """
    ranged_items = [equip for equip in GameState.inventory if equip.ranged]
    equipped_ranged = [equip.name for equip in ranged_items if equip.equipment.is_equipped]
    if equipped_ranged:
        Render.print_line(layers['side_panel_console'], Constants.MAP_CONSOLE_WIDTH + 9, 20, equipped_ranged[0])


    """ CONTROLS """
    Render.print_line(layers['side_panel_console'], 59, 39, "Move/Attack:      NUMPAD/ARROWS")
    Render.print_line(layers['side_panel_console'], 59, 40, "Fire:                         F")
    Render.print_line(layers['side_panel_console'], 59, 41, "Pickup:                       G")
    Render.print_line(layers['side_panel_console'], 59, 42, "Pop-Up Test:                  B")
    Render.print_line(layers['side_panel_console'], 59, 43, "Decend:                       <")
    Render.print_line(layers['side_panel_console'], 59, 44, "Change Weapon:              [[/]]")
    Render.print_line(layers['side_panel_console'], 59, 45, "DEBUG:                        X")


    """ DUNGEON NAME """
    pos = Pos(0, Constants.MAP_CONSOLE_HEIGHT)

    Render.print_rect(layers['panel_console'], pos.x + 1, pos.y + 1, Constants.SCREEN_WIDTH - 19, 1,
               GameState.dungeon_name.center(57, ' '))
    # print_rect(layers['panel_console'], pos.x + 1, pos.y + 1, Constants.SCREEN_WIDTH - 19, 1,'TEST')


def render_status():
    # RENDER HEALTH BARS
    pos = Pos(Constants.MAP_CONSOLE_WIDTH + 1, 25)
    # CLEAR HP AREA / Status Area
    Render.set_foreground(layers['side_panel_console'], libtcod.black)
    Render.set_background(layers['side_panel_console'], libtcod.black)
    # draw_rect(layers['side_panel_console'], 1, 3, 17, 14, True, libtcod.BKGND_SET)
    # draw_rect(layers['side_panel_console'], pos.x, pos.y, 10, 9, True, libtcod.BKGND_SET)

    # print GameState.player.status

    num_of_status = 0
    inc = 0
    for st in GameState.player.status:
        if num_of_status == 9:
            Render.set_background(layers['side_panel_console'], libtcod.black)
            Render.set_foreground(layers['side_panel_console'], libtcod.Color(51, 51, 51))
            Render.print_line(layers['side_panel_console'], pos.x, pos.y - 1 + inc,
                              "...             ")  # + " (" + str(st[1]) + ")")
            return
        Render.set_background(layers['side_panel_console'], libtcod.black)
        Render.set_foreground(layers['side_panel_console'], st['color'])

        if Utils.is_mouse_in(pos.x, pos.y + inc, 17, 1):
            Render.print_line(layers['side_panel_console'], pos.x, pos.y + inc, str(st['duration']) + " Turns")  # + " (" + str(st[1]) + ")")
        else:
            Render.print_line(layers['side_panel_console'], pos.x, pos.y + inc, st['name'])  # + " (" + str(st[1]) + ")")
        num_of_status += 1
        inc += 1


def render_stat_bars():

    pos = Pos(Constants.MAP_CONSOLE_WIDTH + 4, 35)

    # SHOW PLAYER STAT BARS
    Render.draw_box_bar(pos.x, pos.y, 14, '', GameState.get_player().fighter.hp, GameState.get_player().fighter.base_max_hp,
                        libtcod.Color(178, 0, 45),
                        libtcod.Color(64, 0, 16), layers['side_panel_console'])
    Render.draw_box_bar(pos.x, pos.y + 1, 14, '', GameState.get_player().fighter.sp, GameState.get_player().fighter.base_max_sp,
                        libtcod.Color(0, 30, 255),
                        libtcod.Color(0, 10, 64), layers['side_panel_console'])
    Render.draw_box_bar(pos.x, pos.y + 2, 14, '', GameState.get_player().fighter.xp, 1000,  # TODO: will be NEXT_LVL_XP
                   libtcod.Color(255, 255, 0),
                        libtcod.Color(65, 65, 0), layers['side_panel_console'])

    # RENDER MONSTER HEALTH BARS
    temp_y = 3
    for object in GameState.current_level.get_visible_objects():
        if object.fighter and object.base_speed != 0 and (object is not GameState.get_player()):  # and Fov.is_visible(obj=object)
            if temp_y < 17: # TODO: Make constant to scale UI
                Render.draw_box_bar(Constants.MAP_CONSOLE_WIDTH + 1, temp_y, 17, object.name, object.fighter.hp, object.fighter.max_hp,
                                    libtcod.Color(0, 255, 0),
                                    libtcod.Color(0, 64, 0),
                                    layers['side_panel_console'])
                temp_y += 2


def render_messages():
    Render.clear_layer(layers['messages'])
    y = 3 + Constants.MAP_CONSOLE_HEIGHT
    for (line, color) in GameState.get_msg_queue():
        if y < Constants.SCREEN_HEIGHT - 1:
            Render.set_foreground(layers['messages'], color)
            # line_height = libtcod.console_get_height_rect(consoles['panel_console'], 0, 0, Constants.MSG_WIDTH, Constants.PANEL_HEIGHT - 3, line)
            line_height = 1
            Render.print_rect(layers['messages'], Constants.MSG_X, y, Constants.MSG_WIDTH, line_height, line)

            y += line_height


def load_from_xp(x, y, filename, console):
    import gzip
    from Engine import xp_loader

    xp_file = gzip.open('Assets\_' + filename + '.xp')
    raw_data = xp_file.read()
    xp_file.close()

    xp_data = xp_loader.load_xp_string(raw_data)

    xp_loader.load_layer_to_layer(console, x, y, xp_data['layer_data'][0])


def menu(header, options, width):
    key = libtcod.Key()
    mouse = libtcod.Mouse()
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_get_height_rect(Render.layers['map_console'], 0, 0, width, Constants.SCREEN_HEIGHT, header)
    if header == '':
        header_height = 0
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)

    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        Render.print_line(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = Constants.SCREEN_WIDTH / 2 - width / 2
    y = Constants.SCREEN_HEIGHT / 2 - height / 2
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.5)

    # compute x and y offsets to convert console position to menu position
    x_offset = x  # x is the left edge of the menu
    y_offset = y + header_height  # subtract the height of the header from the top edge of the menu

    while True:
        # present the root console to the player and check for input
        libtcod.console_flush()
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if mouse.lbutton_pressed:
            (menu_x, menu_y) = (mouse.cx - x_offset, mouse.cy - y_offset)
            # check if click is within the menu and on a choice
            if 0 <= menu_x < width and 0 <= menu_y < height - header_height:
                return menu_y

        if mouse.rbutton_pressed or key.vk == libtcod.KEY_ESCAPE:
            return None  # cancel if the player right-clicked or pressed Escape

        if key.vk == libtcod.KEY_ENTER and key.lalt:
            # Alt+Enter: toggle fullscreen
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        # convert the ASCII code to an index; if it corresponds to an option, return it
        index = key.c - ord('a')
        if 0 <= index < len(options):
            return index
        # if they pressed a letter that is not an option, return None
        if 0 <= index <= 26:
            return


def display_mainMenu():
    # new_game()

    width = Constants.SCREEN_WIDTH
    height = Constants.SCREEN_HEIGHT

    Render.draw_rect(10, 0, 0, width, height,
                     frame=True,
                     f_color=terminal.color_from_name('dark azure'),
                     bk_color=terminal.color_from_name('darkest azure'),
                     title="DEEP FRIED SUPERNOVA v0.01")

    Render.print_rect(10, 4, 4, width, height, 'Welcome to Deep Fried Supernova')


    # blit the contents of "window" to the root console
    x = 0
    y = 0


    button_text = 'New Game'
    ng_button = Button(button_text,
                       width / 2,
                       height - 12,
                       length=16,
                       function=new_game,
                       target=10)

    button_text = 'Continue Game'
    ct_button = Button(button_text,
                       width / 2,
                       height - 9,
                       length=16,
                       function=continue_game,
                       target=10)

    button_text = 'Quit'
    qt_button = Button(button_text,
                       width / 2,
                       height - 6,
                       length=16,
                       function=close_window,
                       target=10)

    img = libtcod.image_load('diner_logo_sm.png')
    # libtcod.image_set_key_color(img, libtcod.Color(0, 0, 0))

    # show the background image, at twice the regular console resolution
    #libtcod.image_blit_2x(img, mm, 37, 2)

    #libtcod.console_blit(mm, 0, 0, width, height, 0, 0, 0, 1.0, 1.0)

    while True:
        Input.update()

        if qt_button.draw(0,0) == 'close':
            return

        if ct_button.draw(0,0) == 'continue':
            return

        ng_button.draw(0, 0)
        terminal.refresh()


def pop_up(width=None, height=None, title=None, text=None):
    mouse = Input.mouse
    key = Input.key

    # calculate total height for the header (after auto-wrap) and one line per option
    if width is None:
        width = Constants.MAP_CONSOLE_WIDTH - 30

    if height is None:
        height = libtcod.console_get_height_rect(0, 0, 0, width, Constants.SCREEN_HEIGHT, text) + 7

    pop = libtcod.console_new(width, height)
    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(pop, Constants.UI_PopFore)
    libtcod.console_set_default_background(pop, Constants.UI_PopBack)

    libtcod.console_print_frame(pop, 0, 0, width, height, clear=True,
                                flag=libtcod.BKGND_SET,
                                fmt=title)

    Render.print_rect(pop, 3, 3, width - 6, height, text)


    # blit the contents of "window" to the root console
    x = Constants.MAP_CONSOLE_WIDTH / 2 - width / 2
    y = Constants.MAP_CONSOLE_HEIGHT / 2 - height / 2


    button_text = 'Click to Continue'
    button = Button(button_text,
                    width / 2,
                    height - 3,
                    function=close_window,
                    target=pop,
                    length=len(button_text))

    libtcod.console_blit(pop, 0, 0, width, height, 0, x, y, 1.0, .85)

    while True:
        libtcod.console_blit(pop, 0, 0, width, height, 0, x, y, 1.0, 0.0)
        libtcod.console_flush()
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if button.draw(x, y) == 'close':
            return

        if key.vk == libtcod.KEY_ENTER and key.lalt:
            # Alt+Enter: toggle fullscreen
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        if key.vk == libtcod.KEY_ESCAPE or key.vk == libtcod.KEY_ESCAPE or key.vk == libtcod.KEY_SPACE:
            return


def beastiary(width=10, height=10, title=None, text=None):

    # calculate total height for the header (after auto-wrap) and one line per option
    if width is None:
        width = Constants.MAP_CONSOLE_WIDTH - 10

    if height is None:
        height = libtcod.console_get_height_rect(0, 0, 0, width, Constants.SCREEN_HEIGHT, text) + 7

    pop = libtcod.console_new(width, height)
    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(pop, Constants.UI_PopFore)
    libtcod.console_set_default_background(pop, Constants.UI_PopBack)

    libtcod.console_print_frame(pop, 0, 0, width, height, clear=True,
                                flag=libtcod.BKGND_SET,
                                fmt=title)
    # blit the contents of "window" to the root console

    x = 0
    y = 0

    button_text = 'Click to Continue'
    button = Button(button_text,
                    width / 2,
                    height - 3,
                    function=close_window)

    img = libtcod.image_load('Images//cipher_warden_80x80_test_01.png')
    libtcod.image_set_key_color(img, libtcod.Color(0, 0, 0))
    # show the background image, at twice the regular console resolution
    libtcod.image_blit_2x(img, pop, 9, 2)

    libtcod.console_set_default_foreground(pop, Constants.UI_PopFore)
    libtcod.console_set_default_background(pop, Constants.UI_PopBack)
    Render.print_rect(pop, 3, 3, width - 6, height, text)

    background = libtcod.console_new(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)
    libtcod.console_blit(0, 0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, background, 0, 0, 1.0, 1.0)

    dragging = False

    click_x = None

    while True:
        Input.update()
        mouse = Input.mouse

        Render.blit(background, 0)
        # libtcod.console_blit(background, 0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, 0, 0, 0, 1.0, 1.0)
        libtcod.console_blit(pop, 0, 0, width, height, 0, x, y, 1.0, .85)

        if mouse.lbutton and x <= mouse.cx <= x + width and (mouse.cy == y or dragging):
            if click_x is None:
                click_x = mouse.cx - x
            x = mouse.cx - click_x    # (width / 2)
            y = mouse.cy
            dragging = True
        else:
            dragging = False
            click_x = None

        if button.draw(x, y) == 'close':
            return
        libtcod.console_flush()


def msgbox(text, width=50):
    menu(text, [], width)  # use menu() as a sort of "message box"


def inventory_menu(header):
    # show a menu with each item of the inventory as an option
    if len(GameState.inventory) == 0:
        options = ['Inventory is empty.']
    else:
        options = []
        for item in GameState.inventory:
            text = item.name
            # show additional information, in case it's equipped
            if item.equipment and item.equipment.is_equipped:
                text = text + ' (on ' + item.equipment.slot + ')'
            options.append(text)

    index = menu(header, options, Constants.INVENTORY_WIDTH)

    # if an item was chosen, return it
    if index is None or len(GameState.inventory) == 0:
        return None
    return GameState.inventory[index].item


def skill_tree():
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # calculate total height for the header (after auto-wrap) and one line per option
    width = Constants.MAP_CONSOLE_WIDTH
    height = Constants.MAP_CONSOLE_HEIGHT

    st = libtcod.console_new(width, height)
    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(st, Constants.UI_PopFore)
    libtcod.console_set_default_background(st, Constants.UI_PopBack)

    libtcod.console_print_frame(st, 0, 0, width, height, clear=True,
                                flag=libtcod.BKGND_SET,
                                fmt="Skill Tree")

    Render.print_rect(st, 4, 4, width, height, 'Insert Skill Tree')

    # blit the contents of "window" to the root console
    x = 0
    y = 0

    file = open('Assets\skill_tree.map', 'r')

    # fill map with "blocked" tiles
    #kills = [[' ' for y in range(Constants.MAP_CONSOLE_HEIGHT)] for x in range(Constants.MAP_CONSOLE_WIDTH)]

    skills = [[Skill(' ') for y in range(Constants.MAP_HEIGHT)] for x in range(Constants.MAP_WIDTH)]



    selected_x = 0
    selected_y = 0

    for y in range(Constants.MAP_CONSOLE_HEIGHT):
        line = file.readline()
        # print line
        x = 0
        for c in line:
            if c == 'S':
                selected_x = x
                selected_y = y
                skills[x][y] = Skill(c, True)
            else:
                skills[x][y] = Skill(c)
            x += 1

    # print selected_x, selected_y



    button_text = 'Exit'
    ct_button = Button(button_text,
                       width / 2,
                       height - 3,
                       length=6,
                       function=close_window)



    while True:

        libtcod.console_flush()
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)



        if key.vk == libtcod.KEY_LEFT:
            if skills[selected_x-1][selected_y].char == "-":
                selected_x -= 2
        elif key.vk == libtcod.KEY_RIGHT:
            if skills[selected_x + 1][selected_y].char == "-":
                selected_x += 2
        elif key.vk == libtcod.KEY_UP:
            if skills[selected_x][selected_y-1].char == "|":
                selected_y -= 2
        elif key.vk == libtcod.KEY_DOWN:
            if skills[selected_x ][selected_y+1].char == "|":
                selected_y += 2
        elif key.vk == libtcod.KEY_SPACE:
            skills[selected_x][selected_y].purchased = True

        if selected_y < 0:
            selected_y = 0
        if selected_x < 0:
            selected_x = 0

        offset = 20, 10

        for y in range(Constants.MAP_CONSOLE_HEIGHT):
            for x in range(Constants.MAP_CONSOLE_WIDTH):
                # print skills
                if selected_x == x and selected_y == y:
                    color = libtcod.purple
                else:
                    if skills[x][y].purchased:
                        color = libtcod.green
                    else:
                        color = libtcod.white

                char = skills[x][y].char
                if char == "|":
                    Render.draw_char(st, x + x + offset[0], y + y + offset[1], libtcod.CHAR_VLINE, libtcod.white, Constants.UI_PopBack)
                elif char == "-":
                    Render.draw_char(st, x + x + offset[0], y + y + offset[1], libtcod.CHAR_HLINE, libtcod.white, Constants.UI_PopBack)
                elif char == ".":
                    if color == libtcod.purple:
                        Render.draw_char(st, x + x + offset[0] + 1, y + y + offset[1] - 1, libtcod.CHAR_DNE,
                                         color, Constants.UI_PopBack)
                        Render.draw_char(st, x + x + offset[0], y + y + offset[1] - 1, libtcod.CHAR_DHLINE,
                                         color, Constants.UI_PopBack)
                        Render.draw_char(st, x + x + offset[0] - 1, y + y + offset[1] - 1, libtcod.CHAR_DNW,
                                         color, Constants.UI_PopBack)
                        Render.draw_char(st, x + x + offset[0] - 1, y + y + offset[1], libtcod.CHAR_DVLINE,
                                         color, Constants.UI_PopBack)
                        Render.draw_char(st, x + x + offset[0] + 1, y + y + offset[1], libtcod.CHAR_DVLINE,
                                         color, Constants.UI_PopBack)
                        Render.draw_char(st, x + x + offset[0] + 1, y + y + offset[1] + 1, libtcod.CHAR_DSE,
                                         color, Constants.UI_PopBack)
                        Render.draw_char(st, x + x + offset[0], y + y + offset[1] + 1, libtcod.CHAR_DHLINE,
                                         color, Constants.UI_PopBack)
                        Render.draw_char(st, x + x + offset[0] - 1, y + y + offset[1] + 1, libtcod.CHAR_DSW,
                                         color, Constants.UI_PopBack)
                    else:
                        Render.draw_char(st, x + x + offset[0] + 1, y + y + offset[1] - 1, ' ',
                                         color, Constants.UI_PopBack)
                        Render.draw_char(st, x + x + offset[0], y + y + offset[1] - 1, ' ',
                                         color, Constants.UI_PopBack)
                        Render.draw_char(st, x + x + offset[0] - 1, y + y + offset[1] - 1, ' ',
                                         color, Constants.UI_PopBack)
                        Render.draw_char(st, x + x + offset[0] - 1, y + y + offset[1], ' ',
                                         color, Constants.UI_PopBack)
                        Render.draw_char(st, x + x + offset[0] + 1, y + y + offset[1], ' ',
                                         color, Constants.UI_PopBack)
                        Render.draw_char(st, x + x + offset[0] + 1, y + y + offset[1] + 1, ' ',
                                         color, Constants.UI_PopBack)
                        Render.draw_char(st, x + x + offset[0], y + y + offset[1] + 1, ' ',
                                         color, Constants.UI_PopBack)
                        Render.draw_char(st, x + x + offset[0] - 1, y + y + offset[1] + 1, ' ',
                                         color, Constants.UI_PopBack)

                    Render.draw_char(st, x + x + offset[0], y + y + offset[1], chr(4),
                                     libtcod.white, Constants.UI_PopBack)




                elif char != ' ' and char != chr(10):
                    Render.draw_char(st, x + x + offset[0] + 1, y + y + offset[1] - 1, libtcod.CHAR_DNE, color, Constants.UI_PopBack)
                    Render.draw_char(st, x + x + offset[0], y + y + offset[1] - 1, libtcod.CHAR_DHLINE, color, Constants.UI_PopBack)
                    Render.draw_char(st, x + x + offset[0] - 1, y + y + offset[1] - 1, libtcod.CHAR_DNW, color, Constants.UI_PopBack)

                    Render.draw_char(st, x + x + offset[0] - 1, y + y + offset[1], libtcod.CHAR_DVLINE, color, Constants.UI_PopBack)

                    Render.draw_char(st, x + x + offset[0], y + y + offset[1], char, libtcod.red, Constants.UI_PopBack)

                    Render.draw_char(st, x + x + offset[0] + 1, y + y + offset[1], libtcod.CHAR_DVLINE, color, Constants.UI_PopBack)

                    Render.draw_char(st, x + x + offset[0] + 1, y + y + offset[1] + 1, libtcod.CHAR_DSE, color, Constants.UI_PopBack)
                    Render.draw_char(st, x + x + offset[0], y + y + offset[1] + 1, libtcod.CHAR_DHLINE, color, Constants.UI_PopBack)
                    Render.draw_char(st, x + x + offset[0] - 1, y + y + offset[1] + 1, libtcod.CHAR_DSW, color, Constants.UI_PopBack)



        if ct_button.draw(x, y) == 'close':
            return


        libtcod.console_blit(st, 0, 0, width, height, 0, 0, 0, 1.0, 1.0)


def close_window():
    return terminal.close()


def continue_game():
    GameState.load_game()
    return GameState.play_game()


def new_game():
    # print "NG?"
    return GameState.new_game()


def do_nothing():
    return