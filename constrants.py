# constants.py

ROWS = 6
COLS = 7

PLAYER_1_PIECE = "R"
PLAYER_2_PIECE = "Y"
EMPTY = "."

# circular celss
CELL_SIZE = 100
RADIUS = CELL_SIZE // 2 - 5

# gap between cells
GAP = 5

SIDE_PANEL_WIDTH = 300

# window size
WIDTH = COLS * CELL_SIZE
HEIGHT = (ROWS + 1) * CELL_SIZE  # extra row for preview


DISPLAY_CAPTION = "Connect 4 by Alpha Group"

# colors
BLUE = (29, 99, 242)
RED = (211, 34, 54)
YELLOW = (254, 202, 16)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = 60

