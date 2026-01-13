# aiWrapper.py
from typing import List, Optional
from constrants import ROWS, COLS, EMPTY


def check_win_token(grid: List[List[str]]) -> Optional[str]:
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            t = grid[r][c]
            if t != EMPTY and t == grid[r][c+1] == grid[r][c+2] == grid[r][c+3]:
                return t

    # Vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            t = grid[r][c]
            if t != EMPTY and t == grid[r+1][c] == grid[r+2][c] == grid[r+3][c]:
                return t

    # Diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            t = grid[r][c]
            if t != EMPTY and t == grid[r+1][c+1] == grid[r+2][c+2] == grid[r+3][c+3]:
                return t

    # Diagonal /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            t = grid[r][c]
            if t != EMPTY and t == grid[r-1][c+1] == grid[r-2][c+2] == grid[r-3][c+3]:
                return t

    return None


def is_full(grid: List[List[str]]) -> bool:
    return all(grid[0][c] != EMPTY for c in range(COLS))


def get_valid_columns(grid: List[List[str]]) -> List[int]:
    return [c for c in range(COLS) if grid[0][c] == EMPTY]


def drop_piece_copy(grid: List[List[str]], col: int, piece: str) -> List[List[str]]:
    new_grid = [row[:] for row in grid]
    for r in range(ROWS - 1, -1, -1):
        if new_grid[r][col] == EMPTY:
            new_grid[r][col] = piece
            break
    return new_grid


class Connect4Agent:
    def __init__(self, max_token: str, min_token: str, depth: int = 4):
        self.max_token = max_token
        self.min_token = min_token
        self.depth = depth

    def evaluate(self, grid: List[List[str]]) -> int:
        winner = check_win_token(grid)
        if winner == self.max_token:
            return 10000
        if winner == self.min_token:
            return -10000
        return 0

    def min_value(self, grid: List[List[str]], depth: int, alpha: int, beta: int) -> int:
        winner = check_win_token(grid)
        if depth == 0 or winner is not None or is_full(grid):
            return self.evaluate(grid)

        v = 10**9
        for col in get_valid_columns(grid):
            child = drop_piece_copy(grid, col, self.min_token)
            v = min(v, self.max_value(child, depth - 1, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def max_value(self, grid: List[List[str]], depth: int, alpha: int, beta: int) -> int:
        winner = check_win_token(grid)
        if depth == 0 or winner is not None or is_full(grid):
            return self.evaluate(grid)

        v = -10**9
        for col in get_valid_columns(grid):
            child = drop_piece_copy(grid, col, self.max_token)
            v = max(v, self.min_value(child, depth - 1, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def choose_next_move(self, grid: List[List[str]]) -> int:
        best_val = -10**9
        best_col = get_valid_columns(grid)[0]  # fallback

        for col in get_valid_columns(grid):
            child = drop_piece_copy(grid, col, self.max_token)
            val = self.min_value(child, self.depth - 1, -10**9, 10**9)
            if val > best_val:
                best_val = val
                best_col = col

        return best_col


def get_ai_move(grid: List[List[str]], ai_piece: str, human_piece: str, depth: int = 4) -> int:
    agent = Connect4Agent(max_token=ai_piece, min_token=human_piece, depth=depth)
    return agent.choose_next_move(grid)
