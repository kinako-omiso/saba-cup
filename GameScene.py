import random

from Card import Card
from advanced_textbox import AdvancedTextBox


CARDS_PER_ROW = 5
CARD_ROWS = 2


def setup(game):
    random.shuffle(game.books)
    game.field_cards = [
        Card(book, *_card_position(index))
        for index, book in enumerate(game.books[:CARDS_PER_ROW * CARD_ROWS])
    ]
    game.book_index = len(game.field_cards)
    game.reading_index = 0
    game.reading_box = AdvancedTextBox(40, 390, 520, 120, 7, 1, s=15, auto=False) ##sで表示するフレーム間隔を指定
    _set_reading_text(game)
    game.scores = {1: 0, 2: 0}
    game.card_confirm_held = {
        player.num: player.interaction for player in (game.player_1, game.player_2)
    }
    # 場の座標と、その位置にあるカードのタイトルを確認する。
    for card in game.field_cards:
        print(f"({card.x}, {card.y}) {card.book.title}")


def _card_position(index):
    row, column = divmod(index, CARDS_PER_ROW)
    return 40 + column * 108, 80 + row * 148


def _set_reading_text(game):
    text = ""
    if game.reading_index < len(game.books):
        book = game.books[game.reading_index]
        text = "\n".join((book.opening_hint, book.famous_passage_hint, book.title))
    game.reading_box.set_text(text)


def update(game):
    # すでに一文字以上表示されている問題だけ、札を取れる。
    answer_book = None
    if game.reading_box.text_counter > 0:
        answer_book = game.books[game.reading_index]

    # 同じフレームの選択を集めてから、場のカードを取り除く。
    selections = {}
    for player in (game.player_1, game.player_2):
        was_held = game.card_confirm_held[player.num]
        game.card_confirm_held[player.num] = player.interaction
        if not player.interaction or was_held or answer_book is None:
            continue

        # 決定ボタンを押した瞬間に、正解の札にポインターが重なっているか確認する。
        for index, card in enumerate(game.field_cards):
            if card is None or card.book.id != answer_book.id:
                continue
            if card.contains(player.x, player.y):
                # 同じカードを選んだら中心に近い方を優先する。同距離なら1P。
                priority = (card.distance_squared(player.x, player.y), player.num)
                if index not in selections or priority < selections[index]:
                    selections[index] = priority
            break

    for index, (_, player_num) in selections.items():
        game.field_cards[index] = None
        # 山札が残っていれば、空いた位置に補充して場を10枚に戻す。
        if game.book_index < len(game.books):
            book = game.books[game.book_index]
            card = Card(book, *_card_position(index))
            game.field_cards[index] = card
            game.book_index += 1
            print(f"({card.x}, {card.y}) {card.book.title}")
        # カードを取ったプレイヤーに1点を加える。
        game.scores[player_num] += 1
        print(f"1P: {game.scores[1]}  2P: {game.scores[2]}")
        game.reading_index += 1
        _set_reading_text(game)

    game.reading_box.update()
    return game.reading_index == len(game.books)


def draw(game):
    for card in game.field_cards:
        if card is not None:
            card.draw()
    game.reading_box.draw()
