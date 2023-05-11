import os
import random
import pygame

os.environ['SDL_VIDEODRIVER'] = 'x11'

WIDTH = 900

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Sudoku:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont('Arial', 40)
        self.screen = pygame.display.set_mode((WIDTH, WIDTH))
        pygame.display.set_caption("Sudoku Solver")
        self.selected_cell = None
        self.constraints = [[set(range(1, 10)) for _ in range(9)] for _ in range(9)]
        self.grid = self.generate_grid()
        self.rects = self.create_rects()

    def generate_grid(self):
        grid = [[random.randint(1, 9) if random.randint(0, 10) == 0 else 0 for _ in range(9)] for _ in range(9)]
        return grid


    def get_possible_values(self, row, col):
        all_values = set(range(1, 10))
        row_values = set(self.grid[row])
        col_values = set(self.grid[i][col] for i in range(9))
        box_values = set(self.grid[i][j] for i in range(row // 3 * 3, (row // 3 + 1) * 3)
                        for j in range(col // 3 * 3, (col // 3 + 1) * 3))
        possible_values = all_values - row_values - col_values - box_values
        return list(possible_values)

    def update_constraints(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.update_constraints_for_cell(i, j)
        return True

    def update_constraints_for_cell(self, i, j):
        value = self.grid[i][j]
        for k in range(9):
            if k != j:
                self.constraints[i][k].discard(value)
            if k != i:
                self.constraints[k][j].discard(value)
        box_row, box_col = i // 3, j // 3
        for row in range(box_row * 3, box_row * 3 + 3):
            for col in range(box_col * 3, box_col * 3 + 3):
                if row != i or col != j:
                    self.constraints[row][col].discard(value)

    def solve(self):
        while True:
            min_values = 10
            min_cell = None
            for i in range(9):
                for j in range(9):
                    if self.grid[i][j] == 0:
                        values = self.get_possible_values(i, j)
                        if len(values) < min_values:
                            min_values = len(values)
                            min_cell = (i, j)
            if min_cell is None:
                return True
            values = self.get_possible_values(*min_cell)
            if not values:
                return False
            value = random.choice(values)
            self.grid[min_cell[0]][min_cell[1]] = value
            self.draw_board()
            self.update_constraints()


    def create_rects(self):
        rects = []
        for i in range(9):
            rect_list = []
            for j in range(9):
                rect = pygame.Rect(j*WIDTH // 9, i*WIDTH // 9, WIDTH // 9, WIDTH // 9)
                rect_list.append(rect)
            rects.append(rect_list)
        return rects

    def draw_cells(self):
        for i in range(9):
            for j in range(9):
                rect = self.rects[i][j]
                number = self.grid[i][j]
                pygame.draw.rect(self.screen, BLACK, rect, 1)
                if  number != 0:
                    text = self.font.render(str(number), True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)

    def draw_board(self):
        self.screen.fill(WHITE)
        self.draw_cells()
        pygame.display.flip()

    def show_text(self, text, color):
        font = pygame.font.Font(None, 100)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (WIDTH // 2, WIDTH // 2)
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

def main():
    # Solve the Sudoku puzzle using the Wave Function Collapse algorithm
    sudoku = Sudoku()
    while 1:
        sudoku.grid = sudoku.generate_grid()
        sudoku.update_constraints()
        if sudoku.solve() is True:
            sudoku.show_text("TRUE", GREEN)
        else:
            sudoku.show_text("FALSE", RED)
        pygame.time.delay(500)

if __name__ == "__main__":
    main()
