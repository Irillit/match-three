from enum import StrEnum
import math
import pygame
import pygame_gui
from game_board import GameBoard


class Colors(StrEnum):
    RED = "#EF1313"
    YELLOW = "#ffcc00"
    GREEN = "#39fc12"
    BLUE = "#12b6fc"
    MAGENTA = "#fc12f9"


COLOR_MAP = {
    0: Colors.RED,
    1: Colors.YELLOW,
    2: Colors.GREEN,
    3: Colors.BLUE,
    4: Colors.MAGENTA
}

BACKGROUND_COLOR = (220, 220, 220)
START_COORD_I = 15
START_COORD_J = 40
STEP = 22

WIDTH = 8
HEIGHT = 8

WINDOW_WIDTH = 230
WINDOW_HEIGHT = 300
all_sprites_list = pygame.sprite.Group()


class ClickableSprite(pygame.sprite.Sprite):

    def __init__(self, color_code: Colors):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(BACKGROUND_COLOR)

        pygame.draw.rect(self.image, color_code, pygame.Rect(0, 0, 20, 20))

        self.rect = self.image.get_rect()


def decode_click(position: tuple[int, int]) -> tuple[int, int] | None:
    """From window coordinates to game board matrix."""
    if position[0] < START_COORD_I or position[1] < START_COORD_J:
        return None

    i = math.floor((position[0] - START_COORD_I) / STEP)
    j = math.floor((position[1] - START_COORD_J) / STEP)

    if i > WIDTH or j > HEIGHT:
        return None

    return i, j

def draw_board(board: GameBoard):
    i_marg = START_COORD_I
    j_marg = START_COORD_J

    field = board.board
    for i in range(len(field)):
        for j in range(len(field[0])):
            elem = field[i][j]
            sprite = ClickableSprite(COLOR_MAP[elem])
            sprite.rect.x = i_marg
            sprite.rect.y = j_marg
            all_sprites_list.add(sprite)
            i_marg += STEP
        j_marg += + STEP
        i_marg = START_COORD_I

clock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('Quick Start')
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
background.fill(pygame.Color('#FFFFFF'))

is_running = True

manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), theme_path="quick_start.json")
new_game_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((105, 220), (90, 40)),
                                               text='New Game',
                                               manager=manager)

board = GameBoard(WIDTH, HEIGHT, 5)
font = pygame.font.SysFont("monospace", 15)

while is_running:
    time_delta = clock.tick(60) / 1000.0
    events = pygame.event.get()

    screen.fill(BACKGROUND_COLOR)
    draw_board(board)
    board.detect_row()
    board.detect_column()

    for event in events:
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == new_game_button:
                board.regenerate_board()
                draw_board(board)

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            coords = decode_click(pos)
            if coords:
                if board.selected_item and board.are_neighbours(coords):
                    board.swap(coords)
                    draw_board(board)
                    board.remove_selection()
                else:
                    board.select_item(coords)
                print(coords)

        manager.process_events(event)

    label = font.render(f"Score: {board.score}", True, (0, 0, 0))

    manager.update(time_delta)
    screen.blit(background, (0, 0))
    screen.blit(label, (START_COORD_I, 10))

    all_sprites_list.update(events)
    all_sprites_list.draw(screen)

    manager.draw_ui(screen)
    pygame.display.update()
