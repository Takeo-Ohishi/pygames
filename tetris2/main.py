import pygame
import sys
import random

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

# 描画オフセット (中央に寄せる)
X_OFFSET = (SCREEN_WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2
Y_OFFSET = (SCREEN_HEIGHT - GRID_HEIGHT * BLOCK_SIZE) // 2

# 色 (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# テトロミノの色
COLORS = [
    (0, 255, 255),  # I: シアン
    (255, 255, 0),  # O: イエロー
    (128, 0, 128),  # T: パープル
    (0, 255, 0),    # S: グリーン
    (255, 0, 0),    # Z: レッド
    (0, 0, 255),    # J: ブルー
    (255, 165, 0)   # L: オレンジ
]

# テトロミノの形状 (0: 空, 1: ブロック)
SHAPES = [
    [[1, 1, 1, 1]], # I
    [[1, 1], [1, 1]], # O
    [[0, 1, 0], [1, 1, 1]], # T
    [[0, 1, 1], [1, 1, 0]], # S
    [[1, 1, 0], [0, 1, 1]], # Z
    [[1, 0, 0], [1, 1, 1]], # J
    [[0, 0, 1], [1, 1, 1]]  # L
]

class Tetromino:
    def __init__(self, x, y, shape_index):
        self.x = x
        self.y = y
        self.shape_index = shape_index
        self.shape = SHAPES[shape_index]
        self.color_index = shape_index

    def rotate(self):
        # 行列を転換して左右反転で回転
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class TetrisGame:
    def __init__(self):
        self.grid = [[-1 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False
        self.score = 0
    def new_piece(self):
        shape_index = random.randint(0, len(SHAPES) - 1)
        return Tetromino(GRID_WIDTH // 2 - 1, 0, shape_index)

    def check_collision(self, piece, dx=0, dy=0):
        shape = piece.shape
        for r, row in enumerate(shape):
            for c, cell in enumerate(row):
                if cell:
                    new_x = piece.x + c + dx
                    new_y = piece.y + r + dy
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return True
                    if new_y >= 0 and self.grid[new_y][new_x] != -1:
                        return True
        return False

    def freeze_piece(self):
        for r, row in enumerate(self.current_piece.shape):
            for c, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece.y + r][self.current_piece.x + c] = self.current_piece.color_index
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        if self.check_collision(self.current_piece):
            self.game_over = True

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(cell != -1 for cell in row)]
        for i in lines_to_clear:
            del self.grid[i]
            self.grid.insert(0, [-1 for _ in range(GRID_WIDTH)])
        
        # スコア計算 (1ライン: 100, 2ライン: 300, 3ライン: 500, 4ライン: 800)
        score_map = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}
        self.score += score_map.get(len(lines_to_clear), len(lines_to_clear) * 200)

    def move(self, dx, dy):
        if not self.check_collision(self.current_piece, dx, dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        if dy > 0:
            self.freeze_piece()
        return False

    def rotate_piece(self):
        old_shape = self.current_piece.shape
        self.current_piece.rotate()
        if self.check_collision(self.current_piece):
            self.current_piece.shape = old_shape

    def hard_drop(self):
        while self.move(0, 1):
            pass

def draw_grid(screen, grid):
    for r in range(GRID_HEIGHT):
        for c in range(GRID_WIDTH):
            color = BLACK if grid[r][c] == -1 else COLORS[grid[r][c]]
            # グリッドの枠線を描画
            pygame.draw.rect(screen, GRAY, (X_OFFSET + c * BLOCK_SIZE, Y_OFFSET + r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
            # ブロックの中身を描画
            if grid[r][c] != -1:
                pygame.draw.rect(screen, color, (X_OFFSET + c * BLOCK_SIZE + 1, Y_OFFSET + r * BLOCK_SIZE + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2))

def draw_piece(screen, piece):
    for r, row in enumerate(piece.shape):
        for c, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, COLORS[piece.color_index], 
                                 (X_OFFSET + (piece.x + c) * BLOCK_SIZE + 1, 
                                  Y_OFFSET + (piece.y + r) * BLOCK_SIZE + 1, 
                                  BLOCK_SIZE - 2, BLOCK_SIZE - 2))

def draw_next_piece(screen, piece):
    font = pygame.font.SysFont('Arial', 24)
    label = font.render('Next:', True, WHITE)
    screen.blit(label, (SCREEN_WIDTH - 100, 50))
    for r, row in enumerate(piece.shape):
        for c, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, COLORS[piece.color_index], 
                                 (SCREEN_WIDTH - 100 + c * BLOCK_SIZE, 
                                  80 + r * BLOCK_SIZE, 
                                  BLOCK_SIZE - 2, BLOCK_SIZE - 2))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Python Tetris')
    clock = pygame.time.Clock()
    game = TetrisGame()
    
    fall_time = 0
    fall_speed = 500 # ms
    
    while True:
        screen.fill(BLACK)
        dt = clock.tick(60)
        fall_time += dt
        
        if fall_time >= fall_speed:
            game.move(0, 1)
            fall_time = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if not game.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        game.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        game.move(1, 0)
                    elif event.key == pygame.K_DOWN:
                        game.move(0, 1)
                    elif event.key == pygame.K_UP:
                        game.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        game.hard_drop()
        
        # 描画
        draw_grid(screen, game.grid)
        if not game.game_over:
            draw_piece(screen, game.current_piece)
            draw_next_piece(screen, game.next_piece)
        else:
            font = pygame.font.SysFont('Arial', 48)
            text = font.render('GAME OVER', True, (255, 0, 0))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        
        # スコア表示
        font = pygame.font.SysFont('Arial', 24)
        score_text = font.render(f'Score: {game.score}', True, WHITE)
        screen.blit(score_text, (20, 20))

        pygame.display.flip()

if __name__ == "__main__":
    main()
