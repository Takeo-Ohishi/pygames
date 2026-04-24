import os
import pygame
import sys

pygame.init()

# 画面設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Screen Transition Demo")
clock = pygame.time.Clock()

# 色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 200)
GREEN = (0, 150, 100)
GRAY = (200, 200, 200)
HOVER_COLOR = (100, 150, 255)

# フォント
def load_font(size):
    """プロジェクトに日本語フォントがあればそれを使い、無ければシステムの日本語フォントを試す。"""
    # 優先してプロジェクト内のフォントファイルを探す
    candidates = [
        "NotoSansJP-Regular.otf",
        "NotoSansJP-Regular.ttf",
        "NotoSansJP-Medium.otf",
    ]
    for name in candidates:
        path = os.path.join(os.path.dirname(__file__), name)
        if os.path.exists(path):
            try:
                return pygame.font.Font(path, size)
            except Exception:
                pass

    # システムフォント候補（Windowsを想定）
    sys_candidates = ["Meiryo", "Yu Gothic", "MS Gothic", "MS UI Gothic", "Noto Sans JP"]
    for s in sys_candidates:
        try:
            f = pygame.font.SysFont(s, size)
            if f:  # SysFont は必ずフォントオブジェクトを返すが念のため
                return f
        except Exception:
            continue

    # 最後の手段でデフォルト
    return pygame.font.Font(None, size)

font_large = load_font(48)
font_medium = load_font(36)

# ボタンクラス
class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.is_hovered = False

    def draw(self, surface):
        color = HOVER_COLOR if self.is_hovered else BLUE
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        text_surf = font_medium.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()

# 画面クラス
class Screen:
    def __init__(self, name):
        self.name = name
        self.buttons = []

    def draw(self, surface):
        surface.fill(WHITE)
        title = font_large.render(self.name, True, BLACK)
        surface.blit(title, (50, 50))
        for button in self.buttons:
            button.draw(surface)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.check_hover(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                button.check_click(event.pos)

# 画面遷移管理
current_screen = None

def go_to_screen1():
    global current_screen
    current_screen = screen1

def go_to_screen2():
    global current_screen
    current_screen = screen2

def go_to_screen3():
    global current_screen
    current_screen = screen3

# スクリーン定義
screen1 = Screen("画面1")
screen1.buttons = [
    Button(300, 200, 200, 60, "画面2へ", go_to_screen2),
    Button(300, 300, 200, 60, "画面3へ", go_to_screen3),
]

screen2 = Screen("画面2")
screen2.buttons = [
    Button(300, 200, 200, 60, "画面1へ戻る", go_to_screen1),
    Button(300, 300, 200, 60, "画面3へ", go_to_screen3),
]

screen3 = Screen("画面3")
screen3.buttons = [
    Button(300, 200, 200, 60, "画面1へ戻る", go_to_screen1),
    Button(300, 300, 200, 60, "画面2へ戻る", go_to_screen2),
]

current_screen = screen1

# メインループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        current_screen.handle_event(event)

    current_screen.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()