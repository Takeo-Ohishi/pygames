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
import os

# Pygame の初期化。これを呼ばないと Pygame の機能は使えません。
pygame.init()

# ------------------ 画面設定 ------------------
# 画面サイズを幅800、高さ600で作成します。
screen = pygame.display.set_mode((800, 600))
# ウィンドウのタイトル（キャプション）を設定します。
pygame.display.set_caption("Rect move sample")

# ------------------ プレイヤー設定 ------------------
# pygame.image.load() でプレイヤーの画像を読み込みます。
# pygame.transform.scale() で画像のサイズを調整します。
# get_rect() で画像の矩形領域を取得します。
# player_rect.center = (x, y)  # 矩形の中心座標を指定して配置します。
BASE_DIR = os.path.dirname(__file__)
image1 = pygame.image.load(os.path.join(BASE_DIR, "costume1.png")).convert_alpha()  # プレイヤーの画像を読み込みます。
image1 = pygame.transform.scale(image1, (50, 50))  # 画像を 50x50 にリサイズします。
image2 = pygame.image.load(os.path.join(BASE_DIR, "costume2.png")).convert_alpha()  # プレイヤーの画像を読み込みます。
image2 = pygame.transform.scale(image2, (50, 50))  # 画像を 50x50 にリサイズします。
image3 = pygame.transform.flip(image1, True, False)  # 画像を左右反転します。
image4 = pygame.transform.flip(image2, True, False)  # 画像を左右反転します。
image5 = pygame.transform.rotate(image1, 90)  # 画像を90度回転します。
image6 = pygame.transform.rotate(image2, 90)  # 画像を90度回転します。
image7 = pygame.transform.rotate(image1, 270)  # 画像を270度回転します。
image8 = pygame.transform.rotate(image2, 270)  # 画像を270度回転します。
frames = [image1, image2, image3, image4, image5, image6, image7, image8]  # アニメーション用のフレームリスト
frame_index = 0  # 現在のフレームインデックス
image = frames[frame_index]  # 最初のフレームを表示するため 
player_rect = image.get_rect()  # 画像のサイズに合わせた Rect を作ります。
player_rect.center = (400, 300)  # プレイヤーを画面の中心に配置します。
# ------------------ メインループ準備 ------------------
# フレームレート制御用の Clock を作ります。
clock = pygame.time.Clock()
# ゲームを続けるかどうかのフラグ
running = True
animation_timer = 0  # アニメーションのタイマー
animation_speed = 2  # アニメーションの速度（フレーム数）

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
        animation_timer += 1
        if animation_timer >= animation_speed:
            frame_index = (frame_index + 1) % 2
            image = frames[frame_index]
            animation_timer = 0
    # 左矢印キーが押されていたら x を減らす（左へ移動）
    if keys[pygame.K_LEFT]:
        player_rect.x -= 5
        animation_timer += 1
        if animation_timer >= animation_speed:
            frame_index = (frame_index + 1) % 2 + 2
            image = frames[frame_index]
            animation_timer = 0
    # 上矢印キーが押されていたら y を減らす（上へ移動）
    # Pygame では y が下方向に増えるので上へ行くには減らす
    if keys[pygame.K_UP]:
        player_rect.y -= 5
        animation_timer += 1
        if animation_timer >= animation_speed:
            frame_index = (frame_index + 1) % 2 + 4
            image = frames[frame_index]
            animation_timer = 0
    # 下矢印キーが押されていたら y を増やす（下へ移動）
    if keys[pygame.K_DOWN]:
        player_rect.y += 5
        animation_timer += 1
        if animation_timer >= animation_speed:
            frame_index = (frame_index + 1) % 2 + 6
            image = frames[frame_index]
            animation_timer = 0

    # ------------------ 描画処理 ------------------
    screen.fill((0, 0, 0))  # 背景を黒で消す

    screen.blit(image, player_rect)  # プレイヤー（画像）を描画します。
    pygame.display.flip()   # 変更内容を画面に反映します（ダブルバッファの入れ替え）

pygame.quit()   # ループを抜けたら Pygame を終了してリソースを解放します。
