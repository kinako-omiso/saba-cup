import pyxel


class Card:
    WIDTH = 88
    HEIGHT = 124

    def __init__(self, book, x, y):
        self.book = book
        self.x = x
        self.y = y

    def draw(self):
        pyxel.rect(self.x, self.y, self.WIDTH, self.HEIGHT, 13)

    def contains(self, x, y):
        return self.x <= x < self.x + self.WIDTH and self.y <= y < self.y + self.HEIGHT

    def distance_squared(self, x, y):
        dx = x - (self.x + self.WIDTH / 2)
        dy = y - (self.y + self.HEIGHT / 2)
        return dx * dx + dy * dy
