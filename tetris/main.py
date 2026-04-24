import pygame
import random
from enum import Enum

# Pygame の初期化を行います。
pygame.init()

# -------------------- 定数定義 --------------------
# 画面サイズ（ピクセル）
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# ゲームのグリッド（横幅と縦幅、テトリスの標準は 10x20）
GRID_WIDTH = 10
GRID_HEIGHT = 20

# 1 マスあたりのピクセルサイズ（描画に使う）
CELL_SIZE = 20

# フレームレート（1 秒あたりの更新最大回数）
FPS = 60

# 色の定義（RGB タプル）
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# テトロミノのブロックに使う色の候補
COLORS = [
    (255, 0, 0),    # 赤
    (0, 255, 0),    # 緑
    (0, 0, 255),    # 青
    (255, 255, 0),  # 黄
    (255, 165, 0),  # オレンジ
    (255, 0, 255),  # マゼンタ
    (0, 255, 255),  # シアン
]

# -------------------- 形定義 --------------------
# それぞれの形は 2 次元配列で表現します。1 はブロック、0 は空。
# 例: I, O, S, Z, J, L, T
SHAPES = [
    [[1, 1, 1, 1]],  # I（一直線）
    [[1, 1], [1, 1]],  # O（正方形）
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[0, 1, 0], [1, 1, 1]],  # T
]


class Tetromino:
    """
    1 つのテトロミノ（落ちてくるブロック）の状態を表現するクラス。
    - shape: 2 次元リストで形を持つ（1=ブロック、0=空）
    - color: ブロックの色（RGB）
    - x, y: グリッド上の位置（x は横、y は縦）
    """

    def __init__(self):
        # ランダムに形と色を決める
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)

        # 初期 x は画面中央に近い位置に設定します。
        # len(self.shape[0]) は形の横幅（列数）を返すので、それを使って中央に置く。
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2

        # 初期 y は画面上部（0 行目）
        self.y = 0

    def rotate(self):
        """
        形を時計回りに 90 度回転させる。
        zip とスライスを使った簡単な行列回転のテクニック。
        """
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


# 自動で下に移動する間隔（ミリ秒）。値が大きいほどゆっくり落ちる。
FALL_INTERVAL = 500  # 0.5 秒ごとに 1 マス落ちる（例）


class Game:
    """
    ゲーム全体の状態を管理するクラス。
    - grid: 積み上がったブロックの状態（0=空、色タプル=ブロック）
    - current_piece: 現在操作中のテトロミノ
    - score: スコア
    - game_over: ゲーム終了フラグ
    - fall_timer: 落下のための時間計測用（ミリ秒）
    """

    def __init__(self):
        # 空のグリッドを作る（高さ GRID_HEIGHT 行、各行に GRID_WIDTH 列）
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

        # 最初のピースを生成
        self.current_piece = Tetromino()

        self.score = 0
        self.game_over = False

        # 経過時間を管理するタイマー
        self.fall_timer = 0

    def is_collision(self, piece, x, y):
        """
        指定した位置にピースを置いたときに衝突が起きるかを判定する。
        - 壁（左右）や床（下）にぶつかる
        - 既に積まれているブロックと重なる
        True を返すと「衝突している」
        """
        for row in range(len(piece.shape)):
            for col in range(len(piece.shape[row])):
                if piece.shape[row][col]:
                    grid_x = x + col
                    grid_y = y + row

                    # 左右の壁や床を超えると衝突
                    if grid_x < 0 or grid_x >= GRID_WIDTH or grid_y >= GRID_HEIGHT:
                        return True

                    # グリッド内で、既にブロックがある場所に当たると衝突
                    if grid_y >= 0 and self.grid[grid_y][grid_x]:
                        return True
        return False

    def place_piece(self, piece):
        """
        現在のピースをグリッドに固定（配置）する。
        グリッドに色タプルを入れて、積み上がるようにする。
        """
        for row in range(len(piece.shape)):
            for col in range(len(piece.shape[row])):
                if piece.shape[row][col]:
                    grid_y = piece.y + row
                    grid_x = piece.x + col
                    if grid_y >= 0:
                        # グリッドは 0（空）か色タプルが入る
                        self.grid[grid_y][grid_x] = piece.color

    def clear_lines(self):
        """
        横一列がすべて埋まっている行を消す（1 列消すごとにスコア加算）。
        消した行の上にある行を下げ、上に空行を挿入する。
        """
        # all(self.grid[i]) は行のすべての要素が真（0 でない）かを判定
        lines_to_clear = [i for i in range(GRID_HEIGHT) if all(self.grid[i])]
        for i in lines_to_clear:
            # 行を削除して、先頭に空行を挿入する
            del self.grid[i]
            self.grid.insert(0, [0] * GRID_WIDTH)

        # 消した行数に応じてスコアを加算（ここでは 100 点 / 行）
        self.score += len(lines_to_clear) * 100

    def update(self, dt):
        """
        毎フレーム（または毎ループ）呼ばれる更新処理。
        dt は前フレームからの経過時間（ミリ秒）
        """
        self.fall_timer += dt

        # 落下間隔に達していなければ何もしない
        if self.fall_timer < FALL_INTERVAL:
            return

        # タイマーをリセットして 1 マス下に落とす
        self.fall_timer = 0
        piece = self.current_piece

        # 下に移動して衝突しなければ下げる
        if not self.is_collision(piece, piece.x, piece.y + 1):
            piece.y += 1
        else:
            # 衝突する場合は現在の位置で固定して、新しいピースを生成
            self.place_piece(piece)
            self.clear_lines()
            self.current_piece = Tetromino()

            # 新しいピースが初期位置で既に衝突している場合はゲームオーバー
            if self.is_collision(self.current_piece, self.current_piece.x, self.current_piece.y):
                self.game_over = True

    def handle_input(self):
        """
        ユーザーからの入力処理（キーボードやウィンドウ閉じるなど）。
        戻り値: 続行するなら True、終了するなら False
        """
        for event in pygame.event.get():
            # ウィンドウの閉じるボタンが押された
            if event.type == pygame.QUIT:
                return False

            # キーが押されたときの処理
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # 左に移動して衝突しなければ x を減らす
                    if not self.is_collision(self.current_piece, self.current_piece.x - 1, self.current_piece.y):
                        self.current_piece.x -= 1
                elif event.key == pygame.K_RIGHT:
                    # 右に移動して衝突しなければ x を増やす
                    if not self.is_collision(self.current_piece, self.current_piece.x + 1, self.current_piece.y):
                        self.current_piece.x += 1
                elif event.key == pygame.K_DOWN:
                    # 下に素早く落とす（ソフトドロップ）
                    if not self.is_collision(self.current_piece, self.current_piece.x, self.current_piece.y + 1):
                        self.current_piece.y += 1
                elif event.key == pygame.K_UP:
                    # 回転させて、もし回転後に衝突したら元に戻す
                    original_shape = self.current_piece.shape
                    self.current_piece.rotate()
                    if self.is_collision(self.current_piece, self.current_piece.x, self.current_piece.y):
                        self.current_piece.shape = original_shape
        return True

    def draw(self, screen):
        """
        画面の描画処理。
        - グリッドに積まれたブロックを描画
        - 現在操作中のピースを描画
        - マス目（グリッド線）も描画して見やすくする
        """
        # 画面を黒で塗りつぶす
        screen.fill(BLACK)

        # グリッド上の各マスを描画する
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    # ブロックがある場合はその色で塗りつぶす
                    pygame.draw.rect(screen, self.grid[y][x],
                                     (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                # マス目の枠線を描画（どのセルがどれか分かるようにするため）
                pygame.draw.rect(screen, GRAY,
                                 (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        # 現在のピースを描画する（まだグリッドに固定されていない）
        piece = self.current_piece
        for row in range(len(piece.shape)):
            for col in range(len(piece.shape[row])):
                if piece.shape[row][col]:
                    pygame.draw.rect(screen, piece.color,
                                     ((piece.x + col) * CELL_SIZE, (piece.y + row) * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def main():
    """
    ゲーム実行のエントリポイント。
    ウィンドウ作成、メインループ、終了処理を行う。
    """
    # ウィンドウを作成（幅、高さ）
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")

    # 時間管理用のクロック（フレーム制御）
    clock = pygame.time.Clock()

    # ゲーム本体を生成
    game = Game()

    # メインループ（ゲームオーバーになるかウィンドウが閉じられるまで回る）
    while not game.game_over:
        # dt は前フレームからの経過時間（ミリ秒）
        dt = clock.tick(FPS)

        # 入力処理（False が返ると終了）
        if not game.handle_input():
            break

        # ゲーム状態更新（落下など）
        game.update(dt)

        # 描画
        game.draw(screen)
        pygame.display.flip()

    # Pygame を終了してリソースを解放
    pygame.quit()


if __name__ == "__main__":
    main()