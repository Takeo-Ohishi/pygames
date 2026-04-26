'''
オブジェクト指向（クラスとインスタンス）で動く移動ゲームサンプル

このファイルは「クラス」を使ってオブジェクトを定義し、
そのクラスから複数のインスタンス（実体）を作って動かす例です。

ポイント（初心者向け）:
- クラスは「設計図」。同じ設計図から何個でもインスタンスを作れます。
- インスタンスはそれぞれ独立した状態（位置や色など）を持ちます。
- メソッドはそのオブジェクトができる操作（例: move, draw）です。
'''

import pygame

# ------------------ 単一クラス構成（初心者向けにフラット化） ------------------
class MovingObject:
    """移動するオブジェクトの単純なクラス（初心者向け）

    このクラスは「設計図」と「操作」を一つにまとめています。
    - インスタンスは位置や色、速度を持つ
    - 自分でキー入力を処理できる（controls を持つ）

        各操作キーは個別の属性（flat な変数）で渡します。例:
            key_left=pygame.K_LEFT, key_right=pygame.K_RIGHT, key_up=pygame.K_UP, key_down=pygame.K_DOWN
    """

    def __init__(self, x, y, width, height, color,
                 key_left, key_right, key_up, key_down, speed=5):
        # 状態（属性）を初期化
        # Rect で位置とサイズをまとめて扱います（x, y は左上の座標）
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = speed
        # フラットなキー属性（必ず指定してください）
        self.key_left = key_left
        self.key_right = key_right
        self.key_up = key_up
        self.key_down = key_down

    def move(self, dx, dy):
        """相対移動: dx, dy 分だけ位置を変える"""
        self.rect.x += dx
        self.rect.y += dy

    def handle_input(self, keys):
        """自分の controls を見てキーが押されていたら移動する"""
        dx = dy = 0
        if keys[self.key_left]:
            dx -= self.speed
        if keys[self.key_right]:
            dx += self.speed
        if keys[self.key_up]:
            dy -= self.speed
        if keys[self.key_down]:
            dy += self.speed
        self.move(dx, dy)

    def draw(self, screen):
        """画面に自分を四角で描画する"""
        pygame.draw.rect(screen, self.color, self.rect)

# ------------------ Pygame 初期化 ------------------
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Move Sample - 2 Objects")

# ------------------ インスタンス作成 ------------------
# ここでクラス（設計図）からインスタンス（実体）を2つ作ります。

# 矢印キーで動くプレイヤー（青）
player1 = MovingObject(
    100, 100, 50, 50, (0, 128, 255),
    pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN,
    speed=5
)

# WASD で動くプレイヤー（緑）
player2 = MovingObject(
    300, 200, 50, 50, (0, 200, 100),
    pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s,
    speed=5
)

# ------------------ メインループ ------------------
clock = pygame.time.Clock()     # フレームレート制御用の Clock を作ります
running = True                  # ゲームを続けるかどうかのフラグ

while running:
    clock.tick(60)  # 60FPS

    for event in pygame.event.get():    # イベント処理
        if event.type == pygame.QUIT:   # ウィンドウの「閉じる」ボタンが押されたら終了フラグを立てる
            running = False             # これでループを抜けてゲームが終了します

    # 押されているキーの状態を一度取得して各インスタンスに渡す
    keys = pygame.key.get_pressed()     # これで全キーの状態がわかります（True/False のリスト）
    player1.handle_input(keys)  # player1 は矢印キーで動く
    player2.handle_input(keys)  # player2 は WASD で動く

    # 描画
    screen.fill((0, 0, 0))  # 背景を黒で消す
    player1.draw(screen)    # player1 を描画
    player2.draw(screen)    # player2 を描画

    pygame.display.update() # 変更内容を画面に反映します（ダブルバッファの入れ替え）

pygame.quit()   # ループを抜けたら Pygame を終了してリソースを解放します。
