'''
基本の移動ゲーム（初心者向けコメント付き）

このスクリプトは Pygame を使って、矢印キーで四角（プレイヤー）を動かす
とてもシンプルな例です。コメントを多めに入れているので、Pygame の
基本的な流れ（初期化 → メインループ → 入力処理 → 描画 → 終了）が
理解しやすくなっています。

座標系の注意:
- 画面の左上が (0, 0) で、x が右に増え、y が下に増えます。
  （Scratch と異なり、Pygame の y 軸は下向きです）
'''

import pygame

# Pygame の初期化。これを呼ばないと Pygame の機能は使えません。
pygame.init()

# ------------------ 画面設定 ------------------
# 画面サイズを幅800、高さ600で作成します。
screen = pygame.display.set_mode((800, 600))
# ウィンドウのタイトル（キャプション）を設定します。
pygame.display.set_caption("Rect move sample")

# ------------------ プレイヤー設定 ------------------
# プレイヤーは四角（Rect）で表現します。
# Rect(x, y, width, height)
# ここでの x, y は矩形の左上の座標です。
player_rect = pygame.Rect(400, 300, 50, 50)  # x, y, 幅, 高さ
# プレイヤーの色は RGB タプルで指定します。
player_color = (0, 128, 255)  # 水色っぽい色

# ------------------ メインループ準備 ------------------
# フレームレート制御用の Clock を作ります。
clock = pygame.time.Clock()
# ゲームを続けるかどうかのフラグ
running = True

# ------------------ メインループ ------------------
while running:
    # ここで毎フレームの上限 FPS を設定します（60 FPS に制限）。
    # これにより処理速度がマシン依存になりにくくなります。
    clock.tick(60)  # 60FPS

    # ------------------ イベント処理 ------------------
    # Pygame ではキーボードやマウス、ウィンドウ操作などの
    # イベントをイベントキューから取り出して処理します。
    for event in pygame.event.get():
        # ウィンドウの「閉じる」ボタンが押されたら終了フラグを立てる
        if event.type == pygame.QUIT:
            running = False

    # ------------------ キー入力（連続判定） ------------------
    # pygame.key.get_pressed() は全キーの押下状態を返します。
    # これを使うとキーを押し続けたときに連続して移動できます。
    keys = pygame.key.get_pressed()
    # 右矢印キーが押されていたら x を増やす（右へ移動）
    if keys[pygame.K_RIGHT]:
        player_rect.x += 5
    # 左矢印キーが押されていたら x を減らす（左へ移動）
    if keys[pygame.K_LEFT]:
        player_rect.x -= 5
    # 上矢印キーが押されていたら y を減らす（上へ移動）
    # Pygame では y が下方向に増えるので上へ行くには減らす
    if keys[pygame.K_UP]:
        player_rect.y -= 5
    # 下矢印キーが押されていたら y を増やす（下へ移動）
    if keys[pygame.K_DOWN]:
        player_rect.y += 5

    # ------------------ 描画処理 ------------------
    # まず画面全体を塗りつぶして前のフレームの残像を消します。
    # 引数は RGB のタプルで、ここでは黒にしています。
    screen.fill((0, 0, 0))  # 黒背景

    # プレイヤー（四角形）を描画します。
    # 引数は (画面, 色, 矩形)
    pygame.draw.rect(screen, player_color, player_rect)

    # 変更内容を画面に反映します（ダブルバッファの入れ替え）
    pygame.display.update()

# ループを抜けたら Pygame を終了してリソースを解放します。
pygame.quit()