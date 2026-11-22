import pyxel
import setting
import ui


TITLE_IMAGE_PATH = str(setting.BASE_PATH / "assets/title.png")


def load_image():
    palette = list(pyxel.colors)
    pyxel.Image.from_image(TITLE_IMAGE_PATH, include_colors=True)
    title_colors = [color for color in pyxel.colors if color not in palette]
    pyxel.colors[:] = palette + title_colors
    return pyxel.Image.from_image(TITLE_IMAGE_PATH)


def title_button_layout():
    x = 190
    return {
        "start": dict(x=x, y=340, w=240, h=60, label="対戦開始", align="center"),
    }


def draw(image):
    ui.draw_image(0, 0, image)
