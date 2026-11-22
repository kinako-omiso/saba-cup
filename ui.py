import pyxel
import setting


FONT_HEIGHT = 12
font = None


def aligned_position(x, y, width, height, align="left", valign="top"):
    left = x
    top = y
    if align == "center":
        left -= width // 2
    elif align == "right":
        left -= width
    if valign == "center":
        top -= height // 2
    elif valign == "bottom":
        top -= height
    return left, top


def draw_image(x, y, image, align="left", valign="top", colkey=None):
    left, top = aligned_position(x, y, image.width, image.height, align, valign)
    pyxel.blt(left, top, image, 0, 0, image.width, image.height, colkey)


def draw_text(x, y, n, text, col, align="left", valign="top", width=None, line_height=None):
    lines = text.split("\n") if width is None else wrap_text(text, font, width // n)
    if line_height is None:
        line_height = FONT_HEIGHT * n
    height = (len(lines) - 1) * line_height + FONT_HEIGHT * n
    _, top = aligned_position(x, y, 0, height, valign=valign)
    for index, line in enumerate(lines):
        if not line:
            continue
        text_width = font.text_width(line)
        left, _ = aligned_position(x, y, text_width * n, 0, align=align)
        image = pyxel.Image(text_width, FONT_HEIGHT)
        transparent = (col + 1) % 16
        image.cls(transparent)
        image.text(0, 0, line, col, font)

        pyxel.blt(left + text_width * (n - 1) / 2,
                  top + index * line_height + FONT_HEIGHT * (n - 1) / 2,
                  image, 0, 0, text_width, FONT_HEIGHT, transparent, scale=n)
    return height


def wrap_text(text, font, width):
    lines = []
    line = ""
    for character in text:
        if character == "\n":
            lines.append(line)
            line = ""
            continue
        if font.text_width(line + character) > width:
            lines.append(line)
            line = ""
        line += character
    lines.append(line)
    return lines


class UI:
    def __init__(self, books):
        global font
        font = pyxel.Font(str(setting.FONT_PATH), FONT_HEIGHT)


    def draw_buttons(self, buttons):
        for b in buttons.values():
            if b.act:
                b.draw()
            else:
                pyxel.rectb(b.x, b.y, b.w, b.h, 5)
                draw_text(b.x + b.w // 2, b.y + b.h // 2, 1, b.label, 5,
                          align="center", valign="center")
