import pygame

# ------------------ 1) Pygame の初期化 ------------------
# まず Pygame を使える状態にします。
pygame.init()

# ゲーム画面（ウィンドウ）を作成
screen = pygame.display.set_mode((800, 600))
# ウィンドウのタイトルを設定
pygame.display.set_caption("Click to change text クリックすると文字が変わるサンプル")

# ------------------ 2) 日本語フォントを選ぶ関数 ------------------
# 環境によって使えるフォントが違うため、候補を順番に試します。
def get_jp_font(size):
    """日本語表示に使うフォントを取得する。

    優先候補にあるフォントが見つかればそれを使い、
    見つからなければデフォルトフォントを返す。
    """
    available_fonts = set(pygame.font.get_fonts())

    # 優先したいフォント名を順番にチェック
    for font_name in ["meiryo", "notosansjp", "notosanscjkjp"]:
        if font_name in available_fonts:
            print(f"Using font: {font_name}")
            return pygame.font.SysFont(font_name, size)

    # どれも見つからなかった場合のフォールバック
    print("日本語フォントが見つからなかったため、デフォルトフォントを使用します。")
    return pygame.font.SysFont(None, size)

# 実際に使うフォントを決定
font = get_jp_font(24)

# ------------------ 3) ボタン見た目の準備 ------------------
# Rect は「位置とサイズ」をまとめて扱える便利な箱です。
button_rect = pygame.Rect(0, 0, 300, 100)
# 画面中央に配置
button_rect.center = (400, 300)
# ボタンの色（薄い青）
button_color = (200, 200, 255)

# ------------------ 4) 表示する文字の準備 ------------------
# クリックのたびに、このリストを順番に切り替えます。
messages = [
    "文字をクリックしてね",
    "1回クリックされた！",
    "2回クリックされた！",
    "3回クリックされた！",
    "またクリックしてね"
]

msg_index = 0  # 現在のメッセージ番号

# 最初に表示する文字を画像として作る（文字は毎回 render が必要）
text = font.render(messages[msg_index], True, (0, 0, 0))
text_rect = text.get_rect(center=button_rect.center)

# ------------------ 5) メインループ ------------------
# running が True の間、入力処理と描画を繰り返します。
running = True
while running:
    # まずイベント（閉じる、クリックなど）を処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # × ボタンが押されたらループ終了
            running = False

        # マウスクリック
        if event.type == pygame.MOUSEBUTTONDOWN:
            # クリック位置がボタン内ならメッセージを進める
            if button_rect.collidepoint(event.pos):
                # 次のメッセージへ
                # % を使うことで、最後まで行ったら先頭に戻る
                msg_index = (msg_index + 1) % len(messages)

                # 新しい文字をレンダリング
                text = font.render(messages[msg_index], True, (0, 0, 0))
                text_rect = text.get_rect(center=button_rect.center)

    # 画面を白で塗りつぶして前フレームを消す
    screen.fill((255, 255, 255))

    # ボタン本体を描画
    pygame.draw.rect(screen, button_color, button_rect)
    # ボタン上に文字を描画
    screen.blit(text, text_rect)

    # ここまでの描画結果を実際の画面に反映
    pygame.display.update()

# ループ終了後、Pygame を終了してリソースを解放
pygame.quit()