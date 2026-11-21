import pyxel


CARD_WIDTH = 88
CARD_HEIGHT = 124
CARDS_PER_ROW = 5
CARD_ROWS = 2


def setup(game):
    game.field_books = game.books[:CARDS_PER_ROW * CARD_ROWS]
    game.book_index = len(game.field_books)
    for book in game.field_books:
        print(book.title)


def draw(game):
    for index in range(len(game.field_books)):
        row, column = divmod(index, CARDS_PER_ROW)
        x = 40 + column * 108
        y = 80 + row * 148
        pyxel.rect(x, y, CARD_WIDTH, CARD_HEIGHT, 13)
