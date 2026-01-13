# drawing.py
import pygame

from constrants import (
    BLACK,
    BLUE,
    CELL_SIZE,
    COLS,
    PLAYER_1_PIECE,
    PLAYER_2_PIECE,
    RADIUS,
    RED,
    ROWS,
    SIDE_PANEL_WIDTH,
    WHITE,
    YELLOW,
)


def draw_board(screen, game):
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(
                screen,
                BLUE,
                (col * CELL_SIZE, (row + 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )
            pygame.draw.circle(
                screen,
                BLACK,
                (
                    col * CELL_SIZE + CELL_SIZE // 2,
                    (row + 1) * CELL_SIZE + CELL_SIZE // 2,
                ),
                RADIUS,
            )
            # White bold border
            pygame.draw.circle(
                screen,
                WHITE,
                (
                    col * CELL_SIZE + CELL_SIZE // 2,
                    (row + 1) * CELL_SIZE + CELL_SIZE // 2,
                ),
                RADIUS,
                5,
            )

    for row in range(ROWS):
        for col in range(COLS):
            piece = game.board.grid[row][col]
            if piece == PLAYER_1_PIECE:
                color = RED
            elif piece == PLAYER_2_PIECE:
                color = YELLOW
            else:
                continue

            pygame.draw.circle(
                screen,
                color,
                (
                    col * CELL_SIZE + CELL_SIZE // 2,
                    (row + 1) * CELL_SIZE + CELL_SIZE // 2,
                ),
                RADIUS - 4,
            )

