import pygame
import sys
import random

class MinesweeperAI:
    def __init__(self, rows, cols, num_mines):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.board = [[0] * cols for _ in range(rows)]
        self.revealed = set()
        self.mines = set()
        self.safe_cells = set()

    def place_mines(self, first_move):
        all_cells = [(i, j) for i in range(self.rows) for j in range(self.cols)]
        all_cells.remove(first_move)
        self.mines = set(random.sample(all_cells, self.num_mines))

    def calculate_neighbors(self, cell):
        neighbors = []
        row, col = cell
        for i in range(max(0, row - 1), min(row + 2, self.rows)):
            for j in range(max(0, col - 1), min(col + 2, self.cols)):
                if (i, j) != cell:
                    neighbors.append((i, j))
        return neighbors

    def update_board(self, cell, value):
        row, col = cell
        self.board[row][col] = value

    def reveal_cell(self, cell):
        self.revealed.add(cell)

    def flag_mine(self, cell):
        self.revealed.add(cell)

    def make_safe_move(self):
        if self.safe_cells:
            return self.safe_cells.pop()
        return None

    def make_random_move(self):
        all_cells = [(i, j) for i in range(self.rows) for j in range(self.cols)]
        unexplored_cells = set(all_cells) - self.revealed
        return random.choice(list(unexplored_cells))

    def make_move(self):
        safe_move = self.make_safe_move()
        if safe_move:
            return safe_move

        if not self.mines:
            return self.make_random_move()

        for mine in self.mines.copy():
            neighbors = self.calculate_neighbors(mine)
            unrevealed_neighbors = set(neighbors) - self.revealed
            mine_neighbors = unrevealed_neighbors.intersection(self.mines)
            if mine_neighbors:
                self.mines.remove(mine)
                self.safe_cells.update(unrevealed_neighbors - mine_neighbors)
                return mine_neighbors.pop()

        return self.make_random_move()

def draw_board(screen, ai):
    cell_size = 30
    margin = 2
    font = pygame.font.Font(None, 36)

    for row in range(ai.rows):
        for col in range(ai.cols):
            pygame.draw.rect(screen, (255, 255, 255), (col * cell_size, row * cell_size, cell_size - margin, cell_size - margin))
            pygame.draw.rect(screen, (0, 0, 0), (col * cell_size, row * cell_size, cell_size, cell_size), margin)

            cell = (row, col)
            if cell in ai.revealed:
                value = ai.board[row][col]
                text = font.render(str(value), True, (0, 0, 0))
                screen.blit(text, (col * cell_size + cell_size // 4, row * cell_size + cell_size // 4))

    pygame.display.flip()

def main():
    rows = 8
    cols = 8
    num_mines = 10
    first_move = (4, 4)

    ai = MinesweeperAI(rows, cols, num_mines)
    ai.place_mines(first_move)

    pygame.init()
    screen = pygame.display.set_mode((cols * 30, rows * 30))
    pygame.display.set_caption("Minesweeper AI")

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        move = ai.make_move()
        ai.reveal_cell(move)
        ai.update_board(move, 1)  # Assume the revealed cell has a value of 1 (can be adapted based on the actual game)
        draw_board(screen, ai)

        pygame.time.delay(500)  # Delay to visualize the moves
        clock.tick(10)

if __name__ == "__main__":
    main()
