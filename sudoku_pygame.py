import pygame

WIDTH = 361
HEIGHT = 361
SQUARE = 40
XTRA = 100
FPS = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SUDOKU SOLVER")
clock = pygame.time.Clock()

font_name = pygame.font.match_font("arial")


def draw_grid(screen, col=BLACK):
    for x in range(0, WIDTH, SQUARE):
        if x % 3 == 0:
            pygame.draw.line(screen, BLUE, (x, 0), (x, HEIGHT), 3)
        else:
            pygame.draw.line(screen, col, (x, 0), (x, HEIGHT), 1)

    for y in range(0, HEIGHT, SQUARE):
        if y % 3 == 0:
            pygame.draw.line(screen, BLUE, (0, y), (WIDTH, y), 3)
        else:
            pygame.draw.line(screen, col, (0, y), (WIDTH, y), 1)


def get_board():
    board = [[0, 0, 3, 4, 0, 0, 6, 0, 0],
             [5, 0, 0, 0, 2, 0, 0, 3, 0],
             [0, 0, 0, 0, 8, 0, 0, 0, 0],
             [0, 1, 7, 0, 0, 0, 0, 0, 0],
             [0, 0, 4, 0, 6, 2, 0, 0, 0],
             [0, 0, 0, 0, 0, 9, 0, 0, 0],
             [0, 7, 0, 0, 0, 0, 5, 0, 8],
             [9, 0, 0, 6, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 4, 0, 1, 0, 7]]
    return board.copy()


def draw_text(surf, text, size, x, y, color = WHITE):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)



def print_board(board):
    for i in range(len(board)):
        if i > 0 and i % 3 == 0:
            print()
        for j in range(len(board[0])):
            if j % 3 == 0 and j > 0:
                print(' ', end='')
            if board[i][j] == 0:
                print('_', end=' ')
            else:
                print(board[i][j], end=' ')
        print()
    print()



class Board:
    def __init__(self, screen):
        self.board = get_board()
        self.screen = screen
        self.pos_list = [(i, j) for i in range(9) for j in range(9) if self.board[i][j] == 0]
        self.show_board()

    def show_board(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] > 0:
                    x = (j * SQUARE) + SQUARE // 2
                    y = (i * SQUARE) + SQUARE // 4
                    if (i, j) in self.pos_list:
                        col = YELLOW
                    else:
                        col = WHITE
                    draw_text(screen, str(self.board[i][j]), 20, x, y, col)

    def isSafe(self, x, y, no):
        for i in range(9):
            if self.board[x][i] == no:
                return False
        for j in range(9):
            if self.board[j][y] == no:
                return False

        a = (x // 3) * 3
        b = (y // 3) * 3
        for i in range(a, a + 3):
            for j in range(b, b + 3):
                if self.board[i][j] == no:
                    return False
        return True

    def solve(self, x, y):
        if x == 9:
            return True
        if self.board[x][y] != 0:
            if y == 8:
                return self.solve(x + 1, 0)
            else:
                return self.solve(x, y + 1)

        for k in range(1, 10):
            if self.isSafe(x, y, k):
                self.board[x][y] = k
                if y == 8:
                    flag = self.solve(x + 1, 0)
                else:
                    flag = self.solve(x, y + 1)
                if flag:
                    return True
                self.board[x][y] = 0

        return False


    def next_move(self, ind):
        if ind == len(self.pos_list):
            return ind, True

        x, y = self.pos_list[ind]
        no = self.board[x][y] + 1

        if no <= 9:
            if self.isSafe(x, y, no):
                self.board[x][y] = no
                return ind+1, False
            else:
                self.board[x][y] = no
                return self.next_move(ind)
        else:
            self.board[x][y] = 0
            return ind-1, False

    def solve_instantly(self):
        self.board = get_board()
        self.solve(0, 0)


board = Board(screen)
ind = 0

running, gameover = True, False

print_board(board.board)
print("Press SpaceBar to skip Animation!")

#Game Loop
while running:

    #clock.tick(FPS)
    screen.fill(BLACK)

    draw_grid(screen, WHITE)
    board.show_board()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    #Press Space to solve instantly
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        board.solve_instantly()
        gameover = True


    if not gameover:
        ind, gameover = board.next_move(ind)
        # print_board(board.board)


    pygame.display.flip()

