import pyxel

import setting


TITLE_FONT_SIZE = 10
title_font = pyxel.Font(str(setting.FONT_PATH), TITLE_FONT_SIZE)


class Card:
    WIDTH = 88
    HEIGHT = 124

    def __init__(self, book, x, y):
        self.book = book
        self.x = x
        self.y = y

    def draw(self):
        #JSONのassetsに指定されたパスからカード画像を読み込んで描画する。
        pyxel.rect(self.x, self.y, self.WIDTH, self.HEIGHT, 13)
        title = self.book.title
        title_x = self.x + (self.WIDTH - title_font.text_width(title)) // 2
        title_y = self.y + (self.HEIGHT - TITLE_FONT_SIZE) // 2
        pyxel.text(title_x, title_y, title, 7, title_font)

    def contains(self, x, y):
        return self.x <= x < self.x + self.WIDTH and self.y <= y < self.y + self.HEIGHT

    def distance_squared(self, x, y):
        dx = x - (self.x + self.WIDTH / 2)
        dy = y - (self.y + self.HEIGHT / 2)
        return dx * dx + dy * dy
