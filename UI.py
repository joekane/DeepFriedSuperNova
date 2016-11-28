import libtcodpy as libtcod
import Constants
import Map
import GameState
import Render
import Animate
import Input
import Utils


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
        import Input
        mouse = Input.mouse

        min_x = offset_x - (self.length / 2)
        if Utils.is_mouse_in(min_x + self.x - 1, offset_y + self.y - 1, self.length + 2, 3):
            # libtcod.console_set_default_foreground(self.target, self.fore_alt)
            # libtcod.console_set_default_background(self.target, self.back_alt)
            Animate.large_button(self.x + offset_x, self.y + offset_y, self.text, True, length=self.length, target=self.target)
            if mouse.lbutton_pressed:
                # print "Func!"
                return self.function()

        else:
            # libtcod.console_set_default_foreground(self.target, self.fore)
            # libtcod.console_set_default_background(self.target, self.back)
            Animate.large_button(self.x + offset_x, self.y + offset_y, self.text, False, length=self.length, target=self.target)

        # libtcod.console_print_ex(self.target, 0, 0, libtcod.BKGND_SET, libtcod.LEFT, self.text)

        # libtcod.console_blit(self.target, 0, 0, self.rect.width, self.rect.height, 0 , min_x + 1 , min_y , 1.0, 1.0)


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
        import graphics
        self.opened = True
        print self.width, self.height
        pop = libtcod.console_new(self.width, self.height)
        # print the header, with auto-wrap
        libtcod.console_set_default_foreground(pop, Constants.UI_PopFore)
        libtcod.console_set_default_background(pop, Constants.UI_PopBack)

        libtcod.console_print_frame(pop, 0, 0, self.width, self.height, clear=True,
                                    flag=libtcod.BKGND_SET,
                                    fmt=self.title)
        # blit the contents of "window" to the root console

        x = 0
        y = 0

        button_text = 'Close'
        button = Button(button_text,
                        self.width / 2,
                        self.height - 3,
                        function=close_window)

        libtcod.console_set_default_foreground(pop, Constants.UI_PopFore)
        libtcod.console_set_default_background(pop, Constants.UI_PopBack)
        Render.print_rect(pop, 3, 3, self.width, self.height, self.text)

        background = libtcod.console_new(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)
        libtcod.console_blit(0, 0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, background, 0, 0, 1.0, 1.0)

        dragging = False
        click_x = None

        while True:

            Input.update()
            mouse = Input.mouse

            Render.blit(background, 0)
            # libtcod.console_blit(background, 0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, 0, 0, 0, 1.0, 1.0)
            libtcod.console_blit(pop, 0, 0, self.width, self.height, 0, x, y, 1.0, .85)

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
                return








            libtcod.console_flush()



            graphics.draw_image(x, y, enlarge=True)
            # graphics.draw_image(x + 1, y + 1, enlarge=True)
            # graphics.clear()
            graphics.draw_font(0,0)



def load_from_xp(x, y, filename, console):
    import gzip
    import xp_loader

    xp_file = gzip.open('Assets\_' + filename + '.xp')
    raw_data = xp_file.read()
    xp_file.close()

    xp_data = xp_loader.load_xp_string(raw_data)

    xp_loader.load_layer_to_console(console, xp_data['layer_data'][0])


def menu(header, options, width):
    key = libtcod.Key()
    mouse = libtcod.Mouse()
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_get_height_rect(Render.consoles['map_console'], 0, 0, width, Constants.SCREEN_HEIGHT, header)
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


def Display_MainMenu():
    new_game()

    # calculate total height for the header (after auto-wrap) and one line per option
    width = Constants.SCREEN_WIDTH
    height = Constants.SCREEN_HEIGHT

    mm = libtcod.console_new(width, height)
    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(mm, Constants.UI_PopFore)
    libtcod.console_set_default_background(mm, Constants.UI_PopBack)

    #libtcod.console_print_frame(mm, 0, 0, width, height, clear=True,
    #                            flag=libtcod.BKGND_SET,
    #                            fmt="Deep Fried Supernova")

    Render.print_rect(mm, 4, 4, width, height, 'Welcome to Deep Fried Supernova')


    # blit the contents of "window" to the root console
    x = 0
    y = 0


    button_text = 'New Game'
    ng_button = Button(button_text,
                       width / 2,
                       height - 12,
                       length=16,
                       function=new_game)

    button_text = 'Continue Game'
    ct_button = Button(button_text,
                       width / 2,
                       height - 9,
                       length=16,
                       function=continue_game)

    button_text = 'Quit'
    qt_button = Button(button_text,
                       width / 2,
                       height - 6,
                       length=16,
                       function=close_window)

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
        libtcod.console_flush()




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

    Render.print_rect(pop, 3, 3, width-6, height, text)


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


class Skill:
    def __init__(self, char, purchased=False):
        self.char = char
        self.purchased = purchased




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
    return 'close'


def continue_game():
    save_game = False
    if not save_game and GameState.get_player() is None:
        return 'nothing'
    elif not save_game and GameState.get_player() is not None:
        return 'continue'
    else:
        return 'load_save'



def new_game():
    # print "NG?"
    return GameState.new_game()


def test():
    print "TEST CLICK"


def do_nothing():
    return