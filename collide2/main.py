'''
基本の移動ゲーム（初心者向けコメント付き）

このスクリプトは Pygame を使って、矢印キーでネコ（プレイヤー）を動かす
とてもシンプルな例です。コメントを多めに入れているので、Pygame の
基本的な流れ（初期化 → メインループ → 入力処理 → 描画 → 終了）が
理解しやすくなっています。

座標系の注意:
- 画面の左上が (0, 0) で、x が右に増え、y が下に増えます。
  （Scratch と異なり、Pygame の y 軸は下向きです）
'''

import pygame
import os
import sys
import random
import math

class WhiteCat(pygame.sprite.Sprite):
    def __init__(self, frames):
        super().__init__()
        self.frames = [f.copy() for f in frames]
        color = (255, 255, 255)  # 白色 
        for frame in self.frames:
            frame.fill(color, special_flags=pygame.BLEND_RGB_MULT)  
        self.frame_index = 0  # 現在のフレームインデックス
        self.image = self.frames[self.frame_index]  # 最初のフレームを表示するため
        self.rect = self.image.get_rect()  # 画像のサイズに合わせた Rect を作ります。
        px = random.randint(100, 700)
        py = random.randint(100, 500)
        self.rect.center = (px, py)  # プレイヤーを画面の中心に配置します。
        self.animation_timer = 0  # アニメーションのタイマー
        self.animation_speed = 2  # アニメーションの速度（フレーム数）

    def update(self,keys,mouse_pos):
        xx, yy = mouse_pos
        dx = xx - self.rect.centerx
        dy = yy - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.rect.x += dx / dist * 5
            self.rect.y += dy / dist * 5
        self.animate()
        angle = math.degrees(math.atan2(-dy, dx)) 
        self.image = pygame.transform.rotate(self.frames[self.frame_index], angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    def animate(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.animation_timer = 0

class RedCat(pygame.sprite.Sprite):
    def __init__(self, frames):
        super().__init__()
        self.frames = [f.copy() for f in frames]
        color = (255, 0, 0)  # 赤色
        for frame in self.frames:
            frame.fill(color, special_flags=pygame.BLEND_RGB_MULT)  
        self.frame_index = 0  # 現在のフレームインデックス
        self.image = self.frames[self.frame_index]  # 最初のフレームを表示するため
        self.rect = self.image.get_rect()  # 画像のサイズに合わせた Rect を作ります。
        px = random.randint(100, 700)
        py = random.randint(100, 500)
        self.rect.center = (px, py)  # プレイヤーを画面の中心に配置します。
        self.animation_timer = 0  # アニメーションのタイマー
        self.animation_speed = 2  # アニメーションの速度（フレーム数）

    def update(self,keys,mouse_pos):
        if keys[pygame.K_d]:
            self.rect.x += 5
            self.animate()
        elif keys[pygame.K_a]:
            self.rect.x -= 5
            self.animate()
            self.image = pygame.transform.flip(self.frames[self.frame_index], True, False)
        elif keys[pygame.K_w]:
            self.rect.y -= 5
            self.animate()
            self.image = pygame.transform.rotate(self.frames[self.frame_index], 90)
        elif keys[pygame.K_s]:
            self.rect.y += 5
            self.animate()
            self.image = pygame.transform.rotate(self.frames[self.frame_index], -90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def animate(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.animation_timer = 0

# --- メイン処理 ---
def main():

# Pygame の初期化。これを呼ばないと Pygame の機能は使えません。
    pygame.init()
    pygame.mixer.init()

# ------------------ 画面設定 ------------------
# 画面サイズを幅800、高さ600で作成します。
    screen = pygame.display.set_mode((800, 600))
# ウィンドウのタイトル（キャプション）を設定します。
    pygame.display.set_caption("Cat move sample")

# ------------------ プレイヤー設定 ------------------
    BASE_DIR = os.path.dirname(__file__)
    image1 = pygame.image.load(os.path.join(BASE_DIR, "costume1.png")).convert_alpha()  # プレイヤーの画像を読み込みます。
    image2 = pygame.image.load(os.path.join(BASE_DIR, "costume2.png")).convert_alpha()  # プレイヤーの画像を読み込みます。
    image1 = pygame.transform.scale(image1, (50, 50))  # 画像を 50x50 にリサイズします。
    image2 = pygame.transform.scale(image2, (50, 50))  # 画像を 50x50 にリサイズします。
    frames = [image1, image2]  # アニメーション用のフレームリスト

    pop_sound = os.path.join(BASE_DIR, "Pop.wav")

    cats = pygame.sprite.Group()
    whitecats = pygame.sprite.Group()
    redcats = pygame.sprite.Group()

    for _ in range(1):  # プレイヤーを複数作る
        cat = WhiteCat(frames)  # WhiteCat オブジェクトを作成
        cats.add(cat)
        whitecats.add(cat)
    for _ in range(5):  # プレイヤーを複数作る
        cat = RedCat(frames)  # RedCat オブジェクトを作成
        cats.add(cat)
        redcats.add(cat)

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
        mouse_pos = pygame.mouse.get_pos()
        cats.update(keys, mouse_pos)

        hits = pygame.sprite.groupcollide(whitecats, redcats, False, True)  # 衝突判定
        if hits:
            pygame.mixer.Sound(pop_sound).play()  # 衝突時の効果音を再生
            
    # ------------------ 描画処理 ------------------
        screen.fill((255, 255, 255))  # 背景を白で消す

        cats.draw(screen)  # プレイヤー（画像）を描画します。
        
        pygame.display.flip()   # 変更内容を画面に反映します（ダブルバッファの入れ替え）

    pygame.quit()   # ループを抜けたら Pygame を終了してリソースを解放します。
    sys.exit()

if __name__ == "__main__":
    main()
