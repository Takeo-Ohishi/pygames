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
    - インスタンスは位置や色を持つ
    - 移動（move）と描画（draw）を担当する
    """

    def __init__(self, x, y, width, height, color):
        # 状態（属性）を初期化
        # Rect で位置とサイズをまとめて扱います（x, y は左上の座標）
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def move(self, dx, dy):
        """相対移動: dx, dy 分だけ位置を変える"""
        self.rect.x += dx
        self.rect.y += dy

    def move_x(self, dx):
        """相対移動: dx 分だけ位置を変える"""
        self.rect.x += dx

    def move_y(self, dy):
        """相対移動: dy 分だけ位置を変える"""
        self.rect.y += dy

    def draw(self, screen):
        """画面に自分を四角で描画する"""
        pygame.draw.rect(screen, self.color, self.rect)

# ------------------ Pygame 初期化 ------------------
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Move Sample - 2個のオブジェクトが動くサンプル")

# 全オブジェクトで共通の移動速度
SPEED = 5

# ------------------ インスタンス作成 ------------------
# ここでクラス（設計図）からインスタンス（実体）を2つ作ります。

# 矢印キーで動くプレイヤー（青）
player1 = MovingObject(
    400, 200, 50, 50, (0, 128, 255)
)

# WASD で動くプレイヤー（緑）
player2 = MovingObject(
    100, 200, 50, 50, (0, 200, 100)
)

# ------------------ メインループ ------------------
clock = pygame.time.Clock()     # フレームレート制御用の Clock を作ります
running = True                  # ゲームを続けるかどうかのフラグ

while running:
    clock.tick(60)  # 60FPS

    for event in pygame.event.get():    # イベント処理
        if event.type == pygame.QUIT:   # ウィンドウの「閉じる」ボタンが押されたら終了フラグを立てる
            running = False             # これでループを抜けてゲームが終了します

    # 押されているキーの状態を一度取得し、ここで直接キー分岐して移動する
    keys = pygame.key.get_pressed()     # これで全キーの状態がわかります（True/False のリスト）

    # player1 は矢印キーで動く
    if keys[pygame.K_LEFT]:
        player1.move_x(-SPEED)
    if keys[pygame.K_RIGHT]:
        player1.move_x(SPEED)
    if keys[pygame.K_UP]:
        player1.move_y(-SPEED)
    if keys[pygame.K_DOWN]:
        player1.move_y(SPEED)

    # player2 は WASD で動く
    if keys[pygame.K_a]:
        player2.move_x(-SPEED)
    if keys[pygame.K_d]:
        player2.move_x(SPEED)
    if keys[pygame.K_w]:
        player2.move_y(-SPEED)
    if keys[pygame.K_s]:
        player2.move_y(SPEED)

    # 描画
    screen.fill((0, 0, 0))  # 背景を黒で消す
    player1.draw(screen)    # player1 を描画
    player2.draw(screen)    # player2 を描画

    pygame.display.flip()   # 変更内容を画面に反映します（ダブルバッファの入れ替え）

pygame.quit()   # ループを抜けたら Pygame を終了してリソースを解放します。
