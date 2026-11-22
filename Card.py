import pyxel

from advanced_textbox import normal_font as title_font


TITLE_LEFT_MARGIN = 2
COVER_RIGHT_MARGIN = 12
TITLE_LINE_HEIGHT = 13


class Card:
    WIDTH = 119
    HEIGHT = 168
    TITLE_BAND_WIDTH = WIDTH - COVER_RIGHT_MARGIN

    def __init__(self, book, x, y, cover, color):
        self.book = book
        self.x = x
        self.y = y
        self.cover = cover
        self.color = color
        self.title_lines = []
        line = ""
        for char in book.title:
            if title_font.text_width(line + char) > self.TITLE_BAND_WIDTH - TITLE_LEFT_MARGIN:
                self.title_lines.append(line)
                line = ""
            line += char
        self.title_lines.append(line)

    def draw(self):
        pyxel.rect(self.x, self.y, self.WIDTH, self.HEIGHT, self.color)
        if self.cover is not None:
            width, height = self.cover.width, self.cover.height
            scale = min(self.WIDTH / width, self.HEIGHT / height)
            pyxel.blt(
                self.x + (self.WIDTH - width) / 2,
                self.y + (self.HEIGHT - height) / 2,
                self.cover, 0, 0, width, height, scale=scale,
            )
            return

        for index, line in enumerate(self.title_lines):
            title_y = self.y + 3 + index * TITLE_LINE_HEIGHT
            pyxel.text(self.x + TITLE_LEFT_MARGIN, title_y, line, 0, title_font)

    def contains(self, x, y):
        return self.x <= x < self.x + self.WIDTH and self.y <= y < self.y + self.HEIGHT

    def distance_squared(self, x, y):
        dx = x - (self.x + self.WIDTH / 2)
        dy = y - (self.y + self.HEIGHT / 2)
        return dx * dx + dy * dy
