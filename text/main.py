import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Click to change text")

# 日本語フォントを取得する関数
def get_jp_font(size):
    # 1. Windows の Meiryo を試す
    try:
        return pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", size)
    except:
        pass

    # 2. あえて、Linux（Chromebook）の NotoSansCJKjp をファイル名で試す
    try:
        return pygame.font.SysFont("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", size)
    except:
        pass

    # 3. Linux（Chromebook）の NotoSansCJKjp を試す
    try:
        pass
        # return pygame.font.SysFont("NotoSansCJKjp", size)
    except:
        pass

    # 4. 最後のフォールバック（日本語は豆腐になる可能性あり）
    return pygame.font.SysFont(None, size)

font = get_jp_font(24)

# ボタンの Rect（画面中央）
button_rect = pygame.Rect(0, 0, 300, 100)
button_rect.center = (400, 300)
button_color = (200, 200, 255)

# 切り替える文字のリスト
messages = [
    "文字をクリックしてね",
    "1回クリックされた！",
    "2回クリックされた！",
    "3回クリックされた！",
    "またクリックしてね"
]

msg_index = 0  # 現在のメッセージ番号

# 最初の文字
text = font.render(messages[msg_index], True, (0, 0, 0))
text_rect = text.get_rect(center=button_rect.center)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # マウスクリック
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                # 次のメッセージへ
                msg_index = (msg_index + 1) % len(messages)

                # 新しい文字をレンダリング
                text = font.render(messages[msg_index], True, (0, 0, 0))
                text_rect = text.get_rect(center=button_rect.center)

    screen.fill((255, 255, 255))

    pygame.draw.rect(screen, button_color, button_rect)
    screen.blit(text, text_rect)

    pygame.display.update()

pygame.quit()