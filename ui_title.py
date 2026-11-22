import pyxel
import setting
import ui


def title_button_layout():
    x = setting.GAME_WINDOW_WIDTH // 2
    return {
        "start": dict(x=x, y=340, w=240, h=60, label="対戦開始", align="center"),
    }


def draw():
    pyxel.cls(1)
    ui.draw_text(setting.GAME_WINDOW_WIDTH // 2, 170, 3, setting.TITLE_NAME, 7, align="center")
