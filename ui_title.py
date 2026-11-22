import pyxel
import setting
import ui


title_image = pyxel.Image.from_image(str(setting.BASE_PATH / "assets/images/title.png"))


def title_button_layout():
    x = 190
    return {
        "start": dict(x=x, y=340, w=240, h=60, label="対戦開始", align="center"),
    }


def draw():
    ui.draw_image(0, 0, title_image)
