import os
import pygame
import sys

# Pygame を初期化します。ウィンドウやフォントなどが使えるようになります。
pygame.init()

# ====== 画面設定（ウィンドウの大きさやクロック） ======
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 画面オブジェクト（この上に描画します）
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Screen Transition Demo")

# 時間管理用（フレーム制御）
clock = pygame.time.Clock()


# ====== 色定義（R,G,B のタプル） ======
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 200)
GREEN = (0, 150, 100)
GRAY = (200, 200, 200)
HOVER_COLOR = (100, 150, 255)  # マウスが乗ったときの色


# ====== フォント読み込みのヘルパー ======
def load_font(size):
    """
    指定したサイズのフォントを返す関数。
    - まずプロジェクトフォルダにある日本語フォントを探す。
    - なければシステムの日本語フォント候補を順に試す。
    - それでも無ければ Pygame のデフォルトフォントを使う。

    初心者向けのポイント:
    フォントは日本語を表示するために重要です。日本語が文字化けする場合、
    プロジェクト内に日本語対応フォント（例: NotoSansJP）を置くと確実です。
    """

    # プロジェクト内にあるフォントファイル名の候補
    candidates = [
        "NotoSansJP-Regular.otf",
        "NotoSansJP-Regular.ttf",
        "NotoSansJP-Medium.otf",
    ]

    # この Python ファイルと同じディレクトリにフォントファイルがあれば使う
    for name in candidates:
        path = os.path.join(os.path.dirname(__file__), name)
        if os.path.exists(path):
            try:
                return pygame.font.Font(path, size)
            except Exception:
                # フォントが壊れていたり読み込めない場合は次へ
                pass

    # システムに入っている日本語フォントを順に試す（Windows 想定）
    sys_candidates = ["Meiryo", "Yu Gothic", "MS Gothic", "MS UI Gothic", "Noto Sans JP"]
    for s in sys_candidates:
        try:
            f = pygame.font.SysFont(s, size)
            if f:
                return f
        except Exception:
            continue

    # どれも無ければ Pygame のデフォルトフォントを返す
    return pygame.font.Font(None, size)


# よく使うフォントを作っておく（大・中サイズ）
font_large = load_font(48)
font_medium = load_font(36)


# ====== ボタンクラス（再利用できる UI 部品） ======
class Button:
    """
    単純なボタンを表すクラス。
    - rect: 位置とサイズ（pygame.Rect）
    - text: ボタンに表示する文字列
    - callback: クリック時に呼ばれる関数
    - is_hovered: マウスが上にあるかのフラグ
    """

    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.is_hovered = False

    def draw(self, surface):
        """ボタンを画面に描画する。"""
        color = HOVER_COLOR if self.is_hovered else BLUE
        pygame.draw.rect(surface, color, self.rect)  # ボタンの背景
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # 枠線

        # 文字を中央寄せで描画
        text_surf = font_medium.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        """マウス座標 pos を受け取って、hover 状態を更新する。"""
        self.is_hovered = self.rect.collidepoint(pos)

    def check_click(self, pos):
        """クリック座標 pos がボタン内ならコールバックを呼ぶ。"""
        if self.rect.collidepoint(pos):
            self.callback()


# ====== 画面（スクリーン）クラス ======
class Screen:
    """
    1 つの「画面」を表すクラス。
    - name: 画面の名前（タイトル表示に使う）
    - buttons: その画面にあるボタンのリスト
    """

    def __init__(self, name):
        self.name = name
        self.buttons = []

    def draw(self, surface):
        """画面全体を描画する（背景とタイトル、ボタン）。"""
        surface.fill(WHITE)  # 背景を白で塗りつぶす
        title = font_large.render(self.name, True, BLACK)
        surface.blit(title, (50, 50))
        for button in self.buttons:
            button.draw(surface)

    def handle_event(self, event):
        """イベント（マウス移動・クリック）を受け取り、ボタンに伝える。"""
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.check_hover(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                button.check_click(event.pos)


# ====== 画面遷移のための管理（グローバルで現在の画面を持つ） ======
current_screen = None


def go_to_screen1():
    """画面1 に遷移するヘルパー関数。ボタンのコールバックとして使う。"""
    global current_screen
    current_screen = screen1


def go_to_screen2():
    """画面2 に遷移するヘルパー関数。"""
    global current_screen
    current_screen = screen2


def go_to_screen3():
    """画面3 に遷移するヘルパー関数。"""
    global current_screen
    current_screen = screen3


# ====== 実際のスクリーンを作る ======
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

current_screen = screen1  # 最初に表示する画面を設定


# ====== メインループ ======
running = True
while running:
    # イベント処理: キーボードやマウス、ウィンドウ操作を取得する
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # ウィンドウの閉じるボタンが押されたらループを抜ける
            running = False
        # 現在の画面にイベントを渡す（ボタンの hover/click 処理など）
        current_screen.handle_event(event)

    # 描画処理: 現在の画面を描画してウィンドウに表示する
    current_screen.draw(screen)
    pygame.display.flip()

    # フレームレート制御（ここでは 60 FPS）
    clock.tick(60)


# 終了処理: Pygame を終了してプロセスをクリーンに終了する
pygame.quit()
sys.exit()