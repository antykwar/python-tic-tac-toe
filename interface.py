import pygame
from colors import *
from logic import PvpGameLogic


class Cell(pygame.sprite.Sprite):
    _images_folder = 'resources/images/'
    _images_extension = '.png'

    def __init__(self, side, position_x, position_y):
        pygame.sprite.Sprite.__init__(self)
        self._side = side
        self._state = '-'
        self.image = pygame.Surface((self._side, self._side))
        self.rect = self.image.get_rect()
        self.rect.center = (position_x, position_y)

    def set_background(self, color):
        self.image.fill(color)

    def reset(self):
        self.set_background(WHITE)
        self._state = '-'

    def mark_as_success(self):
        self._draw_sign(winner=True)

    def get_state(self):
        return self._state

    def process_click(self, state):
        if self._state != '-':
            return

        if state != 'X':
            state = 'O'

        self._state = state
        self._draw_sign()

    def _draw_sign(self, winner=False):
        image = self._images_folder \
                + (self._state if not winner else self._state + '_winner') \
                + self._images_extension

        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (int(self._side), int(self._side)))


class Field(pygame.sprite.Group):
    _field_height_part = 0.7
    _game_in_progress = False
    _is_users_turn = True
    _current_symbol = 'X'
    _logic = PvpGameLogic()

    def __init__(self, screen_width, screen_height):
        pygame.sprite.Group.__init__(self)
        self._field_width = screen_width
        self._field_height = screen_height
        self._cell_side = self._field_height_part * 0.25 * self._field_height
        self._cells = []
        self._fill_cells()

    def set_game_state(self, state):
        self._game_in_progress = state

    def get_cell_size(self):
        return self._cell_side

    def get_screen_size(self):
        return self._field_width, self._field_height

    def process_click(self, mouse_position):
        if self._game_in_progress and self._is_users_turn:
            self._process_cells_click(mouse_position)

    def reset(self):
        for cell in self._cells:
            cell.reset()
        self._current_symbol = 'X'
        self.set_game_state(True)

    def _process_cells_click(self, mouse_position):
        for cell in self._cells:
            if cell.rect.collidepoint(mouse_position):
                cell.process_click(self._current_symbol)
                self._current_symbol = 'X' if self._current_symbol == 'O' else 'O'
                click_result = self._logic.get_movement_result(self._prepare_field_snapshot())
                self._process_cells_click_result(click_result)
                break

    def _prepare_field_snapshot(self):
        snapshot = []
        for cell in self._cells:
            snapshot.append(cell.get_state())
        return snapshot

    def _process_cells_click_result(self, result):
        self._is_users_turn = False
        if result['winner']:
            self._game_in_progress = False
            for index in result['winner_combination']:
                self._cells[index].mark_as_success()
        self._is_users_turn = True
        pass

    def _fill_cells(self):
        center_x = self._field_width / 2
        center_y = self._field_height * self._field_height_part / 2

        for row_num in range(0, 3):
            for cell_num in range(0, 3):
                shift_x = self._calculate_shift(cell_num)
                shift_y = self._calculate_shift(row_num)
                cell = Cell(self._cell_side, center_x + shift_x, center_y + shift_y)
                cell.set_background(WHITE)
                self.add(cell)
                self._cells.append(cell)

    def _calculate_shift(self, index):
        if index == 0:
            return -1 * self._cell_side - 5
        elif index == 2:
            return self._cell_side + 5
        else:
            return 0


class Button(pygame.sprite.Sprite):
    _color = BUTTONS_GREY
    _color_pressed = BUTTONS_PRESS_GREY

    def __init__(self, size, center, title, font_color=BLACK):
        pygame.sprite.Sprite.__init__(self)
        self._size = size
        self._center = center
        self._font_color = font_color
        self._font_size = self._size[-1] * 0.15
        self._title = title
        self.image = pygame.Surface(self._size)
        self.rect = self.image.get_rect()
        self.rect.center = self._center
        self.image.fill(self._color)
        self.print_title()

    def set_color(self, color=BUTTONS_GREY):
        self.image.fill(color)
        self.print_title()

    def print_title(self):
        font = pygame.font.SysFont("Arial", int(self._font_size), bold=True)
        title_surface = font.render(self._title, True, self._font_color)
        title_width = title_surface.get_width()
        title_height = title_surface.get_height()
        width, height = self._size
        self.image.blit(title_surface, [width / 2 - title_width / 2, height / 2 - title_height / 2])


class UserInterface(pygame.sprite.Group):
    _field_height_part = 0.3

    def __init__(self, field):
        pygame.sprite.Group.__init__(self)
        self._field = field
        self._field_width, self._field_height = field.get_screen_size()
        self._buttons = self._create_buttons()

    def process_button_down(self, mouse_position):
        for button in self._buttons.values():
            if button.rect.collidepoint(mouse_position):
                button.set_color(BUTTONS_PRESS_GREY)

    def process_button_up(self, mouse_position):
        for button in self._buttons.values():
            button.set_color()
            if button.rect.collidepoint(mouse_position):
                self._field.reset()

    def _calculate_buttons_dimensions(self):
        button_width = self._field.get_cell_size() * 2.5
        button_height = self._field_height_part * 0.66 * self._field_height

        center_x = self._field_width / 2
        basic_y = self._field_height * (1 - self._field_height_part)
        center_y = basic_y + 0.4 * self._field_height * self._field_height_part

        return button_width, button_height, center_x, center_y

    def _create_buttons(self):
        button_width, button_height, center_x, center_y = self._calculate_buttons_dimensions()

        pvp_button = Button(
            (button_width, button_height),
            (center_x, center_y),
            'Start new game'
        )
        self.add(pvp_button)

        return {'pvp_button': pvp_button}
